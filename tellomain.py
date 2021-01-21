from djitellopy import Tello
import cv2

width = 320
height = 240
startCounter = 0

# initialization
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0


print(me.get_battery())


me.streamoff()
me.streamon()

while True:
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))
    cv2.imshow("The Camera", img)

    if startCounter == 0:
        me.takeoff()
        print(me.get_height())
        me.move_back(40)
        # me.move_right(20)
        me.rotate_clockwise(180)
        me.rotate_counter_clockwise(180)
        me.move_forward(40)
        startCounter = 1

    # cv2.imshow("The Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        me.streamoff()
        me.land()
        break
