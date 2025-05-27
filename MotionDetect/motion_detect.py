
# python3 motion_detect.py

# https://www.youtube.com/watch?v=kn2-oNTVXfM
# https://github.com/biplob004/Motion-detection-cv2/blob/main/motion_detect.py

import imutils
import cv2
import numpy as np
import time # remove?
from datetime import datetime

import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

# motion detection is comparision between previous_frame && current_frame

class MotionDetect:
    FRAMES_TO_PERSIST = 10 # Updates the previous frame in every 10th frame from the loop.
    MIN_SIZE_FOR_MOVEMENT = 200 #400 # 200 - higher is the number lesser is motion detection sensitivity. (window size)
    MAX_SIZE_FOR_MOVEMENT = 200000
    MOVEMENT_DETECTED_PERSISTENCE = 100 # no. of frame count down before saving the video.
    LIMIT_TOTAL_FRAMES = -1
    MUST_SEPARATE_CUT = True
    EXTENSION = "mp4"
    FRAMES_BEFORE_CUT = MOVEMENT_DETECTED_PERSISTENCE + 100

    cap = None
    output_path = ""
    camera_name = ""
    movement_persistent_counter = 0

    def __init__(self):
        # Init frame variables
        self.cap = None
        self.total_frames = 0
        self.frame_processed_counter = 0
        self.frame_saved_counter = 0
        
        self.movement_persistent_counter = 0  
        self.cut_persistent_counter = 0      
        self.out = None
        self.out_full = None
        self.current_hour = self.get_current_hour()
        self.hours = 0
        self.hours_to_cut = 0

        self.frame_pivot = None
        self.frame_size_diff = 0
        self.frame_diff_coord = None

        self.blur_amount = 29 #21 #only odds
        self.avoid_x = 0
        self.avoid_y = 0

        self.fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        # fourcc = cv2.VideoWriter_fourcc(*'XVID') # .avi
        self.font = cv2.FONT_HERSHEY_SIMPLEX # for display only

    def apply(self, source, output_path):
        self.cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG) # Then start the webcam
        if not self.cap.isOpened():
            print("Failed to open")
            return
        
        self.output_path = output_path
        if (self.LIMIT_TOTAL_FRAMES < 1):
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) # if stream, going to be negative
        else:
            self.total_frames = self.LIMIT_TOTAL_FRAMES

        print(self.total_frames)
        
        self.process()

    def get_current_hour(self):
        current_datetime = datetime.now()
        return current_datetime.hour

    def process(self):
        self.delay_counter = 0
        self.print_frame_progress()
        hasFrameLimit = self.total_frames > 0

        while True: 
            if hasFrameLimit and self.frame_processed_counter >= self.total_frames:
                break

            # get frame, no resize
            ret, frame = self.cap.read()
            if not ret:
                print("Frame skipped")
                continue
            
            # frame = self.get_frame()
            # if not frame.any():
            #     print("Frame skipped")
            #     continue

            self.checkHour()
            self.recordFull(frame)
            
            self.frame_processed_counter += 1
            if self.movement_persistent_counter > 0:
                self.movement_persistent_counter -= 1
                self.record(frame)
                if self.movement_persistent_counter == 0:
                    self.frame_pivot = None
                continue
            
            if self.MUST_SEPARATE_CUT == True and self.cut_persistent_counter > 0:
                self.cut_persistent_counter -= 1
                if self.cut_persistent_counter == 0:
                    self.cutRecord()

            self.process_frame(frame)
            if (self.frame_processed_counter % 50 == 0):
                self.print_frame_progress()


        self.close()

    def get_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            print("CAPTURE ERROR")
            return list()

        return frame
        # return imutils.resize(frame, width = 750) # TODO

    def process_frame(self, frame):
        gray = self.prepare_frame(frame)

        if self.check_update_pivot_frame(gray) == False:
            self.frame_size_diff = 0
            self.frame_diff_coord = None
            return

        if self.compare_frames(self.frame_pivot, gray) == False:
            return
        
        self.movement_persistent_counter = self.MOVEMENT_DETECTED_PERSISTENCE
        self.cut_persistent_counter = self.FRAMES_BEFORE_CUT
        # self.display(frame)
        self.record(frame)
        # self.saveSeparated()

    def prepare_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (self.blur_amount, self.blur_amount), 0)
        return gray

    def check_update_pivot_frame(self, new_frame):
        if self.frame_pivot is None:
            self.frame_pivot = new_frame
            return False

        self.delay_counter += 1

        # freeze the frame to compare agaist future frames
        if self.delay_counter > self.FRAMES_TO_PERSIST:
            self.delay_counter = 0
            self.frame_pivot = new_frame
            return False
        return True

    def compare_frames(self, frame1, frame2):
        frame_delta = cv2.absdiff(frame1, frame2)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations = 2)
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        biggestDiff = -1
        for c in cnts:
            diffSize = cv2.contourArea(c)
            if diffSize > self.MIN_SIZE_FOR_MOVEMENT and diffSize > biggestDiff and diffSize < self.MAX_SIZE_FOR_MOVEMENT:
                # removing timer
                (x, y, w, h) = cv2.boundingRect(c)
                # print(f"{x} {y} {w} {h} = {cv2.contourArea(c)}")
                if y + h < self.avoid_y and x + w < self.avoid_x:
                    continue
                
                biggestDiff = diffSize
                self.frame_size_diff = biggestDiff
                self.frame_diff_coord = c
        return biggestDiff != -1

    def display(frame):
        text = "Movement Detected " + str(self.movement_persistent_counter) if self.movement_persistent_counter > 0 else "No Movement Detected"
        cv2.putText(frame, str(text), (10,35), self.font, 0.75, (255,255,255), 2, cv2.LINE_AA)
        # frame_delta = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)
        # cv2.imshow("frame", np.hstack((frame_delta, frame)))
        cv2.imshow("frame", frame)

    def record(self, frame):
        # print("write frame")
        if not self.out: # for the very first frame
            height, width, _ = frame.shape
            self.out = cv2.VideoWriter(self.getFileName(False), self.fourcc, 30.0 ,(width, height))

        self.frame_saved_counter += 1
        diff_area_Desc = ""
        if self.frame_size_diff > 1:
            (x, y, w, h) = cv2.boundingRect(self.frame_diff_coord)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(frame, str(self.frame_size_diff), (10,35), self.font, 0.75, (255,255,255), 2, cv2.LINE_AA)
            diff_area_Desc = f"x={x} y={y} w={w} h={h}"
        frame_desc = f"{self.frame_size_diff} - {self.movement_persistent_counter} {diff_area_Desc}"
        cv2.putText(frame, frame_desc, (10,70), self.font, 0.75, (255,255,255), 2, cv2.LINE_AA)
        self.out.write(frame)

    def recordFull(self, frame):
        if not self.out_full: # for the very first frame
            height, width, _ = frame.shape
            self.out_full = cv2.VideoWriter(self.getFileName(True), self.fourcc, 30.0 ,(width, height))
        self.out_full.write(frame)

    def getFileName(self, isFull):
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        extra_folder = "/full" if isFull else ""
        extra = "-full" if isFull else ""
        return f"{self.output_path}{extra_folder}/{current_datetime}-{self.camera_name}{extra}.{self.EXTENSION}"

    def cutRecord(self):
        print("cutRecorded")
        if not self.out:
            return
        self.out.release()
        self.out = None

    def checkHour(self):
        if self.hours_to_cut == 0:
            return
        
        curr_hour = self.get_current_hour()
        if curr_hour == self.current_hour:
            return

        self.current_hour = curr_hour
        self.hours += 1
        if self.hours != self.hours_to_cut:
            return

        self.hours = 0
        self.saveFiles()

    def saveFiles(self):
        if self.out:
            self.out.release()
            self.out = None
        if self.out_full:
            self.out_full.release()
            self.out_full = None
        frame_processed_counter = 0
        frame_saved_counter = 0

    def saveSeparated(self):
        if self.movement_persistent_counter == 0 and out:
            self.out.release()
            self.out = None

    def print_frame_progress(self):
        print(f"reading {self.frame_processed_counter} of {self.total_frames}, saved {self.frame_saved_counter} ")

    def close(self):
        # Cleanup when closed
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if self.out != None:
            self.out.release()

        self.cap.release()
        print("END")