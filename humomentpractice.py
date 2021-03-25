import cv2
import numpy as np
import math


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


img = cv2.imread(r'C:\Users\hfrey\Desktop\picture2.jpg')
img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))
control = cv2.imread(r'C:\Users\hfrey\Desktop\controlimage.jpg', cv2.IMREAD_GRAYSCALE)
control = cv2.resize(control, (int(control.shape[1] / 2), int(control.shape[0] / 2)))
_, control = cv2.threshold(control, 128, 255, cv2.THRESH_BINARY)
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
blue_mask = cv2.medianBlur(blue_mask, 5)

contours_b, hierarchy_b = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for pic_b, contour_b in enumerate(contours_b):
    area_b = cv2.contourArea(contour_b)

    comp = np.zeros((int(img.shape[0]), int(img.shape[1])))
    cv2.fillPoly(comp, pts=[contour_b], color=(255, 255, 255))
    # _, comp = cv2.threshold(comp, 128, 255, cv2.THRESH_BINARY)
    d1 = cv2.matchShapes(comp, control, cv2.CONTOURS_MATCH_I2, 0)

    # approx_b = cv2.approxPolyDP(contour_b, 0.01*cv2.arcLength(contour_b, True), True)
    # if area_b > 750 and len(approx_b) > 15:
    if d1 < 0.0001:
        print(d1)
        cv2.drawContours(output, contours_b, pic_b, (255, 0, 0), 3)


cv2.imshow("Output", output)
cv2.imshow("mask", blue_mask)
cv2.imshow("control", control)
cv2.imshow("comp", comp)
cv2.waitKey()
