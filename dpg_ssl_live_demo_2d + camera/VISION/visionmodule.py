# -*- coding: utf-8 -*-
"""
@Brief: This is a vision module(single robot) for RoboCup Small Size League 
@Version: grSim 4 camera version
@author: Wang Yunkai
"""

import socket
from time import sleep
import VISION.vision_detection_pb2 as detection
import VISION.zss_debug_pb2 as debugs
import BASE.GlobalData as vision_data

VISION_PORT = 23333 # Athena vision port
ROBOT_ID = 6

class VisionModule:
    def __init__(self, VISION_PORT=23333, SENDERIP = '0.0.0.0'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
        self.sock.bind((SENDERIP,VISION_PORT))
        self.robot_info = [0, 0, 0, 0, 0, 0]
        self.ball_info = [0, 0, 0, 0]

    def receive(self):
        data, addr = self.sock.recvfrom(65535)
        # sleep(0.0001) # wait for reading
        return data

    def get_info(self, ROBOT_ID):
        data = self.receive()
        package = detection.Vision_DetectionFrame()
        package.ParseFromString(data)
        vision_data.vision = package
        return package
    
class DEBUG:
    def __init__(self, VISION_PORT=23333, SENDERIP='0.0.0.0'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((SENDERIP, VISION_PORT))
        self.robot_info = [0, 0, 0, 0, 0, 0]
        self.ball_info = [0, 0, 0, 0]

    def receive(self):
        data, addr = self.sock.recvfrom(65535)
        
        # sleep(0.0001)  # wait for reading
        return data

    def get_info(self):
        data = self.receive()
        debug_message = debugs.Debug_Msgs()
        debug_message.ParseFromString(data)
        return debug_message