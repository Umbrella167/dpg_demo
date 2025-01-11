# -*- coding: utf-8 -*-
"""
@Brief: This is a test run script
@Version: Test Run 2.0.0
@author: Wang Yunkai
"""
import VISION.visionmodule
import BASE.GlobalData as data
import VISION.zss_debug_pb2 as debugs
LOG = False

ACTION_IP = '127.0.0.1'
ACTION_PORT = 20011
ROBOT_ID = 1

def get_debug_data(func,item):
    visions = VISION.visionmodule
    debug = visions.DEBUG(20001)
    FLAG = func(item)

    while FLAG:
        FLAG = func(item)
        debug_info=debug.get_info()
        texts = []
        lines = []
        arcs = []
        for msg in debug_info.msgs:
            if msg.type == debugs.Debug_Msg.LINE:
                lines.append([[msg.line.start.x, -1*msg.line.start.y],[msg.line.end.x, -1*msg.line.end.y],msg.color])
                pass
            elif msg.type == debugs.Debug_Msg.ARC:
                arcs.append([[[msg.arc.rect.point1.x,-1*msg.arc.rect.point1.y],[msg.arc.rect.point2.x,-1*msg.arc.rect.point2.y]],msg.arc.start,msg.arc.span,msg.color])

                pass
            elif msg.type == debugs.Debug_Msg.TEXT:
                texts.append([[msg.text.pos.x, -1*(msg.text.pos.y + 160)],msg.text.text,msg.text.size,msg.color]   )
                pass
        data.debug_line = lines
        data.debug_arc = arcs
        data.debug_text = texts
def get_vision_data(func,item):
    VISION_PORT = 41001
    visions = VISION.visionmodule
    vision = visions.VisionModule(VISION_PORT)
    FLAG = True
    while FLAG:
        FLAG = func(item)
        packge = vision.get_info(ROBOT_ID)
        robots_blue = packge.robots_blue
        robots_yellow = packge.robots_yellow
        ball = packge.balls
        data.ball_data["pos"] = [ball.x, ball.y,data.ball_radius]
        car_live = {}
        for robot_yellow in robots_yellow:
            id_yellow = robot_yellow.robot_id
            pos_yellow = [robot_yellow.x, robot_yellow.y]
            dir_yellow = -1*robot_yellow.orientation
            tag_yellow = f"YELLOW_{id_yellow}"
            car_live[tag_yellow] = {
                "pos" : pos_yellow,
                "dir" : dir_yellow,
                "color":"YELLOW"
            }
        for robot_blue in robots_blue:
            id_blue = robot_blue.robot_id
            pos_blue = [robot_blue.x, robot_blue.y] 
            dir_blue = -1*robot_blue.orientation
            tag_blue = f"BLUE_{id_blue}"
            car_live[tag_blue] = {
                "pos" : pos_blue,
                "dir" : dir_blue,
                "color":"BLUE"
            }
        data.car_data = car_live
