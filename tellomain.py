import time
import cv2
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
    print("Battery:", me.get_battery())

###############################################################################


def testing():
    print("MAde it to test")
    drone_setup()

    me.streamoff()
    me.streamon()
    # camera = me.get_video_capture()

    while True:
        # _, imageFrame = camera.read()
        frame_read = me.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (320, 240))

        if startCounter == 0:
            me.takeoff()
            print(me.get_height())
            # me.move_back(40)
            # me.move_right(20)
            me.move_up(65)
            print(me.get_height())
            # me.move_forward(153)
            me.go_xyz_speed(100, 0, 0, 100)
            # me.rotate_counter_clockwise(180)
            # me.move_forward(40)
            startCounter = 1

        cv2.imshow("The Camera", img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            me.end()


def camera():
    # drone_setup()
    # me.streamoff()
    # me.streamon()
    webcam = cv2.VideoCapture(0)
    i = 0
    while(1):
        # frame_read = me.get_frame_read()
        # myFrame = frame_read.frame
        # img = cv2.resize(myFrame, (320, 240))
        _, imageFrame = webcam.read()
        result, pFrame = process_frame(imageFrame)
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


startCounter = 0
#me = Tello()
print("""Please select what you want to do.\n1: Test Run\n2: Camera Only Run\n3: Competition Trial Run""")
arg = input('Selection: ')
if int(arg) == 1:
    testing()
elif int(arg) == 2:
    camera()
elif int(arg) == 3:
    competition()
else:
    print("not an option")
