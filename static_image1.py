import numpy as np
import sys
import argparse
import cv2

print(sys.executable)
print(sys.version)

global control
control = cv2.imread(r'C:\Users\hfrey\Desktop\newcontrol1.jpg', cv2.IMREAD_GRAYSCALE)
control = cv2.resize(control, (int(control.shape[1] / 2), int(control.shape[0] / 2)))
_, control = cv2.threshold(control, 128, 255, cv2.THRESH_BINARY)


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


blue_l = [180, 30, 40]
blue_u = [245, 100, 100]
bl = colorConvert(blue_l)
bu = colorConvert(blue_u)
print('bl', bl)
print('bu', bu)
blue_lower = np.array(bl, np.uint8)
blue_upper = np.array(bu, np.uint8)
kernal = np.ones((5, 5), "uint8")

image1 = cv2.imread(r'C:\Users\hfrey\Desktop\blue.jpg')
height = image1.shape[0]
width = image1.shape[1]
image1 = cv2.resize(image1, (int(width/2), int(height/2)))
image = image1.copy()
hsvFrame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
blue_mask = cv2.dilate(blue_mask, kernal)
contours_b, hierarchy_b = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for pic_b, contour_b in enumerate(contours_b):
    area_b = cv2.contourArea(contour_b)

    comp = np.zeros((int(image1.shape[0]), int(image1.shape[1])))
    cv2.fillPoly(comp, pts=[contour_b], color=(255, 255, 255))
    # _, comp = cv2.threshold(comp, 128, 255, cv2.THRESH_BINARY)
    d1 = cv2.matchShapes(comp, control, cv2.CONTOURS_MATCH_I2, 0)
    print("d1", d1)
    if d1 < 0.01 and area_b > 300:
        # print(d1)
        cv2.drawContours(image, contours_b, pic_b, (255, 255, 255), 3)

        M = cv2.moments(contour_b)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # print("Center Coordinates: ", cX, ", ", cY)
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)

while True:
    cv2.imshow('image', image1)
    cv2.imshow("comp", control)
    cv2.imshow('mask', blue_mask)
    cv2.imshow('output', image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

cv2.waitKey(0)
