from __future__ import print_function
import sys
import cv2
from random import randint
import time
import os
import numpy as np
import errno 
import shutil

# dont put '/' in the end while giving path
VIDEO_PATH= "/home/akarsh/Desktop/video.mp4"
PATH_TO_SAVE= "/home/akarsh/Desktop"
tracker_types = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[2]
tracker = cv2.TrackerKCF_create()
# Read video
video = cv2.VideoCapture(VIDEO_PATH)
# Exit if video not opened.
if not video.isOpened():
    print("Could not open video")
    sys.exit()
# Read first frame.
ok, frame = video.read()
#ok, frame = video.read()
#ok, frame = video.read()
if not ok:
    print('Cannot read video file')
    sys.exit()
## Select boxes
bboxes = []
colors = []
#loop till we select all roi
while True:
    # draw bounding boxes over objects
    # selectROI's default behaviour is to draw box starting from the center
    # when fromCenter is set to false, you can draw box starting from top left corner
    bbox = cv2.selectROI('Select ROI',frame, False)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    print("Press q to quit selecting boxes and start tracking")
    print("Press any other key to select next object")
    k = cv2.waitKey(0) & 0xFF
    if (k == 113):  # q is pressed
        break
print('Selected bounding boxes {}'.format(bboxes))

#create multitracker object
MultiTracker= cv2.MultiTracker_create()

# Initialize Multitracker
try:
    os.mkdir(PATH_TO_SAVE+"/multipt")
except OSError as error:
    if error.errno == errno.EEXIST:
        shutil.rmtree(PATH_TO_SAVE+"/multipt")
        os.mkdir(PATH_TO_SAVE+"/multipt")
    else :print(error)     
i=0
for bbox in bboxes:
    tracker = cv2.TrackerKCF_create()
    MultiTracker.add(tracker,frame,bbox)
    try:
        os.mkdir(PATH_TO_SAVE+"/multipt/"+str(i))
    except OSError as error:
        print(error)
    i=i+1

#Process video by loop
while video.isOpened():
    # Read a new frame
    ok,frame=video.read()
    if not ok:
        break
    # Start timer
    timer = cv2.getTickCount()
    # Update tracker
    ok, boxes = MultiTracker.update(frame)
    #print(format(boxes))
    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    # Draw bounding box
    if ok:
        # Tracking success
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
            crp_frame=frame[p1[1]+2:p2[1]-2,p1[0]+2:p2[0]-2]
            #uncomment for saving frames
            #print(i)
            if np.shape(crp_frame) != ():
                cv2.imwrite(PATH_TO_SAVE+"/multipt/"+str(i)+"/"+str(timer)+".jpg",crp_frame)
        
    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    # Display tracker type on frame
    cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
    # show frame
    cv2.imshow('MultiTracker', frame)
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

# Close the window / Release webcam 
video.release() 

# After we release our webcam, we also release the output 
#out.release()  
  
# De-allocate any associated memory usage  
cv2.destroyAllWindows()

