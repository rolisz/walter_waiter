import cv2
import numpy as np
from color_matcher import ColorMatcher
from perception.pixels2coords import get_distance_from_cup_width


cv2.namedWindow('image')
cap = cv2.VideoCapture(1)

blue_cup = ColorMatcher('pahar_mare_mov')

while(cap.isOpened()):

    # Take each frame
    _, frame = cap.read()

    big_contours = blue_cup.find_bboxes(frame)
    print len(big_contours)
    for x,y,X,Y in big_contours:
        cv2.rectangle(frame,(x-2,y-2),(X, Y),(0,255,0),2)
        dist = '%0.2f' % get_distance_from_cup_width(X-x)
        cv2.putText(frame, dist, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)

    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

_, frame = cap.read()

cap.release()
cv2.destroyAllWindows()

