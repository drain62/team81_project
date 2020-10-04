import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while(1):
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([30, 150, 50])
    upper_red = np.array([255, 255, 180])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Original', frame)

    edges = cv2.Canny(frame, 100, 200)
    cv2.imshow('Edges', edges)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
