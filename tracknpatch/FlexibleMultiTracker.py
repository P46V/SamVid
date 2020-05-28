from __future__ import print_function
import sys
import cv2
from random import randint
import time
import os
import numpy as np
import errno 
import shutil

VIDEO_PATH= "/home/akarsh/Desktop/video.mp4"
PATH_TO_SAVE= "/home/akarsh/Desktop"
tracker = cv2.TrackerKCF_create()
multitracker = cv2.MultiTracker_create()
# Read video
video = cv2.VideoCapture(VIDEO_PATH)
# Exit if video not opened.
if not video.isOpened():
    print("Could not open video")
    sys.exit()
try:
    os.mkdir(PATH_TO_SAVE+"/multipt")
except OSError as error:
    if error.errno == errno.EEXIST:
        shutil.rmtree(PATH_TO_SAVE+"/multipt")
        os.mkdir(PATH_TO_SAVE+"/multipt")
    else :print(error)
# Read frames.
p=0
while True:
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        break
    # Start timer
    timer = cv2.getTickCount()
    # resize the frame (so we can process it faster)
    #frame = imutils.resize(frame, width=600)

    ok, boxes = multitracker.update(frame)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    # loop over the bounding boxes and draw then on the frame
    if ok:
        for i,box in enumerate(boxes):
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame,(x,y),(x+w,y+h), (0, 255, 0), 2)
            crp_frame=frame[y+2:y+h-2,x+2:x+w-2]
            #uncomment for saving frames
            if np.shape(crp_frame) != ():
                cv2.imwrite(PATH_TO_SAVE+"/multipt/"+str(i)+"/"+str(timer)+".jpg",crp_frame)

    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    # Display tracker type on frame
    cv2.putText(frame, " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
    # show frame
    cv2.imshow("Frame",frame)
    key=cv2.waitKey(33) & 0xFF
    # if the 's' key is selected, we are going to "select" a bounding
	# box to track
    if key==ord("s"):
        # select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
        box=cv2.selectROI("Frame",frame,fromCenter=False,showCrosshair=True)
        #making new folder for new object
        try:
            os.mkdir(PATH_TO_SAVE+"/multipt/"+str(p))
            p=p+1
        except OSError as error:
            print(error)
        # create a new object tracker for the bounding box and add it
		# to our multi-object tracker
        tracker = cv2.TrackerKCF_create()
        multitracker.add(tracker, frame, box)
    # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break
video.release()
# close all windows
cv2.destroyAllWindows()
