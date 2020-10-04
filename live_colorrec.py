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
4. Define the range of each color to create mask
5. Morphological Transform: Dilation to remove noise from images
6. Perform bitwise and between image frame and mask to detect paticular color
7. Find contour of each correctly colored object and trace around it
8. Output detection of colors in real time
'''

webcam = cv2.VideoCapture(0)

while(1):
    _, imageFrame = webcam.read()

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
    kernal = np.ones((5, 5), "uint8")

    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    edges = cv2.Canny(imageFrame, 100, 200)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 500):
            cv2.drawContours(imageFrame, contours, pic, (255, 0, 0), 3)
        '''
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h),
                                       (0, 0, 255), 2)
            cv2.putText(imageFrame, "Red Color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))'''

    cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
    cv2.imshow("Edges", edges)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
