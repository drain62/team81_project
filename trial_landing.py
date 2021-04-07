import time
import cv2
import numpy
from scipy import stats
import multiprocessing as mp
from frame_color_process import process_frame
from landing_identification import landing_frame
from djitellopy import Tello

global q
q = mp.Queue()


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


def landing(q, drone):
    i = 0
    first = True
    while(i < 1000):
        time.sleep(3)
        i += 1

        frame_read = drone.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (320, 240))
        cv2.imshow("OG Img", img)

        command, pFrame = landing_frame(img)
        cv2.imshow("Processed Frame", pFrame)

        q.put(command)
        if command == "land" and first:
            return
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def main():
    global me
    me = Tello()

    drone_setup()

    me.enable_mission_pads()
    me.set_mission_pad_detection_direction(2)
    p1 = mp.Process(target=landing, args=(q, me))

    me.takeoff()

    me.go_xyz_speed_yaw_mid(0, 0, 75, 100, 0, 4, 3)
    me.move_down(45)

    p1.start()
    copy = ""
    command = ""
    while p1.is_alive() and command != "land":
        time.sleep(4)
        command = q.get()
        if copy == command:
            copy = ""
            continue
        elif copy == "":
            copy = command

        if command == "left":
            me.move_left(20)
        elif command == "right":
            me.move_right(20)
        elif command == "forward":
            me.move_forward(20)

    p1.join()
    me.move_forward(55)
    me.end()


if __name__ == '__main__':
    main()
