import cv2
import numpy as np

class ColorMatcher(object):

    pahar_mare_rosu = (140, 180)
    pahar_mare_mov = (120, 200)
    pahar_mare_albastru = (90, 120)
    pahar_mic_rosu = (140, 180)
   
    def __init__(self, color):
        """
        Color should be a tuple consisting of low-end of hue value and high-end value of hue,
        or a string containing the variable name that is predefined in the class header.
        """
        if type(color) == str:
            if hasattr(ColorMatcher, color):
                color = getattr(ColorMatcher, color)
            else:
                raise ValueError("Invalid color %s" % color)
        if len(color) != 2 or color[0] > color[1]:
            raise ValueError("Invalid values for color %s" % color)
        self.color = color
            
    def find_bboxes(self, image, kernel_size=10, iterations=3, min_area=200, x_threshold = 25):
        """
        BGR Image to find bounding boxes of objects of given color. Kernel_size is the size of the kernel used
        in the morphological operations, iterations is the number of time the morphological opening should 
        be done. Min_area is the threshold for area for blobs to be considered. x_threshold is the maximum
        distance between a blob's right most part and the next blob's left most part so that they are 
        considered to be in the same bucket.
        Returns a list of contours, as tuples of min_x, min_y, max_x, max_y.
        """
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        h, s, v = self.color[0], 50, 50
        h2, s2, v2 = self.color[1], 255, 255
        
        lower_range = np.array([h,s,v])
        upper_range = np.array([h2,s2,v2])

        kernel = np.ones((kernel_size, kernel_size),np.uint8)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(image, image, mask=mask)
        res = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel, iterations=iterations)

        grey = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)
        #image, contours, hierarchy = cv2.findContours(grey,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        image, contours, hierarchy = cv2.findContours(grey,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        big_contours = []
        for cnt in contours:
            if cv2.contourArea(cnt) > min_area:
                x,y,w,h = cv2.boundingRect(cnt)
                big_contours.append((x,y,w,h))

        big_contours.sort(key=lambda x:x[0])

        if big_contours:
            minX = big_contours[0][0]
            maxX = big_contours[0][0] + big_contours[0][2]

            contour_groups = [[]]
            for x, y, w, h in big_contours:
                if not(minX <= x <= maxX + x_threshold):
                    contour_groups.append([])
                    minX = x
                    maxX = x+w

                contour_groups[-1].append((x,y,x+w,y+h))
                minX = min(x, minX)
                maxX = max(x+w, maxX)

            big_contours = []
            for cg in contour_groups:
                minX = max(min(x[0] for x in cg) - 10, 0)
                maxX = min(max(x[2] for x in cg) + 10, image.shape[1])
                minY = max(min(x[1] for x in cg) - 10, 0)
                maxY = min(max(x[3] for x in cg) + 10, image.shape[0])
                big_contours.append((minX, minY, maxX, maxY))

        return big_contours