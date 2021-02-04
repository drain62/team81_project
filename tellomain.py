# import tellopy
from djitellopy import Tello
import time
import cv2
from Aruco import tellopy
import threading
import socket
import time
import datetime
import struct
import sys
import os
'''
from tellopy import crc
from tellopy import logger
from tellopy import event
from tellopy import state
from tellopy import error
from tellopy import video_stream
from utils import *
from protocol import *
from tellopy import dispatcher
from bytebuffer import *
log = logger.Logger('Tello')



class Tello(object):
    EVENT_CONNECTED = event.Event('connected')
    EVENT_WIFI = event.Event('wifi')
    EVENT_LIGHT = event.Event('light')
    EVENT_FLIGHT_DATA = event.Event('fligt_data')
    EVENT_LOG = event.Event('log')
    EVENT_TIME = event.Event('time')
    EVENT_VIDEO_FRAME = event.Event('video frame')
    EVENT_VIDEO_DATA = event.Event('video data')
    EVENT_DISCONNECTED = event.Event('disconnected')
    EVENT_FILE_RECEIVED = event.Event('file received')
    # internal events
    __EVENT_CONN_REQ = event.Event('conn_req')
    __EVENT_CONN_ACK = event.Event('conn_ack')
    __EVENT_TIMEOUT = event.Event('timeout')
    __EVENT_QUIT_REQ = event.Event('quit_req')

    # for backward comaptibility
    CONNECTED_EVENT = EVENT_CONNECTED
    WIFI_EVENT = EVENT_WIFI
    LIGHT_EVENT = EVENT_LIGHT
    FLIGHT_EVENT = EVENT_FLIGHT_DATA
    LOG_EVENT = EVENT_LOG
    TIME_EVENT = EVENT_TIME
    VIDEO_FRAME_EVENT = EVENT_VIDEO_FRAME

    STATE_DISCONNECTED = state.State('disconnected')
    STATE_CONNECTING = state.State('connecting')
    STATE_CONNECTED = state.State('connected')
    STATE_QUIT = state.State('quit')

    LOG_ERROR = logger.LOG_ERROR
    LOG_WARN = logger.LOG_WARN
    LOG_INFO = logger.LOG_INFO
    LOG_DEBUG = logger.LOG_DEBUG
    LOG_ALL = logger.LOG_ALL
'''

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

# imported Tello-Aruco code:

'''
    11 bits(-1024 ~ +1023) x 4 axis = 44 bits
    44 bits will be packed in to 6 bytes(48 bits)
                axis4      axis3      axis2      axis1
         |          |          |          |          |
             4         3         2         1         0
    98765432109876543210987654321098765432109876543210
     |       |       |       |       |       |       |
         byte5   byte4   byte3   byte2   byte1   byte0
'''


me.streamoff()
me.streamon()
# camera = me.get_video_capture()

while True:
    # imageFrame = camera.read()
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))
    # cv2.imshow("The Camera", img)
    # cv2.imshow("Drone Camera", imageFrame)
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
    if startCounter == 0:
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

    cv2.imshow("The Camera", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        # cv2.destroyAllWindows()
        me.end()
        break
