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
        
        cap = cv2.VideoCapture(self.cam)
        cap.set(3,1280)
        cap.set(4,720)
        blue_cup = ColorMatcher('pahar_mare_albastru')
        
        # We send only one signal, on the 20th frame
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
                cv2.putText(frame, '%0.3f' % ratio, (x, y+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)
                
        
            for x,y,X,Y, matches, ratio in contours:
                
                cv2.rectangle(frame,(x-2,y-2),(X, Y),(0,255,0),2)
                dist = '%0.2f' % get_distance_from_cup_width(X-x)
                coords = pixels2coords((x+X)/2., Y-(X-x), X-x, cam_angle=self.cam_angle)
                cv2.putText(frame, dist, (x, y-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), thickness=2)
                cv2.putText(frame, '%0.2f %0.2f %0.2f'%coords, (x, y-50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), thickness=2)
                
                
                if x>0 and X<frame.shape[1]:
                    located+=1
                    if located == 20:
                        self.emit('cup_appeared', coords)
                        located += 1
            if located>20:
                break
        
            cv2.imshow('frame', cv2.resize(frame, (640,360)))

        
        
            _, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
