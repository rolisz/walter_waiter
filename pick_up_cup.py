import cv2
import numpy as np
from time import sleep

from color_matcher import ColorMatcher
from perception.pixels2coords import pixels2coords, get_distance_from_cup_width
from get_angles import get_angles
import lynx_motion
#from sift_matcher import SIFTMatcher

cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)

blue_cup = ColorMatcher('pahar_mare_albastru')
#s = SIFTMatcher()
l = lynx_motion.Arm()

init_angles = (77,20,62)
cam_angle = -30
l.setAngles(*init_angles)
l.setCam(cam_angle)
located = 0

while(cap.isOpened()):

    # Take each frame
    #sleep(1)
    _, frame = cap.read()

    big_contours = blue_cup.find_bboxes(frame)
    
    contours = []
    for contour in big_contours:    
        x,y,X,Y = contour
        ratio = float(Y-y)/(X-x+1)
        #if 1.1 <= ratio <= 1.5:
        #print("Size ",x,X,y,Y, frame[y:Y,x:X, :].shape)
           # if  X-x > 250 and Y-y > 180:
                #matches = s.find_match(frame[y:Y,x:X, :])
                #print matches
                #if matches > 5:
        contours.append((x,y,X,Y, 1, 1.2))
        #else:
         #   pass
            #bloody_sliding_window(frame[y:Y,x:X, :])
    
    for x,y,X,Y in big_contours:
        ratio = float(Y-y)/(X-x+1)
        cv2.rectangle(frame,(x-2,y-2),(X, Y),(255,0,0),2)
        cv2.putText(frame, '%0.3f' % ratio, (x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)
        

    for i, (x,y,X,Y, matches, ratio) in enumerate(contours):
        
        cv2.rectangle(frame,(x-2,y-2),(X, Y),(0,255,0),2)
        dist = '%0.2f' % get_distance_from_cup_width(X-x)
        coords = pixels2coords((x+X)/2., Y-(X-x), X-x, cam_angle=cam_angle)#, size=(480,640), hfov=90)
        cv2.putText(frame, dist, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)
        cv2.putText(frame, '%0.3f' % ratio, (x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)
        #cv2.putText(frame, '%d' % matches, (x-40, y+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)
        cv2.putText(frame, '%0.2f %0.2f %0.2f'%coords, (x, y-50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), thickness=2)
        
        
        if x>0 and X<frame.shape[1]:
            located+=1
            if located == 20:
                angles = get_angles(coords[0]-10, -coords[1]+50)
                l.setAngles(*angles)
                located += 1

    cv2.imshow('frame', cv2.resize(frame, (640,360)))
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
    
_, frame = cap.read()

#l.setAngles(*init_angles)
a,b,c= get_angles(50, -200)
l.setAngles(a,b,c, 3)
cap.release()
cv2.destroyAllWindows()