import numpy as np
import cv2
import sys
print(sys.executable)
print(sys.version)


'''
Steps:
1. Input camera video of webcam
2. Read the video stream in image frames
3. Convert imageFrame from BGR to HSV color spaces orrrrr
4. Define the range of each color to create mask dhdhdhdhh
5. Morphological Transform: Dilation to remove noise from images
6. Perform bitwise and between image frame and mask to detect paticular color
7. Find contour of each correctly colored object and trace around it
8. Output detection of colors in real time
'''


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


blue_l = [160, 30, 20]
blue_u = [300, 100, 100]
bl = colorConvert(blue_l)
bu = colorConvert(blue_u)


green_l = []
# b = [264, 100, 50]
# print(colorConvert(b))

webcam = cv2.VideoCapture(0)

while(1):
    # reads each frame as an image
    _, imageFrame = webcam.read()
    color = ""
    # make a frame in HSV color scheme
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # set limits for blue and create a mask with the hsvFrame

    blue_lower = np.array(bl, np.uint8)
    blue_upper = np.array(bu, np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    kernal = np.ones((5, 5), "uint8")
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

    # search for the contours within the mask
    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    # for each contour, if it's large enough draw them onto the image
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1000):
            cv2.drawContours(imageFrame, contours, pic, (255, 0, 0), 3)
            # print("there is a blue object")
        '''
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h),
                                       (0, 0, 255), 2)
            cv2.putText(imageFrame, "Red Color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))'''

    # show the result
    cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
    cv2.imshow('bluemask', blue_mask)

    # use the "q" key to exit the webcam view
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
