import numpy as np
import itertools
import cv2
import random
from time import sleep
import os
import math
import event
from threading import Thread


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


def read_cam(cam):
    cap = cv2.VideoCapture(cam)
    #
    #   If this script doesn't work, first check if the paths to the Haar
    # cascades are correct. By default they work on my computer.
    # On other computers they can be overwritten by setting the env variables
    # FACE_HAAR and PROFILE_HAAR to the appropiate values.
    #
    face_cascade = cv2.CascadeClassifier(os.getenv('FACE_HAAR',
        'D:\opencv\data\haarcascades\haarcascade_frontalface_default.xml'
    ))
    profile_cascade = cv2.CascadeClassifier(os.getenv('PROFILE_HAAR',
        "D:\opencv\data\haarcascades\haarcascade_profileface.xml"
    ))

    while True:
        _, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = list(face_cascade.detectMultiScale(gray, 1.3, 5))
        face2 = profile_cascade.detectMultiScale(gray, 1.3, 5)
        faces.extend(face2)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        yield faces

        if len(faces) > 0:
            face = random.choice(faces)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


class FaceRecognizer(event.EventEmitter):
    def __init__(self, ev, cam):
        self.cam = cam
        super(FaceRecognizer, self).__init__(ev)

    def run(self):
        face = None
        d_c = None

        MAX_ITER = 15
        i = MAX_ITER
        for faces in read_cam(self.cam):
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

            if face is None and len(faces) == 0:
                sleep(0.05)
                continue
            elif len(faces):
                distances = sorted([(face, distance_to_center(face,
                                    (1280, 1024))) for face in faces],
                                   key=lambda x: x[1])
                if face is None:
                    face, d_c = distances[0]
                    self.emit('face_pos', face)
                    i = MAX_ITER
                else:
                    distances.sort(key=lambda x: distance_between_faces(x[0],
                                                                        face))
                    if distance_between_faces(face, distances[0][0]) < 50:
                        self.emit('face_pos', distances[0][0])
                        face, d_c = distances[0]
                        i = MAX_ITER
                    else:
                        self.emit('face_gone', face)
            else:
                if face is not None:
                    self.emit('face_gone', face)
                    i -= 1
                    if i == 0:
                        face = None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    import mock
    f = FaceRecognizer(mock.Mock(), 1)
    f.run()
