import VISION.vision_data as vision
import threading
import pygfx as gfx
from wgpu.gui.auto import WgpuCanvas
import Object.Object as obj
from PyQt6.QtWidgets import QApplication
import sys
import numpy as np
from pygfx.controllers import FlyController
import BASE.GlobalData as data
def thread_start():
    # 启动数据接收线程
    print("Thread Starting...")
    vision_thread = threading.Thread(target=lambda: vision.get_vision_data(), daemon=True)
    debug_thread = threading.Thread(target=lambda: vision.get_debug_data(), daemon=True)
    debug_thread.start()
    vision_thread.start()

    print("Thread Started Successfully")

def before_render_loop():

    ball_pos = dtcore.ball.local.position
    ball_x = ball_pos[0]
    ball_y = ball_pos[1]
    error_x =  ball_x - camera.local.x
    error_y =  (-2000 + ball_y) - camera.local.y 

    if abs(error_x) > 100 and abs(error_x) < 500:
        # tag = ball_pos - camera.world.position
        # tag[0] = 0
        # camera.world.forward = tag
        camera.local.x += error_x / 80
    elif abs(error_x) > 500:
        # tag = ball_pos - camera.world.position
        # tag[0] = 0
        # camera.world.forward = tag
        camera.local.x += error_x / 20


    if abs(error_y) > 100 and abs(error_y) < 500:
        camera.local.y += error_y / 80
        # tag = ball_pos - camera.world.position
        # tag[0] = 0
        # camera.world.forward = tag
    elif abs(error_y) > 500:
        camera.local.y += error_y / 20
        # tag = ball_pos - camera.world.position
        # tag[0] = 0
        # camera.world.forward = tag
    # tag = ball_pos - camera.world.position
    # tag[0] = 0
    # camera.world.forward = tag
    # print(tag)
    dtcore.update()
    
def after_render_loop():
    dtcore.debug_drawer.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建QApplication实例
    # 创建窗口
    thread_start()
    dtcore = obj.DTCore(800,600)
    camera = gfx.PerspectiveCamera(70, 1)
    camera.world.position = [0,-2000,2000]

    scene = dtcore.scene
    scene.add(camera)
    canvas = WgpuCanvas(size=(1920, 1080), max_fps=888)
    disp = gfx.Display(canvas)
    disp.stats = True 
    disp.before_render = before_render_loop
    disp.after_render = after_render_loop
    disp.show(scene)  # 显示场景
