# -*- coding: utf-8 -*-
"""
@Brief: This is a test run script
@Version: Test Run 2.0.0
@author: Wang Yunkai
"""
import numpy as np
import VISION.visionmodule
import UI.Components as components
import BASE.GlobalData as data
import VISION.zss_debug_pb2 as debugs
LOG = False
ACTION_IP = '127.0.0.1'
ACTION_PORT = 20011
ROBOT_ID = 1

def get_debug_data(obj):
    visions = VISION.visionmodule
    debug = visions.DEBUG(20001)
    
    while True:
        debug_info=debug.get_info()
        
        texts = []
        lines = []
        arcs = []
        for msg in debug_info.msgs:
            # print(f"Type: {msg.type}, Color: {msg.color}")
            if msg.type == debugs.Debug_Msg.LINE:
                # obj.draw_line([float(msg.line.start.x),float(msg.line.start.y)],[float(msg.line.end.x),float(msg.line.end.y)],msg.color)
                # print(f"Line Start: ({msg.line.start}), End: ({msg.line.end})")
                lines.append([[msg.line.start.x,-1 * msg.line.start.y],[msg.line.end.x,-1 * msg.line.end.y],msg.color])
                pass
            elif msg.type == debugs.Debug_Msg.ARC:
                # print(f"Arc Rectangle: ({msg.arc.rect.point1.x}, {msg.arc.rect.point1.y}) to ({msg.arc.rect.point2.x}, {msg.arc.rect.point2.y}), Start Angle: {msg.arc.start}, Span: {msg.arc.span}")
                arcs.append([[msg.arc.rect.point1.x,msg.arc.rect.point1.y],[msg.arc.rect.point2.x,msg.arc.rect.point2.y],msg.arc.start,msg.arc.span,msg.color])
                pass
            elif msg.type == debugs.Debug_Msg.POLYGON:
                # print("Polygon Vertices:")
                # for vertex in msg.polygon.vertex:
                    # print(f"({vertex.x}, {vertex.y})")
                pass
            elif msg.type == debugs.Debug_Msg.TEXT:
                # print(f"Text Position: ({msg.text.pos.x}, {msg.text.pos.y}), Text: {msg.text.text}, Size: {msg.text.size}, Weight: {msg.text.weight}")
                texts.append([[msg.text.pos.x,-1 * (msg.text.pos.y + 160)],msg.text.text,msg.text.size,msg.color])
                pass

            elif msg.type == debugs.Debug_Msg.POINTS:
                # print("Points:")
                # for point in msg.points.point:
                #     print(f"({point.x}, {point.y})")
                pass
            # print(f"RGB Value: {msg.RGB_value}")
        obj.debug_text = texts
        obj.debug_line = lines
        obj.debug_arc = arcs

def get_vision_data(obj):
    VISION_PORT = 41001
    visions = VISION.visionmodule
    vision = visions.VisionModule(VISION_PORT)
    # log_player = logger.LogPlayer("logs/Rec_2024-08-31_16-12-17-642219.log")
    while True:
        packge = vision.get_info()
        robots_blue = packge.robots_blue
        robots_yellow = packge.robots_yellow
        ball = packge.balls
        pos = [ball.x, -ball.y]
        obj.set_ball(pos, ball.vel_x, ball.vel_y, ball.valid)
        obj.ball_data_time.append(data.time.total_time)

        show_set = set()

        for robot_yellow in robots_yellow:
            id_yellow = robot_yellow.robot_id
            pos_yellow = [robot_yellow.x, -robot_yellow.y]
            dir_yellow = robot_yellow.orientation
            tag_yellow = f"YELLOW_{id_yellow}"
            show_set.add(tag_yellow)
            obj.set_car(tag_yellow, pos=pos_yellow, dir=dir_yellow, show=True)

        for robot_blue in robots_blue:
            id_blue = robot_blue.robot_id
            pos_blue = [robot_blue.x, -robot_blue.y]
            dir_blue = robot_blue.orientation
            tag_blue = f"BLUE_{id_blue}"
            show_set.add(tag_blue)
            obj.set_car(tag_blue, pos=pos_blue, dir=dir_blue, show=True)
        for key, car_show in obj.car_data.items():
            if car_show['tag'] not in show_set:
                car_show['show'] = False