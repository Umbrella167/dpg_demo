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
import Logger as logger
import log_pb2
import time
VISION_PORT = 23333 # Athena vision port
ROBOT_ID = 6
class VisionModule:
    def __init__(self, VISION_PORT=23333, SENDERIP = '0.0.0.0'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
        self.sock.bind((SENDERIP,VISION_PORT))
        self.robot_info = [0, 0, 0, 0, 0, 0]
        self.ball_info = [0, 0, 0, 0]
        # self.log_player = logger.LogPlayer("logs/Rec_2024-08-31_16-25-54-466643.log")
        # self.logger = logger.Logger()
    def receive(self):
        data, addr = self.sock.recvfrom(65535)
        # sleep(0.0001) # wait for reading
        return data

    def get_info(self):
        data = self.receive()
        # 记录收到的数据
        # self.logger.log(message_data=data,save_module="Chunking",size=500,energy_saving=True)
        package = detection.Vision_DetectionFrame()
        package.ParseFromString(data)
        vision_data.vision = package
        print(package)
        return package
    # def get_info(self):
    #     # data = self.receive()
    #     # 记录收到的数据
    #     data = self.log_player.get_next_message()
    #     print(data)
    #     time.sleep(0.030)
    #     package = detection.Vision_DetectionFrame()
        
    #     package.ParseFromString(data.message_data)
        
    #     vision_data.vision = package
    #     return package
    
    
    
    
    
    
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