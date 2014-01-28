import numpy as np
import cv2

from time import time

def slide(image, size, step):
    t = time()
    #@todo
    for size in range(400, 500, 30):
        for i in range(0, image.shape[0] - size, size/10):
            for j in range(0, image.shape[1] - size, size/10):
                img2 = image[i:i+size, j:j+size]
                yield img2
    print(time() - t)
