from djitellopy import Tello
import time
import cv2
import transforms3d as tf
import numpy as np

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

'''


def translate():
    T = [50, 50, 50]
    R = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    Z = [0, 0, 0]

    A = tf.affines.compose(T, R, Z)
    print(type(A))


if __name__ == '__main__':
    startCounter = 0
    global me
    me = Tello()
    # drone_setup()
    translate()
