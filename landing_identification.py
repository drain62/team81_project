import numpy as np
import cv2
import sys
import time
import scipy
import multiprocessing as mp
from array import *
# print(sys.executable)
# print(sys.version)


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

global q
q = mp.Queue()


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


counter = 0
max_red = 0
max_blue = 0
max_green = 0
max_yellow = 0
flag = 0
numframes = 5


def landing_frame(frame):

    # global control
    # control = cv2.imread(r'C:\Users\hfrey\Desktop\controlimage.jpg', cv2.IMREAD_GRAYSCALE)
    # control = cv2.resize(control, (int(control.shape[1] / 2), int(control.shape[0] / 2)))
    # _, control = cv2.threshold(control, 128, 255, cv2.THRESH_BINARY)

    blue_l = [185, 30, 40]
    blue_u = [240, 100, 100]
    bl = colorConvert(blue_l)
    bu = colorConvert(blue_u)

    green_l = [80, 20, 25]
    green_u = [170, 100, 100]
    gl = colorConvert(green_l)
    gu = colorConvert(green_u)

    red_l = [320, 40, 40]
    red_u = [360, 100, 100]
    rl = colorConvert(red_l)
    ru = colorConvert(red_u)

    red2_l = [0, 40, 40]
    red2_u = [15, 100, 100]
    rl2 = colorConvert(red2_l)
    ru2 = colorConvert(red2_u)

    rgb_red_l = [260, 0, 0]
    rgb_red_u = [360, 100, 100]

    yellow_l = [35, 15, 15]
    yellow_u = [75, 100, 100]
    yl = colorConvert(yellow_l)
    yu = colorConvert(yellow_u)

    blue_lower = np.array(bl, np.uint8)
    blue_upper = np.array(bu, np.uint8)
    green_lower = np.array(gl, np.uint8)
    green_upper = np.array(gu, np.uint8)
    red_lower = np.array(rl, np.uint8)
    red_upper = np.array(ru, np.uint8)
    red2_lower = np.array(rl2, np.uint8)
    red2_upper = np.array(ru2, np.uint8)
    yellow_lower = np.array(yl, np.uint8)
    yellow_upper = np.array(yu, np.uint8)

    rgb_red_l = np.array(rgb_red_l, np.uint8)
    rgb_red_u = np.array(rgb_red_u, np.uint8)
    imageFrame = frame.copy()

    height = imageFrame.shape[0]
    width = imageFrame.shape[1]

    lineX = int(width/2) - 30
    twolineX = int(width/2) + 30
    lineY = int(height/2) + 60

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    #rgbFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)
    kernal = np.ones((5, 5), "uint8")

    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
    blue_mask = cv2.dilate(blue_mask, kernal)

    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    green_mask = cv2.dilate(green_mask, kernal)

    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    red_mask = cv2.dilate(red_mask, kernal)

    red_mask2 = cv2.inRange(hsvFrame, red2_lower, red2_upper)
    red_mask2 = cv2.dilate(red_mask, kernal)

    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
    yellow_mask = cv2.dilate(yellow_mask, kernal)

    # rgb_red_mask = cv2.inRange(rgbFrame, rgb_red_l, rgb_red_u)
    # rgb_red_mask = cv2.dilate(rgb_red_mask, kernal)

    blue_mask = cv2.medianBlur(blue_mask, 5)
    green_mask = cv2.medianBlur(green_mask, 5)
    red_mask = cv2.medianBlur(red_mask, 3)
    yellow_mask = cv2.medianBlur(yellow_mask, 5)
    red_mask2 = cv2.medianBlur(red_mask2, 3)
    # rgb_red_mask = cv2.medianBlur(rgb_red_mask, 5)

    final_red_mask = (red_mask | red_mask2)  # & rgb_red_mask

    contours_b, hierarchy_b = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_g, hierarchy_g = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_r, hierarchy_r = cv2.findContours(
        final_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_y, hierarchy_y = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for each contour, if it's large enough draw them onto the image

    allColors = []
    allColors.extend(contours_b)
    allColors.extend(contours_g)
    allColors.extend(contours_r)
    allColors.extend(contours_y)
    # print(allColors)

    move = ""

    for pic_b, contour_b in enumerate(contours_b):
        area = cv2.contourArea(contour_b)
        if area > 5:
            cv2.drawContours(imageFrame, contour_b, -1, (0, 0, 255), 3)
            M = cv2.moments(contour_b)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)

            if cY <= lineY:
                if cX < lineX:
                    move = "left"
                elif cX > twolineX:
                    move = "right"
                else:
                    move = "forward"
            else:
                if cX < lineX:
                    move = "left"
                elif cX > twolineX:
                    move = "right"
                else:
                    move = "land"

    if move == "land":
        return [move, imageFrame]

    for pic_g, contour_g in enumerate(contours_g):
        area = cv2.contourArea(contour_g)
        if area > 5:
            cv2.drawContours(imageFrame, contour_g, -1, (0, 255, 0), 3)
            M = cv2.moments(contour_g)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)

            if cY <= lineY:
                if cX < lineX:
                    move = "left"
                elif cX > twolineX:
                    move = "right"
                else:
                    move = "forward"
            else:
                if cX < lineX:
                    move = "left"
                elif cX > twolineX:
                    move = "right"
                else:
                    move = "land"

            cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)

    if move == "land":
        return [move, imageFrame]

    for pic_r, contour_r in enumerate(contours_r):
        area = cv2.contourArea(contour_r)

        if area > 5:
            cv2.drawContours(imageFrame, contour_r, -1, (0, 0, 255), 3)
            M = cv2.moments(contour_r)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)

            if cY <= lineY:
                if cX < lineX:
                    move = "left"
                elif cX > twolineX:
                    move = "right"
                else:
                    move = "forward"
            else:
                if cX < lineX:
                    move = "left"
                elif cX > twolineX:
                    move = "right"
                else:
                    move = "land"

    if move == "land":
        return [move, imageFrame]

    # for pic_y, contour_y in enumerate(contours_y):
    #     area = cv2.contourArea(contour_y)
    #
    #     if area > 10:
    #         cv2.drawContours(imageFrame, contour_y, pic_y, (125, 125, 255), 3)
    #         M = cv2.moments(contour_y)
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #
    #         cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)
    #
    #         if cY <= lineY:
    #             if cX < lineX:
    #                 move = "left"
    #             elif cX > twolineX:
    #                 move = "right"
    #             else:
    #                 move = "forward"
    #         else:
    #             if cX < lineX:
    #                 move = "left"
    #             elif cX > twolineX:
    #                 move = "right"
    #             else:
    #                 move = "land"

    cv2.line(imageFrame, (lineX, 0), (lineX, height), (255, 255, 255), 3)
    cv2.line(imageFrame, (twolineX, 0), (twolineX, height), (255, 255, 255), 3)

    cv2.line(imageFrame, (0, lineY), (width, lineY), (255, 255, 255), 3)

    return [move, imageFrame]
    # move = ""
    # biggest = 0
    # areas = [biggest_blue, biggest_green, biggest_red, biggest_yellow]
    # biggest = max(areas)
    # found_contour = []
    # if biggest == 0:
    #     move = "forward"
    # elif biggest == biggest_blue:
    #     found_contour = found_blue
    # elif biggest == biggest_green:
    #     found_contour = found_green
    # elif biggest == biggest_red:
    #     found_contour = found_red
    # elif biggest == biggest_yellow:
    #     found_contour = found_yellow
    #
    # if found_contour != []:
    #     M = cv2.moments(found_contour)
    #     cX = int(M["m10"] / M["m00"])
    #     cY = int(M["m01"] / M["m00"])
    #
    #     cv2.drawContours(imageFrame, found_contour, -1, (255, 255, 255), 3)
    #     cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)
    #
    #     if cY <= lineY:
    #         if cX < lineX:
    #             move = "left"
    #         elif cX > twolineX:
    #             move = "right"
    #         else:
    #             move = "forward"
    #     else:
    #         if cX < lineX:
    #             move = "left"
    #         elif cX > twolineX:
    #             move = "right"
    #         else:
    #             move = "land"


def camera(q):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    thisone = True
    i = 0
    while(True):
        i += 1

        _, frame = cam.read()
        cv2.imshow("Normal Cam", frame)
        # result, pFrame, bm, gm, ym, rm = process_frame(frame, control)
        pFrame, result = landing_frame(frame)
        q.put(result)

        print("Results:", result)
        cv2.imshow("Process", pFrame)
        # cv2.imshow("blue", bm)
        #cv2.imshow("red", rm)
        # cv2.imshow("yellow", ym)
        # cv2.imshow("green", gm)
        # if q.get() == [1] and thisone:
        #     q.put(result)
        #     thisone = False
        # else:
        #     pass
        # time.sleep(0.5)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    return


if __name__ == '__main__':
    # parent_conn, child_conn = mp.Pipe()
    # parent_conn.send([0])

    p1 = mp.Process(target=camera, args=(q, ))
    p1.start()

    # time.sleep(20)

    # time.sleep(4)
    # while(p1.is_alive()):
    # print("q", q.get())
    # parent_conn.send([1])
    # print("result", parent_conn.recv())
    cv2.destroyAllWindows()
    p1.join()
    cv2.destroyAllWindows()
    print("q", q.get())
