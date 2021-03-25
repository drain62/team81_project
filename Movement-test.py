from djitellopy import Tello
import time
import cv2
import transforms3d as tf
import numpy as np


'''
Steps: if using affine matrix transformation
    1. Get xyz coordinates for balloon from camera function
    2. Place this coordinate as our T variable
    3. Compose affine matrix with T variable
    4. Add Affine matrix to previous point
    5. Decompose this matrix and go to xyz point of next balloon
    6. Compose affine matrix with next T variable
'''


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


def takin_off():
    '''# calculate height method
    me.takeoff()
    me.get_height()
    print(me.get_height())
    me.move_up(100 - me.get_height())
    print(me.get_height())
    # me.move_forward(50)
    # me.move_back(50)
    '''

    # mission pad start method
    me.takeoff()
    print('Takeoff Height: ', me.get_height())
    me.enable_mission_pads()
    # me.set_mission_pad_detection_direction(0)
    # me.go_xyz_speed_mid(0, 0, 120, 100, 1)
    # print('Height 1: ', me.get_height())
    me.move_forward(50)
    # me.go_xyz_speed(50, 0, 20, 100)
    me.go_xyz_speed_yaw_mid(0, 0, 40, 100, 0, 1, 2)
    me.move_down(20)
    me.get_height()
    me.move_back(50)

    '''
    print('Height 2: ', me.get_height())
    me.move_left(170)
    me.move_forward(170)
    me.go_xyz_speed_yaw_mid(0, 0, 50, 100, 0, 4, 3)
    me.rotate_clockwise(90)


        me.move_left()
        me.move_right()
        me.move_back()
        me.move_forward()
    '''


def translate():
    # Baker method
    # 1st balloon
    me.move_left(100)
    me.move_forward(50)
    me.move_back(50)
    me.move_right(100)
    me.go_xyz_speed_yaw_mid(0, 0, 200, 100, 0, 1, 2)

    # 2nd balloon
    me.move_right(100)
    me.move_forward(250)
    me.move_back(250)
    me.move_left(100)
    me.move_down(100)
    me.go_xyz_speed_yaw_mid(0, 0, 150, 100, 0, 1, 2)

    # 3rd balloon
    me.move_left(100)
    me.move_forward(150)
    me.move_back(150)
    me.move_right(100)
    me.go_xyz_speed_yaw_mid(0, 0, 100, 100, 0, 1, 2)

    # 4th balloon
    me.move_right(100)
    me.move_forward(50)
    me.move_back(50)
    me.move_left(100)
    '''

    start = np.array([0, 0, 0])
    P1 = np.array([50, 100, 0])
    L1 = P1 - start
    print('1st line: ', L1)
    print('Height 1: ', me.get_height())
    me.go_xyz_speed(int(L1[0]), int(L1[1]), int(L1[2]), 100)

    P2 = np.array([250, -100, 100])
    L2 = P2 - P1
    print('2nd line: ', L2)
    print('Height 2: ', me.get_height())
    me.go_xyz_speed(int(L2[0]), int(L2[1]), int(L2[2]), 100)

    P3 = np.array([150, 100, 50])
    L3 = P3 - P2
    print('3rd line: ', L3)
    print('Height 3: ', me.get_height())
    me.go_xyz_speed(int(L3[0]), int(L3[1]), int(L3[2]), 100)

    P4 = np.array([50, -100, 0])
    L4 = P4 - P3
    print('4th line: ', L4)
    print('Height 4: ', me.get_height())
    me.go_xyz_speed(int(L4[0]), int(L4[1]), int(L4[2]), 100)

    '''
    '''
    T0 = [0, 0, 0]
    R0 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    Z = [0, 0, 0]
    # start = tf.affines.compose(T0, R0, Z)
    start = tf.affines.compose(np.zeros(3), np.eye(3), np.ones(3))
    print('start: ')
    print(start)

    T1 = [50, 100, 0]
    R1 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    P1 = tf.affines.compose(T1, R1, Z)
    L1 = P1 - start
    print('1st line: ')
    print(L1)

    T2 = [250, -100, 100]
    R2 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    P2 = tf.affines.compose(T2, R2, Z)
    L2 = P2 - P1
    print('2nd line: ')
    print(L2)

    T3 = [150, 100, 50]
    R3 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    P3 = tf.affines.compose(T3, R3, Z)
    L3 = P3 - P2
    print('3rd line: ')
    print(L3)

    T4 = [50, -100, -50]
    R4 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    P4 = tf.affines.compose(T4, R4, Z)
    L4 = P4 - P3
    print('4th line: ')
    print(L4)
    '''


if __name__ == '__main__':
    startCounter = 0
    global me
    me = Tello()
    drone_setup()
    takin_off()
    # translate()
    me.end()
