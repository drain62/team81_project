import cv2
import numpy as np


def colorConvert(a):
    # possible threshold use
    '''if (min == 1):
        thresh = 50
    else:
        thresh = -50'''

    a[0] = ((a[0]) / 2)
    a[1] = (a[1]) * 255/100
    a[2] = (a[2]) * 255/100

    if(a[0] < 0):
        a[0] = 0
    elif(a[0] > 180):
        a[0] = 180

    if(a[1] < 0):
        a[1] = 0
    elif(a[1] > 255):
        a[1] = 255

    if(a[2] < 0):
        a[2] = 0
    elif(a[2] > 255):
        a[2] = 255

    return a


img = cv2.imread(r'C:\Users\hfrey\Desktop\picture.jpg')
img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))
output = img.copy()
gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blue_l = [190, 30, 10]
blue_u = [240, 100, 100]
bl = colorConvert(blue_l)
bu = colorConvert(blue_u)
blue_lower = np.array(bl, np.uint8)
blue_upper = np.array(bu, np.uint8)

hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
kernal = np.ones((5, 5), "uint8")
blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
blue_mask = cv2.dilate(blue_mask, kernal)
blue_mask = cv2.blur(blue_mask, (3, 3))


circles = cv2.HoughCircles(blue_mask, cv2.HOUGH_GRADIENT, 1.5, 100, 150, 60, 60, 0)
if circles is not None:

    circles = np.uint16(np.around(circles))
    print(circles)

    total = 0
    for pt in circles[0, :]:
        total += 1
        x, y, r = pt[0], pt[1], pt[2]
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.circle(output, (x, y), 1, (0, 0, 255), 4)
    cv2.imshow("gray", gimg)
    cv2.imshow("mask", blue_mask)
    cv2.imshow("output", np.hstack([img, output]))
    print("total", total)
    cv2.waitKey(0)
