import cv2
import event

from color_matcher import ColorMatcher
from perception.pixels2coords import pixels2coords, get_distance_from_cup_width

#from sift_matcher import SIFTMatcher


class CupRecognizer(event.EventEmitter):
    def __init__(self, ev, cam, cam_angle):
        self.cam = cam
        self.cam_angle = cam_angle
        super(CupRecognizer, self).__init__(ev)

    def run(self):

        # We send only one signal, on the 20th frame

        while(cap.isOpened()):

            # Take each frame
            #sleep(1)
            _, frame = cap.read()


            cv2.imshow('frame', cv2.resize(frame, (640, 360)))

        cap.release()
        cv2.destroyAllWindows()
