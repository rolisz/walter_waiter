import cv2
import numpy as np
from color_matcher import ColorMatcher

cv2.namedWindow('image')
cap = cv2.VideoCapture(0)

blue_cup = ColorMatcher('pahar_mare_albastru')
_, frame = cap.read()

while(1):

    # Take each frame
    _, frame = cap.read()

    big_contours = blue_cup.find_bboxes(frame)
    for x,y,X,Y in big_contours:
        frame = cv2.rectangle(frame,(x,y),(X, Y),(0,255,0),2)

    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

_, frame = cap.read()
cv2.destroyAllWindows()

