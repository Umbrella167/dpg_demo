# -*- coding: utf-8 -*-
"""
@Brief: This is a test run script
@Version: Test Run 2.0.0
@author: Wang Yunkai
"""
import BASE.GlobalData as data
import vision_module
LOG = False
ACTION_IP = '127.0.0.1'
ACTION_PORT = 20011
protobuf_message = vision_module.VisionModule()

def get_debug_data():
    detection_dict = protobuf_message.get_detection_dict()
    ball_pos = list(detection_dict["ball"]["pos"])
    data.ball_data["pos"] = [ball_pos[0],ball_pos[1],data.ball_radius]
    data.car_data = detection_dict

    debug_dict = protobuf_message.get_debug_dict()
    data.debug_line = debug_dict["line"]
    data.debug_arc = debug_dict["arc"]
    data.debug_text = debug_dict["text"]