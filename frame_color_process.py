import numpy as np
import cv2
import sys
import time
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


# blue_l = [190, 30, 10]
# blue_u = [240, 100, 100]
# bl = colorConvert(blue_l)
# bu = colorConvert(blue_u)
#
# green_l = [90, 20, 25]
# green_u = [170, 100, 100]
# gl = colorConvert(green_l)
# gu = colorConvert(green_u)
#
# red_l = [220, 20, 20]
# red_u = [360, 100, 100]
# rl = colorConvert(red_l)
# ru = colorConvert(red_u)
#
# yellow_l = [40, 35, 35]
# yellow_u = [65, 100, 100]
# yl = colorConvert(yellow_l)
# yu = colorConvert(yellow_u)
#
#
# blue_lower = np.array(bl, np.uint8)
# blue_upper = np.array(bu, np.uint8)
# green_lower = np.array(gl, np.uint8)
# green_upper = np.array(gu, np.uint8)
# red_lower = np.array(rl, np.uint8)
# red_upper = np.array(ru, np.uint8)
# yellow_lower = np.array(yl, np.uint8)
# yellow_upper = np.array(yu, np.uint8)


counter = 0
max_red = 0
max_blue = 0
max_green = 0
max_yellow = 0
flag = 0
numframes = 5

global control
control = cv2.imread(r'C:\Users\hfrey\Desktop\controlimage.jpg', cv2.IMREAD_GRAYSCALE)
control = cv2.resize(control, (int(control.shape[1] / 2), int(control.shape[0] / 2)))
_, control = cv2.threshold(control, 128, 255, cv2.THRESH_BINARY)


