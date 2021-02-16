from djitellopy import Tello
import time
import cv2


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
d = 0
dh = 130
while True:
    print("Beginning Takeoff:", time.process_time())
    me.takeoff()
    print("Done Takeoff:", time.process_time())
    me.move_up(50)
    curr_height = me.get_height()
    while curr_height > (dh + 5) or curr_height < (dh - 5):
        if curr_height > (dh+5):
            me.move_down(20)
            curr_height = me.get_height()
        if curr_height < (dh-5):
            me.move_up(20)
            curr_height = me.get_height()
    print("Height", curr_height)
    '''
    print("Beginning Move:", time.process_time())
    # me.__send_stick_command()
    me.move_forward(100)
    print("Done Move:", time.process_time())
    '''
    # mission pad detection
    # me.mon()
    me.enable_mission_pads()
    me.set_mission_pad_detection_direction(0)
    '''
    if me.get_mission_pad_id() > 0:
        me.flip_back()
        break
    '''

    while me.get_mission_pad_id() != 4:
        me.move_forward(100)
        d += 100
        if d == 500:
            me.move_back(d)
            me.end()
        print("Haven't found mission pad\n")

    print("Found mission pad\n")
    # me.flip_back()
    me.move_back(d)
    me.end()
    break
    #print("Beginning Move Back:", time.process_time())
    # me.move_back(100)
    #print("Done Move Back:", time.process_time())
    '''
    me.stop()
    if cv2.waitKey(10) & 0xFF == ord('q'):
        # cv2.destroyAllWindows()
        me.end()
        break
    '''
