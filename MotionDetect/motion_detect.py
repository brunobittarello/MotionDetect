
# python3 motion_detect.py

# https://www.youtube.com/watch?v=kn2-oNTVXfM
# https://github.com/biplob004/Motion-detection-cv2/blob/main/motion_detect.py

import imutils
import cv2
import numpy as np
import time

# motion detection is comparision between previous_frame && current_frame

class MotionDetect:
    FRAMES_TO_PERSIST = 10 # Updates the previous frame in every 10th frame from the loop.
    MIN_SIZE_FOR_MOVEMENT = 400 # 200 - higher is the number lesser is motion detection sensitivity. (window size)
    MOVEMENT_DETECTED_PERSISTENCE = 100 # no. of frame count down before saving the video.

    cap = None
    output = ""
    movement_persistent_counter = 0

    def __init__(self):
        # Init frame variables
        self.cap = None
        self.total_frames = 0
        self.curr_frame_num = 0
        self.curr_frame_num_mod = 0
        
        self.movement_persistent_counter = 0        
        self.out = None

        self.fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        # fourcc = cv2.VideoWriter_fourcc(*'XVID') # .avi
        # self.font = cv2.FONT_HERSHEY_SIMPLEX # for display only

    def apply(self, source, output):
        self.cap = cv2.VideoCapture(source) # Then start the webcam
        if not self.cap.isOpened():
            print("Failed to open")
            return
        
        self.output = output
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.process()

    def process(self):
        first_frame = None
        next_frame = None
        delay_counter = 0

        while True: 
            if self.curr_frame_num_mod == 0:
                print(f"reading {self.curr_frame_num} of {self.total_frames}")
            
            ret, frame = self.cap.read()

            if self.curr_frame_num == self.total_frames:
                break

            if not ret:
                print("CAPTURE ERROR")
                break

            frame = imutils.resize(frame, width = 750)
            gray = self.prepare_frame(frame)

            if first_frame is None: first_frame = gray    

            delay_counter += 1

            if delay_counter > self.FRAMES_TO_PERSIST:
                delay_counter = 0
                first_frame = next_frame

            next_frame = gray

            if self.compare_frames(first_frame, next_frame) == True:
                self.movement_persistent_counter = self.MOVEMENT_DETECTED_PERSISTENCE
            elif self.movement_persistent_counter > 0:
                self.movement_persistent_counter -= 1

            # self.display(frame)
            self.record(frame)
            # self.saveSeparated()
            # self.stopKey()
            self.nextFrame()

        self.close()

    def prepare_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def nextFrame(self):
        self.curr_frame_num += 1
        if self.curr_frame_num_mod == 99:
            self.curr_frame_num_mod = 0
        else:
            self.curr_frame_num_mod = 1

    def compare_frames(self, frame1, frame2):
        frame_delta = cv2.absdiff(frame1, frame2)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations = 2)
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if cv2.contourArea(c) > self.MIN_SIZE_FOR_MOVEMENT:
                if y < 18 and x < 190:
                    continue
                # print(f"{x} {y} {w} {h} = {cv2.contourArea(c)}")
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                return True
        return False

    def display(frame):
        text = "Movement Detected " + str(self.movement_persistent_counter) if self.movement_persistent_counter > 0 else "No Movement Detected"
        cv2.putText(frame, str(text), (10,35), self.font, 0.75, (255,255,255), 2, cv2.LINE_AA)
        # frame_delta = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)
        # cv2.imshow("frame", np.hstack((frame_delta, frame)))
        cv2.imshow("frame", frame)

    def record(self, frame):
        if self.movement_persistent_counter == 0:
            return

        print("write frame")
        if self.out:
            self.out.write(frame)
            return

        if not self.out: # for the very first frame
            height, width, _ = frame.shape
            self.out = cv2.VideoWriter(self.output, self.fourcc, 30.0 ,(width, height))
            self.out.write(frame)
        

    def saveSeparated(self):
        if self.movement_persistent_counter == 0 and out:
            self.out.release()
            self.out = None

    def stopKey(self):
        ch = cv2.waitKey(1)
        if ch & 0xFF == ord('q'):
            if self.out is not None: # saving & exiting on press of q
                self.out.release()
                self.out = None
            return True
        return False

    def close(self):
        # Cleanup when closed
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if self.out != None:
            self.out.release()

        self.cap.release()
        print("END")

md = MotionDetect()
source = "Volumes/imggen/sample.mp4" # webcam| rtsp_url | video file as input'
output = f'Volumes/imggen/{int(time.time())}_video.mp4'
md.apply(source, output)
