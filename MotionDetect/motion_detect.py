
# python3 motion_detect.py

# https://www.youtube.com/watch?v=kn2-oNTVXfM
# https://github.com/biplob004/Motion-detection-cv2/blob/main/motion_detect.py

import imutils
import cv2
import numpy as np
import time


# motion detection is comparision between previous_frame && current_frame

FRAMES_TO_PERSIST = 10 # Updates the previous frame in every 10th frame from the loop.
MIN_SIZE_FOR_MOVEMENT = 400 # 200 - higher is the number lesser is motion detection sensitivity. (window size)
MOVEMENT_DETECTED_PERSISTENCE = 100 # no. of frame count down before saving the video.



source = "Volumes/imggen/sample.mp4" # webcam| rtsp_url | video file as input
cap = cv2.VideoCapture(source) # Then start the webcam
if not cap.isOpened():
    print("Failed to open")
    exit()

# Init frame variables
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
curr_frame_num = 0
curr_frame_num_mod = 0
first_frame = None
next_frame = None

# Init display font and timeout counters
font = cv2.FONT_HERSHEY_SIMPLEX
delay_counter = 0
movement_persistent_counter = 0

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
# fourcc = cv2.VideoWriter_fourcc(*'XVID') # .avi
out = None

while True:
    transient_movement_flag = False    
    if curr_frame_num_mod == 0:
        print(f"reading {curr_frame_num} of {total_frames}")
    
    ret, frame = cap.read()
    text = "Unoccupied"


    if curr_frame_num == total_frames:
        break

    if not ret:
        print("CAPTURE ERROR")
        break

    # original_frame = frame.copy()

    frame = imutils.resize(frame, width = 750)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None: first_frame = gray    

    delay_counter += 1

    if delay_counter > FRAMES_TO_PERSIST:
        delay_counter = 0
        first_frame = next_frame

        
    next_frame = gray

    frame_delta = cv2.absdiff(first_frame, next_frame)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations = 2)
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if cv2.contourArea(c) > MIN_SIZE_FOR_MOVEMENT:
            if y < 18 and x < 190:
                continue
            # print(f"{x} {y} {w} {h} = {cv2.contourArea(c)}")
            transient_movement_flag = True
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if transient_movement_flag == True:
        movement_persistent_flag = True
        movement_persistent_counter = MOVEMENT_DETECTED_PERSISTENCE
 
    if movement_persistent_counter > 0:
        # text = "Movement Detected " + str(movement_persistent_counter)
        movement_persistent_counter -= 1
    # else:
        # text = "No Movement Detected"

    # print("puttext")
    # cv2.putText(frame, str(text), (10,35), font, 0.75, (255,255,255), 2, cv2.LINE_AA)
    # print("framedelta")
    # frame_delta = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)
    # # cv2.imshow("frame", np.hstack((frame_delta, frame)))
    # print("umshwo")
    # cv2.imshow("frame", frame)
    # print("umshwo2")


    # record video -----------
    if movement_persistent_counter>0 and not out: # for the very first frame
        height, width, _ = frame.shape
        out = cv2.VideoWriter(f'Volumes/imggen/{int(time.time())}_video.mp4',fourcc, 30.0 ,(width, height))
        out.write(frame)
        print("write file")

    if movement_persistent_counter>0 and out:
        out.write(frame)
        print("write frame")

    # Save each clip in separate video file
    # if movement_persistent_counter == 0 and out:
    #     out.release()
    #     out = None
    # ----------------------
    

    # ch = cv2.waitKey(1)
    # if ch & 0xFF == ord('q'):
    #     if out is not None: # saving & exiting on press of q
    #         out.release()
    #         out = None
    #     break
    
    curr_frame_num = curr_frame_num + 1
    if curr_frame_num_mod == 99:
        curr_frame_num_mod = 0
    else:
        curr_frame_num_mod = curr_frame_num_mod + 1

# Cleanup when closed
# cv2.waitKey(0)
# cv2.destroyAllWindows()

if out != None:
    out.release()

cap.release()
print("END")