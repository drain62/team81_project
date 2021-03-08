import time
import cv2
import multiprocessing as mp
from frame_color_process import process_frame
from djitellopy import Tello
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


def testing():
    # print("Made it to test")
    drone_setup()

    me.streamoff()
    me.streamon()
    # camera = me.get_video_capture()
    startCounter = 0
    blueTotal = 0
    redTotal = 0
    me.takeoff()
    while True:
        #_, imageFrame = camera.read()
        frame_read = me.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (320, 240))
        imgCopy = img.copy()
        # time.sleep(2)
        cv2.imshow("The Camera", img)

        result, pFrame = process_frame(imgCopy)
        cv2.imshow("Process Frame", pFrame)

        if result == 0:
            blueTotal += 1
            if blueTotal == 5:
                me.move_up(20)
                me.land()

        if result == 3:
            redTotal += 1
            if redTotal == 5:
                me.rotate_clockwise(180)
                me.land()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            me.end()


def camera(drone):
    # drone_setup()
    # drone.streamoff()
    # drone.streamon()
    # webcam = cv2.VideoCapture(0)
    i = 0
    while(i < 1000):
        frame_read = drone.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (320, 240))
        imgCopy = img.copy()
        cv2.imshow("Drone", img)
        #_, imageFrame = webcam.read()
        result, pFrame = process_frame(imgCopy)
        print(result)
        cv2.imshow("The Camera", pFrame)
        i += 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
            # me.end()


def competition():
    drone_setup()
    me.streamoff()
    me.streamon()

    while(True):
        frame_read = me.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (320, 240))

        while(True):
            me.takeoff()
            if(process_frame(img) == 1):
                me.move_forward(100)
###############################################################################


if __name__ == '__main__':
    startCounter = 0
    global me
    me = Tello()
    drone_setup()
    p1 = mp.Process(target=camera, args=(me, ))
    p1.start()
    me.takeoff()
    me.rotate_clockwise(360)
    # time.wait(10)
    p1.join()
    me.end()

    if cv2.waitKey(10) & 0xFF == ord('q'):
        me.end()
        cv2.destroyAllWindows()
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
