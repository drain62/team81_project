import numpy as np
import sys
import argparse
import cv2

print(sys.executable)
print(sys.version)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image")
args = vars(ap.parse_args())

image1 = cv2.imread(args["image"])
image = cv2.resize(image1, (500, 500))
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red = np.array([30, 150, 50])
upper_red = np.array([255, 255, 180])

mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(image, hsv, mask=mask)
'''
cv2.imshow('image', image)
cv2.waitkey(5)
cv2.imshow('mask', mask)
cv2.waitkey(0)'''

cv2.imshow('res', res)

cv2.waitKey(0)
