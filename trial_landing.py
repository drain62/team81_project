import time
import cv2
import numpy
from scipy import stats
import multiprocessing as mp
from frame_color_process import process_frame
from landing_identification import landing_frame
from djitellopy import Tello

global l
l = mp.Queue()


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
    me.set_mission_pad_detection_direction(0)
    me.takeoff()
    p2 = mp.Process(target=landing, args=(l, me))
    # me.move_down(30)
    me.go_xyz_speed_yaw_mid(0, 0, 75, 100, 0, 4, 3)
    me.move_down(45)
    me.move_forward(100)
    p2.start()
    copy = ""
    command = ""
    j = 0
    done = False
    first = True
    while p2.is_alive() and j < 4:

        i = 0
        if first:
            while i < 7:
                me.move_left(20)
                command = l.get()
                if command == "land":
                    done = True
                    break
                i += 1
            first = False
            if done:
                j = 4
                break
        else:
            while i < 14:
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


if __name__ == '__main__':
    main()
