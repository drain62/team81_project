import time
import cv2
# from Aruco import tellopy
from djitellopy import Tello


width = 320
height = 240
startCounter = 0
print("Starts Connecting:", time.process_time())
# initialization
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

print("Done Connecting:", time.process_time())
print("Battery:", me.get_battery())


# me.streamoff()
# me.streamon()
#camera = me.get_video_capture()

while True:
    #_, imageFrame = camera.read()
    # frame_read = me.get_frame_read()
    # myFrame = frame_read.frame
    # img = cv2.resize(myFrame, (width, height))
    # cv2.imshow("The Camera", img)
    #cv2.imshow("Drone Camera", imageFrame)
    """
    # if startCounter == 0:
    me.takeoff()
    print(me.get_height())
    # me.move_back(40)
    # me.move_right(20)
    me.move_up(65)
    print(me.get_height())
    me.move_forward(153)
    # me.rotate_counter_clockwise(180)
    # me.move_forward(40)
    #    startCounter = 1

    # cv2.imshow("The Camera", img)
"""
    print("Beginning Takeoff:", time.process_time())
    me.takeoff()
    print("Done Takeoff:", time.process_time())

    print("Beginning Move:", time.process_time())
    me.move_backward(400)
    print("Done Move:", time.process_time())

    me.flip_left()
    me.stop()
    "if cv2.waitKey(10) & 0xFF == ord('q'):"



me.end()
