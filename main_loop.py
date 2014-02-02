import cv2
import numpy as np
from time import sleep

from color_matcher import ColorMatcher
from perception.pixels2coords import pixels2coords, get_distance_from_cup_width
from get_angles import get_angles
import lynx_motion

@profile
def do_all():
	cv2.namedWindow('image')
	cap = cv2.VideoCapture(0)
	cap.set(3,1280)
	cap.set(4,1024)

	blue_cup = ColorMatcher('pahar_mare_mov')
	l = lynx_motion.Arm()
	while True:
		print "bloody loop"
		# Take each frame
		#sleep(1)
		
		_, frame = cap.read()

		big_contours = blue_cup.find_bboxes(frame)
		for x,y,X,Y in big_contours:
			cv2.rectangle(frame,(x-2,y-2),(X, Y),(0,255,0),2)
			dist = '%0.2f' % get_distance_from_cup_width(X-x)
			coords = pixels2coords((x+X)/2., (y+Y)/2, X-x)
			cv2.putText(frame, dist, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)

			angles = get_angles(coords[0], -coords[1])
			sleep(0.1)
			l.setAngles(*angles)
			
			

		cv2.imshow('frame',frame)
		
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
		
		
	_, frame = cap.read()

	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	do_all()