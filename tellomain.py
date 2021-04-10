import time
import cv2
import numpy
from scipy import stats
import multiprocessing as mp
from frame_color_process import process_frame
from landing_identification import landing_frame
from djitellopy import Tello

global control
control = cv2.imread(r'C:\Users\hfrey\Desktop\control.jpg', cv2.IMREAD_GRAYSCALE)
control = cv2.resize(control, (int(control.shape[1] / 2), int(control.shape[0] / 2)))
_, control = cv2.threshold(control, 128, 255, cv2.THRESH_BINARY)
global q
q = mp.Queue()
global l
l = mp.Queue()

###############################################################################


def drone_setup():
    print("Starts Connecting:", time.process_time())
    me.connect()
    me.for_back_velocity = 0
    me.left_right_velocity = 0
    me.up_down_velocity = 0
    me.yaw_velocity = 0
    me.speed = 0
    me.streamoff()
    me.streamon()
    print("Battery:", me.get_battery())

###############################################################################


def camera(q, drone):
    i = 0
    while(i < 20):
        time.sleep(0.1)
        i += 1

        frame_read = drone.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (320, 240))
        cv2.imshow("OG Img", img)

        result, pFrame = process_frame(img, control)
        cv2.imshow("Processed Frame", pFrame)

        q.put(result)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


###############################################################################


def landing(l, drone):
    i = 0
    while(i < 100):
        time.sleep(1)
        i += 1

        frame_read = drone.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (320, 240))
        cv2.imshow("OG Img", img)

        command, pFrame = landing_frame(img)
        cv2.imshow("Processed Frame", pFrame)

        l.put(command)
        if command == "land":
            return
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


###############################################################################


def main():
    global me
    j = 0

    # Blue - 1
    # Green - 2
    # Red - 3
    # Yellow - 4
    order = [3, 2, 4, 1]
    LUarray = [-1] * 15
    LUarray = numpy.array(LUarray)
    MUarray = [-1] * 15
    MUarray = numpy.array(MUarray)
    RUarray = [-1] * 15
    RUarray = numpy.array(RUarray)
    LMarray = [-1] * 15
    LMarray = numpy.array(LMarray)
    MMarray = [-1] * 15
    MMarray = numpy.array(MMarray)
    RMarray = [-1] * 15
    RMarray = numpy.array(RMarray)
    LLarray = [-1] * 15
    LLarray = numpy.array(LLarray)
    MLarray = [-1] * 15
    MLarray = numpy.array(MLarray)
    RLarray = [-1] * 15
    RLarray = numpy.array(RLarray)

    height_front = 110
    # height_front = 69
    height_mid = 150
    # height_mid = 114
    height_back = 185
    # height_back = 138

    me = Tello()
    drone_setup()

    me.takeoff()
    me.enable_mission_pads()
    me.set_mission_pad_detection_direction(0)
    p1 = mp.Process(target=camera, args=(q, me))

    print("here")
    me.go_xyz_speed_yaw_mid(0, 0, 100, 100, 0, 8, 7)
    # me.go_xyz_speed_mid(0, 0, 100, 100, 1)
    me.move_up(110)
    time.sleep(1.5)
    p1.start()
    while p1.is_alive() and j < 15:
        # me.get_height()
        iteration = q.get()
        LUarray[j] = iteration[0][0]
        MUarray[j] = iteration[0][1]
        RUarray[j] = iteration[0][2]

        LMarray[j] = iteration[1][0]
        MMarray[j] = iteration[1][1]
        RMarray[j] = iteration[1][2]

        LLarray[j] = iteration[2][0]
        MLarray[j] = iteration[2][1]
        RLarray[j] = iteration[2][2]
        j += 1
        print("Result:", iteration)

    allArrays = [LUarray, MUarray, RUarray, LMarray, MMarray, RMarray, LLarray, MLarray, RLarray]
    results = [-1] * 9
    for count, array in enumerate(allArrays):
        if numpy.count_nonzero(array == -1) < 15:
            for i in range(1, 5):
                if i in array:
                    results[count] = i
                    break
        else:
            results[count] = -1

    solution = [[results[0], results[1], results[2]], [results[3], results[4],
                                                       results[5]], [results[6], results[7], results[8]]]

    # modeLU = stats.mode(LUarray)
    # modeMU = stats.mode(MUarray)
    # modeRU = stats.mode(RUarray)
    #
    # modeLM = stats.mode(LMarray)
    # modeMM = stats.mode(MMarray)
    # modeRM = stats.mode(RMarray)
    #
    # modeLL = stats.mode(LLarray)
    # modeML = stats.mode(MLarray)
    # modeRL = stats.mode(RLarray)
    # solution = [[int(modeLU[0]), int(modeMU[0]), int(modeRU[0])], [int(modeLM[0]), int(
    #     modeMM[0]), int(modeRM[0])], [int(modeLL[0]), int(modeML[0]), int(modeRL[0])]]
    #
    #
    #
    # if numpy.count_nonzero(LUarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in LUarray:
    #             LU = i
    #             break
    # else:
    #     LU = -1
    #
    # if numpy.count_nonzero(MUarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in MUarray:
    #             MU = i
    #             break
    # else:
    #     MU = -1
    #
    # if numpy.count_nonzero(RUarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in RUarray:
    #             RU = i
    #             break
    # else:
    #     RU = -1
    #
    # if numpy.count_nonzero(LMarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in LMarray:
    #             LM = i
    #             break
    # else:
    #     LM = -1
    #
    # if numpy.count_nonzero(MMarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in MMarray:
    #             MM = i
    #             break
    # else:
    #     MM = -1
    #
    # if numpy.count_nonzero(RMarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in RMarray:
    #             RM = i
    #             break
    # else:
    #     RM = -1
    #
    # if numpy.count_nonzero(LLarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in LLarray:
    #             LL = i
    #             break
    # else:
    #     LL = -1
    #
    # if numpy.count_nonzero(MLarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in MLarray:
    #             ML = i
    #             break
    # else:
    #     ML = -1
    #
    # if numpy.count_nonzero(RLarray == -1) < 8:
    #     for i in range(1, 5):
    #         if i in RLarray:
    #             RL = i
    #             break
    # else:
    #     RL = -1
    #
    # solution = [[LU, MU, RU], [LM, MM, RM], [LU, MU, RU]]

    print("Solution: ", solution)
    cv2.destroyAllWindows()
    p1.join()

    me.move_down(100)
    me.move_forward(160)
    me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, 4, 3)


