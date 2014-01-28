import numpy as np
import cv2


class SIFTMatcher(object):

    def __init__(self, templ='logo_dan.png', features=cv2.SIFT,
                 min_match_count=10):
       self.min_count = min_match_count
       self.templ_img = cv2.imread(templ)
       self.features = features()

       self.kp, self.des = self.features.detectAndCompute(self.templ_img,
                                                            None)


       FLANN_INDEX_KDTREE = 0
       index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
       search_params = dict(checks = 50)

       self.flann = cv2.FlannBasedMatcher(index_params, search_params)


    def find_match(self, img, lowe_ratio=0.6):
        kp2, des2 = self.features.detectAndCompute(img,None)
        matches = self.flann.knnMatch(self.des,des2,k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < lowe_ratio*n.distance:
                good.append(m)

        print "Matches are found - %d/%d" % (len(good), self.min_count)
        if len(good) > self.min_count:
            src_pts = np.float32([ self.kp[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            try:
                matchesMask = mask.ravel().tolist()
                h,w, c = self.templ_img.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)

            except:
                print "Dumb error - %d/%d" % (len(good), self.min_count)
                return None
        else:
            print "Not enough matches are found - %d/%d" % (len(good), self.min_count)
            return None

        return kp2, matchesMask, dst, good, dst_pts


