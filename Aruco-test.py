from Aruco import *
from tellopy import *
import cv2
import time


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
# print("Battery:", me.get_battery())


while True:
    print("Beginning Takeoff:", time.process_time())
    me.takeoff()
    print("Done Takeoff:", time.process_time())

    print("Beginning Move:", time.process_time())
    me.__send_stick_command()
    me.move_forward(100)
    print("Done Move:", time.process_time())

    print("Beginning Move Back:", time.process_time())
    me.move_back(100)
    print("Done Move Back:", time.process_time())

    me.stop()
    if cv2.waitKey(10) & 0xFF == ord('q'):
        # cv2.destroyAllWindows()
        me.end()
        break