# me.go_xyz_speed_mid(0, 0, 115, 100, 2)
#
# if order[0] == solution[2][0]:
#     print("move left")
#     print("move forward")
#     me.move_left(100)
#     me.go_xyz_speed_yaw_mid(0, 0, 110, 100, 0, 4, 3)
#     #me.go_xyz_speed_mid(0, 0, 115, 100, 3)
#     me.move_forward(100)
#     me.move_back(100)
#     me.move_right(100)
# elif order[0] == solution[2][1]:
#     print("move forward")
#     me.move_forward(100)
#     me.move_back(100)
# elif order[0] == solution[2][2]:
#     print("move right")
#     print("move forward")
#     me.move_right(100)
#     me.go_xyz_speed_yaw_mid(0, 0, 110, 100, 0, 6, 5)
#     # me.go_xyz_speed_mid(0, 0, 115, 100, 4)
#     me.move_forward(100)
#     me.move_back(100)
#     me.move_left(100)
#
# me.go_xyz_speed_yaw_mid(0, 0, 110, 100, 0, 2, 1)
# # me.go_xyz_speed_mid(0, 0, 115, 100, 2)
# if order[1] == solution[2][0]:
#     print("move left")
#     print("move forward")
#     me.move_left(100)
#     me.go_xyz_speed_yaw_mid(0, 0, 110, 100, 0, 4, 3)
#     # me.go_xyz_speed_mid(0, 0, 115, 100, 3)
#     me.move_forward(100)
#     me.move_back(100)
#     me.move_right(100)
# elif order[1] == solution[2][1]:
#     print("move forward")
#     me.move_forward(100)
#     me.move_back(100)
# elif order[1] == solution[2][2]:
#     print("move right")
#     print("move forward")
#     me.move_right(100)
#     me.go_xyz_speed_yaw_mid(0, 0, 110, 100, 0, 6, 5)
#     # me.go_xyz_speed_mid(0, 0, 115, 100, 4)
#     me.move_forward(100)
#     me.move_back(100)
#     me.move_left(100)
#
# me.go_xyz_speed_yaw_mid(0, 0, 110, 100, 0, 2, 1)
# # me.go_xyz_speed_mid(0, 0, 115, 100, 2)
# if order[2] == solution[2][0]:
#     print("move left")
#     print("move forward")
#     me.move_left(100)
#     me.go_xyz_speed_yaw_mid(0, 0, 110, 100, 0, 4, 3)
#     # me.go_xyz_speed_mid(0, 0, 115, 100, 3)
#     me.move_forward(100)
#     me.move_back(100)
#     me.move_right(100)
# elif order[2] == solution[2][1]:
#     print("move forward")
#     me.move_forward(100)
#     me.move_back(100)
# elif order[2] == solution[2][2]:
#     print("move right")
#     print("move forward")
#     me.move_right(100)
#     me.go_xyz_speed_yaw_mid(0, 0, 110, 100, 0, 6, 5)
#     # me.go_xyz_speed_mid(0, 0, 115, 100, 4)
#     me.move_forward(100)
#     me.move_back(100)
#     me.move_left(100)
#
# print("\n\nDonezo.")
# me.end()
#
# if cv2.waitKey(10) & 0xFF == ord('q'):
#     print("End command received.")
#     me.end()
#     cv2.destroyAllWindows()
    lfpad = 1
    lbpad = 2
    mfpad = 3
    mbpad = 4
    rfpad = 1
    rbpad = 2

    fdist = 115
    mdist = 220
    bdist = 315
    lateral = 105
    i = 0

    # while i < 4:
    #     if solution[0][0] == order[i]:
    #         print("Chose left back")
    #         me.move_left(lateral)
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
    #         me.move_up(height_back - height_front)
    #         me.move_forward(bdist)
    #         me.move_back(bdist + 10)
    #         me.move_down(height_back - height_front)
    #         me.move_right(lateral)
    #     elif solution[0][1] == order[i]:
    #         print("Chose middle back")
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
    #         me.move_up(height_back - height_front)
    #         me.move_forward(bdist)
    #         me.move_back(bdist + 10)
    #         me.move_down(height_back - height_front)
    #     elif solution[0][2] == order[i]:
    #         print("Chose right back")
    #         me.move_right(lateral)
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
    #         me.move_up(height_back - height_front)
    #         me.move_forward(bdist)
    #         me.move_back(bdist+10)
    #         me.move_down(height_back - height_front)
    #         me.move_left(lateral)
    #
    #     elif solution[1][0] == order[i]:
    #         print("Chose left middle")
    #         me.move_left(lateral)
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
    #         me.move_up(height_mid - height_front)
    #         me.move_forward(mdist)
    #         me.move_back(mdist+10)
    #         me.move_down(height_mid - height_front)
    #         me.move_right(lateral)
    #     elif solution[1][1] == order[i]:
    #         print("Chose center")
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
    #         me.move_up(height_mid - height_front)
    #         me.move_forward(mdist)
    #         me.move_back(mdist+10)
    #         me.move_down(height_mid - height_front)
    #     elif solution[1][2] == order[i]:
    #         print("Chose right back")
    #         me.move_right(lateral)
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
    #         me.move_up(height_mid - height_front)
    #         me.move_forward(mdist)
    #         me.move_back(mdist+10)
    #         me.move_down(height_mid - height_front)
    #         me.move_left(lateral)
    #
    #     elif solution[2][0] == order[i]:
    #         print("Chose left front")
    #         me.move_left(lateral)
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
    #         me.move_forward(fdist)
    #         me.move_back(fdist+5)
    #         me.move_right(lateral)
    #     elif solution[2][1] == order[i]:
    #         print("Chose middle front")
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
    #         me.move_forward(fdist)
    #         me.move_back(fdist+5)
    #     elif solution[2][2] == order[i]:
    #         print("Chose right front")
    #         me.move_right(lateral)
    #         me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
    #         me.move_forward(fdist)
    #         me.move_back(fdist+5)
    #         me.move_left(lateral)
    #
    #     me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mfpad, mbpad)
    #     i += 1
    col = 0  # middle column by default (left = -1, right = 1)

    while i < 4:
        if solution[0][0] == order[i]:
            print("Chose left back")
            if col == 0:
                me.move_left(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist + 15)
                me.move_down(height_back - height_front)
            if col == -1:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist + 15)
                me.move_down(height_back - height_front)
            if col == 1:
                me.move_left(2*lateral)
                # me.move_left(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist + 15)
                me.move_down(height_back - height_front)
            col = -1

        elif solution[0][1] == order[i]:
            print("Chose middle back")
            if col == 0:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist + 15)
                me.move_down(height_back - height_front)
            if col == -1:
                me.move_right(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist + 15)
                me.move_down(height_back - height_front)
            if col == 1:
                me.move_left(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist + 15)
                me.move_down(height_back - height_front)
            col = 0

        elif solution[0][2] == order[i]:
            print("Chose right back")
            if col == 0:
                me.move_right(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist+15)
                me.move_down(height_back - height_front)
            if col == -1:
                me.move_right(2*lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist+15)
                me.move_down(height_back - height_front)
            if col == 1:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_up(height_back - height_front)
                me.move_forward(bdist)
                me.move_back(bdist+15)
                me.move_down(height_back - height_front)
            col = 1

        elif solution[1][0] == order[i]:
            print("Chose left middle")
            if col == 0:
                me.move_left(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            if col == -1:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            if col == 1:
                me.move_left(2*lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            col = -1

        elif solution[1][1] == order[i]:
            print("Chose center")
            if col == 0:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            if col == -1:
                me.move_right(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            if col == 1:
                me.move_left(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            col = 0

        elif solution[1][2] == order[i]:
            print("Chose right back")
            if col == 0:
                me.move_right(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            if col == -1:
                me.move_right(2*lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            if col == 1:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_up(height_mid - height_front)
                me.move_forward(mdist)
                me.move_back(mdist+15)
                me.move_down(height_mid - height_front)
            col = 1

        elif solution[2][0] == order[i]:
            print("Chose left front")
            if col == 0:
                me.move_left(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            if col == -1:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            if col == 1:
                me.move_left(2*lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, lbpad, lfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            col = -1

        elif solution[2][1] == order[i]:
            print("Chose middle front")
            if col == 0:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            if col == -1:
                me.move_right(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            if col == 1:
                me.move_left(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            col = 0

        elif solution[2][2] == order[i]:
            print("Chose right front")
            if col == 0:
                me.move_right(lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            if col == -1:
                me.move_right(2*lateral)
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            if col == 1:
                me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, rbpad, rfpad)
                me.move_forward(fdist)
                me.move_back(fdist+15)
            col = 1

        # me.go_xyz_speed_yaw_mid(0, 0, height_front, 100, 0, mbpad, mfpad)
        i += 1

    if col == 1:
        me.move_left(lateral)
    elif col == -1:
        me.move_right(lateral)

    # command = ""
    # while command != "land":
    #     frame_read = me.get_frame_read()
    #     myFrame = frame_read.frame
    #     img = cv2.resize(myFrame, (320, 240))
    #     command = landing_frame(img)
    #
    #     if command == "left":
    #         me.move_left(20)
    #     elif command == "right":
    #         me.move_right(20)
    #     elif command == "forward":
    #         me.move_forward(20)

    p2 = mp.Process(target=landing, args=(l, me))
    me.move_down(30)
    me.go_xyz_speed_yaw_mid(0, 0, 75, 100, 0, 4, 3)
    me.move_down(45)
    me.move_forward(100)
    p2.start()
    copy = ""
    command = ""
    j = 0
    done = False
    while p2.is_alive() and j < 4:
        # time.sleep(6)

        # if copy == command:
        #     copy = ""
        #     continue
        # elif copy == "":
        #     copy = command
        #
        # if command == "left":
        #     me.move_left(20)
        # elif command == "right":
        #     me.move_right(20)
        # elif command == "forward":
        #     me.move_forward(20)
        i = 0

        while i < 7:
            me.move_left(20)
            command = l.get()
            if command == "land":
                done = True
                break
            i += 1
        if done:
            j = 4
            break
        i = 0
        me.move_forward(40)
        while i < 14:
            me.move_right(20)
            command = l.get()
            if command == "land":
                done = True
                break
            i += 1
        if done:
            j = 4
            break

        me.move_forward(40)
        j += 1

    p2.join()
    me.move_forward(60)
    me.end()


# break
# print("""Please select what you want to do.\n1: Test Run\n2: Camera Only Run\n3: Competition Trial Run""")
# arg = input('Selection: ')
# arg = 1
# if int(arg) == 1:
#     testing()
# elif int(arg) == 2:
#     camera()
# elif int(arg) == 3:
#     competition()
# else:
#     print("not an option")
if __name__ == '__main__':
    main()
