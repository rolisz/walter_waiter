import numpy as np
import cv2
import random
from time import sleep
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("D:\opencv\data\haarcascades\haarcascade_frontalface_default.xml")


face = None

while True:

    # Take each frame
    _, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    if len(faces) > 0:
        face = random.choice(faces)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imshow('frame', frame)
        sleep(2)
        break
        
    cv2.imshow('frame', frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break



# setup initial location of window
x, y, w, h = face # simply hardcoded the values
track_window = (x, y, w, h)

# set up the ROI for tracking
roi = frame[y:y+h, x:x+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while(1):
    ret ,frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

    # apply meanshift to get the new location
    ret, track_window = cv2.CamShift(dst, track_window, term_crit)

    # Draw it on image
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
    img2 = cv2.polylines(frame,[pts],True, 255,2)
    cv2.imshow('img2',img2)

    k = cv2.waitKey(60) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()


