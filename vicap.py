import numpy as np
import cv2 as cv
'''Creating video-capture object to read frames from input camera/video file
    0 is passed as argument to indicate use of first webcam/camera'''
cap = cv.VideoCapture(0)  
if not cap.isOpened():            #isOpened() checks if video-capture object is initialized properly or not
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()       
'''ret-indicates if frame was read properly or not(value=true if properly read) '''
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)     #cvtcolor() to convert the input frame colour according to second argument
    cv.imshow('frame', gray)                           #imshow() to display frame in a new window with title 'frame' 
    if cv.waitKey(1) == ord('q'):                      #waitKey() to wait for useer input(in millisecond)-- 0 for infinity
        break
cap.release()
cv.destroyAllWindows()