def process_frame(frame):

    max_red = 0
    max_blue = 0
    max_green = 0
    max_yellow = 0

    blue_l = [190, 30, 10]
    blue_u = [240, 100, 100]
    bl = colorConvert(blue_l)
    bu = colorConvert(blue_u)

    green_l = [90, 20, 25]
    green_u = [170, 100, 100]
    gl = colorConvert(green_l)
    gu = colorConvert(green_u)

    red_l = [220, 20, 20]
    red_u = [360, 100, 100]
    rl = colorConvert(red_l)
    ru = colorConvert(red_u)

    yellow_l = [40, 35, 35]
    yellow_u = [65, 100, 100]
    yl = colorConvert(yellow_l)
    yu = colorConvert(yellow_u)

    blue_lower = np.array(bl, np.uint8)
    blue_upper = np.array(bu, np.uint8)
    green_lower = np.array(gl, np.uint8)
    green_upper = np.array(gu, np.uint8)
    red_lower = np.array(rl, np.uint8)
    red_upper = np.array(ru, np.uint8)
    yellow_lower = np.array(yl, np.uint8)
    yellow_upper = np.array(yu, np.uint8)

    imageFrame = frame.copy()
    color = ""
    # make a frame in HSV color scheme
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    kernal = np.ones((5, 5), "uint8")
    # set limits for blue and create a mask with the hsvFrame

    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
    blue_mask = cv2.dilate(blue_mask, kernal)

    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    green_mask = cv2.dilate(green_mask, kernal)

    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    red_mask = cv2.dilate(red_mask, kernal)

    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
    yellow_mask = cv2.dilate(yellow_mask, kernal)

    # res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)
    # res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)
    # # res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)
    # res_yellow = cv2.bitwise_and(imageFrame, imageFrame, mask=yellow_mask)

    blue_mask = cv2.medianBlur(blue_mask, 5)
    # blue_circles = cv2.HoughCircles(blue_mask, cv2.HOUGH_GRADIENT, 1, 100, 75, 40, 50, 0)
    # print(blue_circles)
    # if len(blue_circles[0]) > 1:
    #     blue_circles = np.uint16(np.around(blue_circles))
    #
    #     for pt in blue_circles[0, :]:
    #         x, y, r = pt[0], pt[1], pt[2]
    #         cv2.circle(imageFrame, (x, y), r, (0, 255, 0), 4)
    #         cv2.circle(imageFrame, (x, y), 1, (0, 0, 255), 4)
    #
    green_mask = cv2.medianBlur(green_mask, 5)
    # green_circles = cv2.HoughCircles(green_mask, cv2.HOUGH_GRADIENT, 1, 100, 75, 40, 50, 0)
    # print(green_circles)
    # if len(green_circles[0]) > 1:
    #     green_circles = np.uint16(np.around(green_circles))
    #
    #     for pt in green_circles[0, :]:
    #         x, y, r = pt[0], pt[1], pt[2]
    #         cv2.circle(imageFrame, (x, y), r, (0, 255, 0), 4)
    #         cv2.circle(imageFrame, (x, y), 1, (0, 0, 255), 4)

    contours_b, hierarchy_b = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_g, hierarchy_g = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours_r, hierarchy_r = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_y, hierarchy_y = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for each contour, if it's large enough draw them onto the image

    for pic_b, contour_b in enumerate(contours_b):
        area_b = cv2.contourArea(contour_b)

        comp = np.zeros((int(frame.shape[0]), int(frame.shape[1])))
        cv2.fillPoly(comp, pts=[contour_b], color=(255, 255, 255))
        # _, comp = cv2.threshold(comp, 128, 255, cv2.THRESH_BINARY)
        d1 = cv2.matchShapes(comp, control, cv2.CONTOURS_MATCH_I2, 0)

        # approx_b = cv2.approxPolyDP(contour_b, 0.01*cv2.arcLength(contour_b, True), True)
        # if area_b > 750 and len(approx_b) > 15:
        if d1 < 0.001 and area_b > 750:
            print(d1)
            cv2.drawContours(imageFrame, contours_b, pic_b, (255, 0, 0), 3)
            if area_b > max_blue:
                max_blue = area_b
    for pic_g, contour_g in enumerate(contours_g):
        area_g = cv2.contourArea(contour_g)
        approx_g = cv2.approxPolyDP(contour_g, 0.01*cv2.arcLength(contour_g, True), True)
        if area_g > 750 and len(approx_g) > 15:
            if(area_g > max_green):
                max_green = area_g
            cv2.drawContours(imageFrame, contours_g, pic_g, (0, 255, 0), 3)

    # for pic_r, contour_r in enumerate(contours_r):
    #     area_r = cv2.contourArea(contour_r)
    #     if(area_r > 750):
    #         if(area_r > max_red):
    #             max_red = area_r
    #         cv2.drawContours(imageFrame, contours_r, pic_r, (0, 0, 255), 3)

    for pic_y, contour_y in enumerate(contours_y):
        area_y = cv2.contourArea(contour_y)
        if(area_y > 750):
            if(area_y > max_yellow):
                max_yellow = area_y
            cv2.drawContours(imageFrame, contours_y, pic_y, (0, 255, 255), 3)

    areas = [max_blue, max_red, max_green, max_yellow]

    if(max(areas) == max_blue):
        # print("The color chosen is blue")
        return [0, imageFrame, blue_mask]
    elif(max(areas) == max_green):
        # print("The color chosen is green")
        return [1, imageFrame, blue_mask]
    elif(max(areas) == max_yellow):
        # print("The color chosen is yellow")
        return [2, imageFrame, blue_mask]
    elif(max(areas) == max_red):
        # print("The color chosen is red")
        return [3, imageFrame, blue_mask]
    else:
        print("Houston, we have a problem")
        return [27, imageFrame, blue_mask]
    # show the result
    # cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
    # cv2.imshow('redmask', red_mask)

    # use the "q" key to exit the webcam view
    # if cv2.waitKey(10) & 0xFF == ord('q'):
    #     time_key = time.process_time()
    #     print("Key pressed at time:", time_key)
    #     webcam.release()
    #     cv2.destroyAllWindows()
    #     break


# print("\nOutput Time:", time.process_time())
# print("Kill swtich delay is:", time.process_time() - time_key)
# print("Frames Processed:", counter)
# print("FPS: ", counter/time.process_time())
def main():
    cam = cv2.VideoCapture(0)

    while(True):
        _, frame = cam.read()
        cv2.imshow("Normal Cam", frame)
        result, pFrame, mask = process_frame(frame)
        cv2.imshow("Process", pFrame)
        cv2.imshow("mask", mask)
        # time.sleep(0.25)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
