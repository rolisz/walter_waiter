import cv2
import numpy as np
from color_matcher import ColorMatcher
from perception.pixels2coords import pixels2coords, get_distance_from_cup_width


cv2.namedWindow('image')
cap = cv2.VideoCapture(1)

blue_cup = ColorMatcher('pahar_mare_mov')

while(cap.isOpened()):

    # Take each frame
    _, frame = cap.read()

    big_contours = blue_cup.find_bboxes(frame)
    for x,y,X,Y in big_contours:
        cv2.rectangle(frame,(x-2,y-2),(X, Y),(0,255,0),2)
        dist = '%0.2f' % get_distance_from_cup_width(X-x)
        coords = '%0.2f %0.2f %0.2f' % pixels2coords((x+X)/2., (y+Y)/2, X-x)
        cv2.putText(frame, dist, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)
        axis='XYZ'
        for i, coord in enumerate(coords.split(' ')):
            cv2.putText(frame, axis[i]+' '+coord, (x-80, y-30*(i+1)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), thickness=2)
        #print coords

    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

_, frame = cap.read()

cap.release()
cv2.destroyAllWindows()

