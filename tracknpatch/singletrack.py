import cv2
import sys
import time
import numpy as np
import os
import errno
import shutil

if __name__ == '__main__' :
 
    #provide path to video
    VIDEO_PATH= "/home/akarsh/Desktop/video.mp4"
    PATH_TO_SAVE= "/home/akarsh/Desktop"
    # Set up tracker.
    #tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    tracker_type = 'KCF'
    tracker = cv2.TrackerKCF_create()
    # Read video
    video = cv2.VideoCapture("VIDEO_PATH")
    #time.sleep(2.0)
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
    try:
        os.mkdir(PATH_TO_SAVE+"/multipt")
    except OSError as error:
        if error.errno == errno.EEXIST:
            shutil.rmtree(PATH_TO_SAVE+"/multipt")
            os.mkdir(PATH_TO_SAVE+"/multipt")
        else :print(error)
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            crp_frame=frame[p1[1]:p2[1],p1[0]:p2[0]]
            #out.write(crp_frame) not working
            #uncomment for saving frames
            if np.shape(crp_frame) != ():
                if crp_frame.size !=0:
                    cv2.imwrite(PATH_TO_SAVE+"/multipt/"+str(timer)+".jpg",crp_frame)
 
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
    # Close the window / Release webcam 
    video.release() 

    # After we release our webcam, we also release the output 
    out.release()  
  
    # De-allocate any associated memory usage  
    cv2.destroyAllWindows() 
