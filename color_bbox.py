import cv2
import numpy as np

def nothing(arg):
    pass

cv2.namedWindow('image')
cap = cv2.VideoCapture(1)

cv2.createTrackbar('H','image',0,255,nothing)
cv2.createTrackbar('H2','image',0,255,nothing)
_, frame = cap.read()
cv2.imwrite('cam.png', frame)
orb = cv2.SIFT()
while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # h = cv2.getTrackbarPos('H','image')
    h = 140
    s = 100
    v = 100

    # h2 = cv2.getTrackbarPos('H2','image')
    h2 = 180
    s2 = 255
    v2 = 255
    # define range of blue color in HSV
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([h2,s2,v2])

    # find the keypoints with ORB
    # kp = orb.detect(frame,None)

    # compute the descriptors with ORB
    # kp, des = orb.compute(frame, kp)

    # draw only keypoints location,not size and orientation
    # img2 = cv2.drawKeypoints(frame,kp,color=(0,255,0), flags=0)
    kernel = np.ones((5,5),np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    res = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    res = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    res = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    print(res.dtype)
    grey = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)
    image, contours, hierarchy = cv2.findContours(grey,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # res = cv2.drawContours(res, contours, -1, (0,255,0), 3)

    big_countours = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 200:
            print(cnt)
            print(cnt.shape)
            x,y,w,h = cv2.boundingRect(cnt)
            big_countours.append((x,y,w,h))

    big_countours.sort(key=lambda x:x[0])

    print(big_countours)
    if big_countours:
        minX = big_countours[0][0]
        maxX = big_countours[0][0] + big_countours[0][2]
        threshold = 25
        contour_groups = [[]]
        for x, y, w, h in big_countours:
            if not(minX <= x <= maxX+threshold):
                contour_groups.append([])
                minX = x
                maxX = x+w

            contour_groups[-1].append((x,y,x+w,y+h))
            minX = min(x, minX)
            maxX = max(x+w, maxX)

        big_countours = []
        for cg in contour_groups:
            minX = min(x[0] for x in cg) - 5
            maxX = max(x[2] for x in cg) + 5
            minY = min(x[1] for x in cg) -5
            maxY = max(x[3] for x in cg) +5
            big_countours.append((minX, minY, maxX, maxY))

        for x,y,X,Y in big_countours:
            res = cv2.rectangle(res,(x,y),(X, Y),(0,255,0),2)

    cv2.imshow('frame',frame)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

_, frame = cap.read()
cv2.imwrite('cam.png', frame)
cv2.destroyAllWindows()

