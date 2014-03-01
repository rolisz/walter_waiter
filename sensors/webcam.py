import numpy as np
import itertools
import cv2
from time import sleep
import os
import math
import event
from color_matcher import ColorMatcher
from sensors.sift_matcher import SIFTMatcher
from pixels2coords import pixels2coords, get_distance_from_cup_width


def distance_between_faces(face1, face2):
    x1, y1, w1, h1 = face1
    x2, y2, w2, h2 = face2
    return math.sqrt((x1 + w1/2.0 - x2 - w2/2.0)**2 +
                     (y1 + h1/2.0 - y2 - h2/2.0)**2)

def distance_to_center(face, size=(640, 480)):
    """
    Get the distance from the center of the faces bounding box to the center of
    the image.

    >>> distance_to_center((270, 200, 20, 20))
    50.0

    >>> distance_to_center((310, 230, 20, 20))
    0.0

    >>> distance_to_center((310, 230, 20, 20), (1024, 768))
    240.0
    """
    x, y, w, h = face
    c_x, c_y = x+w/2.0, y+h/2.0
    return math.sqrt((c_x - size[0]/2.0)**2+(c_y - size[1]/2.0)**2)


def common_area(face1, face2):
    """
    Calculate the percentage of common area for two bounding boxes. Should be 0
    for completely different bounding boxes, 1 for the same.

    >>> common_area((100, 200, 300, 400), (100, 200, 300, 400))
    1.0

    >>> common_area((1, 2, 3, 4), (6, 7, 8, 9))
    0.0

    >>> common_area((100, 100, 100, 100), (150, 100, 100, 100))
    0.5

    >>> round(common_area((100, 100, 100, 100), (150, 100, 100, 200)), 4)
    0.3333
    """
    area = (face1[2]*face1[3] + face2[2]*face2[3])/2.0
    left = max(face1[0], face2[0])
    right = min(face1[0] + face1[2], face2[0]+face2[2])
    top = max(face1[1], face2[1])
    bottom = min(face1[1]+face1[3], face2[1]+face2[3])
    if left < right and top < bottom:
        return (right - left)*(bottom-top)/area
    return 0.0


class Webcam(event.EventEmitter):
    def __init__(self, ev, cam):
        self.cap = cv2.VideoCapture(cam)

        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        super(Webcam, self).__init__(ev)

    def run(self):

        while self.run_flag.is_set():
            _, frame = self.cap.read()

            self.emit('frame', frame)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
            sleep(0.1)
        cv2.destroyAllWindows()
        self.cap.release()


MAX_ITER = 15
class FaceDetector(event.DecisionMaker):
    def __init__(self, ev):
        self.i = MAX_ITER
        #   If this script doesn't work, first check if the paths to the Haar
        # cascades are correct. By default they work on my computer.
        # On other computers they can be overwritten by setting the env
        # variables FACE_HAAR and PROFILE_HAAR to the appropiate values.
        #
        self.face = None
        self.face_cascade = cv2.CascadeClassifier(os.getenv('FACE_HAAR',
            'haarcascades/haarcascade_frontalface_default.xml'
        ))
        self.profile_cascade = cv2.CascadeClassifier(os.getenv('PROFILE_HAAR',
            "haarcascades/haarcascade_profileface.xml"
        ))
        super(FaceDetector, self).__init__(ev)

    def frame(self, frame):
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5,
                           interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = list(self.face_cascade.detectMultiScale(gray, 1.3, 5))
        face2 = self.profile_cascade.detectMultiScale(gray, 1.3, 5)
        faces.extend(face2)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('faces', frame)
        non_dup = set()
        for f1, f2 in itertools.combinations(faces, 2):
            if common_area(f1, f2) > 0.5:
                non_dup.add(tuple(f1))
            else:
                non_dup.add(tuple(f1))
                non_dup.add(tuple(f2))
        if len(non_dup) > 0:
            faces = non_dup
        elif len(faces):
            faces = [tuple(faces[0])]

        if len(faces):
            distances = sorted([(face, distance_to_center(face,
                               (1280, 1024))) for face in faces],
                               key=lambda x: x[0][2]*x[0][3])  # Area of face
            if self.face is None:
                self.face, self.d_c = distances[-1]
            else:
                distances.sort(key=lambda x: distance_between_faces(x[0],
                                                                    self.face))
                if distance_between_faces(self.face, distances[0][0]) < 50:
                    self.face, self.d_c = distances[0]
                else:
                    self.emit('face_gone', self.face)
                    self.i -= 1
                    if self.i == 0:
                        self.face = None
                    self.sleep(0)
                    return
            self.emit('face_pos', tuple(x*2 for x in self.face))
            self.i = MAX_ITER
        elif self.face is not None:
            self.emit('face_gone', self.face)
            self.i -= 1
            if self.i == 0:
                self.face = None
        self.sleep(0)


class TableDetector(event.DecisionMaker):
    def __init__(self, ev):
        self.ev = ev
        self.table_matcher = SIFTMatcher(templ='haarcascades/table.png', min_match_count=20)
        super(TableDetector, self).__init__(ev)

    def frame(self, frame):
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (3*width/4, 3*height/4))
        result = self.table_matcher.find_match(frame)
        if result is not None:
            kp2, matchesMask, dst, good, dst_pts = result
        else:
            cv2.imshow('frame', frame)
            self.sleep(0)
            return
        frame = cv2.polylines(frame,[np.int32(dst)],True, 255)
        cv2.imshow('Table detector', cv2.resize(frame, dsize=None,
                                              fx=0.5, fy=0.5))
        self.emit('table_pos', dst)
        self.sleep(0)

class CupDetector(event.DecisionMaker):
    def __init__(self, ev, cam_angle, cup_color='pahar_mare_albastru'):
        self.frames_seen = 0
        self.cam_angle = cam_angle
        self.cup_color = cup_color
        self.blue_cup = ColorMatcher(cup_color)
        self.ev = ev
        super(CupDetector, self).__init__(ev)

    def frame(self, frame):
        big_contours = self.blue_cup.find_bboxes(frame)

        contours = []
        for contour in big_contours:
            x, y, X, Y = contour
            ratio = float(Y-y)/(X-x+1)
            contours.append((x, y, X, Y, 1, 1.2))

        for x, y, X, Y in big_contours:
            ratio = float(Y-y)/(X-x+1)
            cv2.rectangle(frame, (x-2, y-2), (X, Y), (255, 0, 0), 2)
            cv2.putText(frame, '%0.3f' % ratio, (x, y+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                        thickness=2)
        coords_list = []
        for x, y, X, Y, matches, ratio in contours:
            cv2.rectangle(frame, (x - 2, y - 2), (X, Y), (0, 255, 0), 2)
            dist = '%0.2f' % get_distance_from_cup_width(X-x)
            coords = pixels2coords((x+X)/2., Y-(X-x), X-x,
                                   cam_angle=self.cam_angle)
            cv2.putText(frame, dist, (x, y-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                        thickness=2)
            cv2.putText(frame, '%0.2f %0.2f %0.2f' % coords, (x, y-50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                        thickness=2)
            if x > 0 and X < frame.shape[1]:
                coords_list.append(coords)
            coords_list.sort()
            for x, y, z in coords_list:
                self.frames_seen = min(self.frames_seen + 1, 20)
                if self.frames_seen == 20 and x < 400:
                    print 'cd: Cup appeared: %s' % self.cup_color
                    self.emit('cup_appeared', (x, y, z))
                    self.frames_seen = 0
                    break
        #else:
            #print 'cd: Cups done: %s' % self.cup_color
            #self.emit('cups_done')

        cv2.imshow('Cup detector', cv2.resize(frame, dsize=None,
                                              fx=0.5, fy=0.5))


