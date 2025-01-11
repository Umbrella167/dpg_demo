import VISION.vision_data as vision
import threading
import pygfx as gfx
from wgpu.gui.auto import WgpuCanvas
import Object.Object as obj
from PyQt6.QtWidgets import QApplication
import sys
import numpy as np

import BASE.GlobalData as data
import vision_module
LOG = False
ACTION_IP = '127.0.0.1'
ACTION_PORT = 20011
protobuf_message = vision_module.VisionModule()

def get_debug_data():
    # while True:
    detection_dict = protobuf_message.get_detection_dict()
    ball_pos = list(detection_dict["ball"]["pos"])
    data.ball_data["pos"] = [ball_pos[0],ball_pos[1],data.ball_radius]
    data.car_data = detection_dict

    debug_dict = protobuf_message.get_debug_dict()
    data.debug_line = debug_dict["line"]
    data.debug_arc = debug_dict["arc"]
    data.debug_text = debug_dict["text"]



def thread_start():
    # 启动数据接收线程
    print("Thread Starting...")
    debug_data_thread = threading.Thread(target=lambda:get_debug_data(), daemon=True)
    get_debug_data.start()

    print("Thread Started Successfully")

def before_render_loop():

    # rotation = camera.world.rotation
    # position = camera.world.position
    # print(f"rotation: {rotation}, position: {position}")
    # vision.get_debug_data()
    dtcore.update()
    
def after_render_loop():
    get_debug_data()
    dtcore.debug_drawer.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建QApplication实例
    # 创建窗口
    # thread_start()
    dtcore = obj.DTCore(900,600)
    camera = gfx.PerspectiveCamera(70, 1)
    camera.world.z = 3000

    scene = dtcore.scene
    scene.add(camera)
    canvas = WgpuCanvas(max_fps=888)
    disp = gfx.Display(canvas)
    disp.stats = True 
    disp.before_render = before_render_loop
    disp.after_render = after_render_loop
    disp.show(scene)  # 显示场景

# import sys
# from PyQt6.QtWidgets import QApplication
# import threading
# import dearpygui.dearpygui as dpg
# import pygfx as gfx
# from wgpu.gui.auto import WgpuCanvas, run
# import Object.Object as obj
# import VISION.vision_data as vision
# def thread_start():
#     # 启动数据接收线程
#     print("Thread Starting...")
#     vision_thread = threading.Thread(target=lambda: vision.get_vision_data(), daemon=True)
#     debug_thread = threading.Thread(target=lambda: vision.get_debug_data(), daemon=True)
#     debug_thread.start()
#     vision_thread.start()
#     print("Thread Started Successfully")


# def start_dearpygui():
#     dpg.create_context()
#     with dpg.window(label="DearPyGui Window"):
#         dpg.add_text("Hello, world")
#         dpg.add_button(label="Button")
#     dpg.create_viewport(title='DearPyGui Window', width=600, height=400)
#     dpg.setup_dearpygui()
#     dpg.show_viewport()
#     dpg.start_dearpygui()
#     dpg.destroy_context()

# def start_pygfx():
#     app = QApplication(sys.argv)  # 创建QApplication实例
#     dtcore = obj.DTCore(900, 600)
#     scene = dtcore.scene
#     canvas = WgpuCanvas(max_fps=888)
#     disp = gfx.Display(canvas)
#     disp.stats = True
#     disp.before_render = lambda: dtcore.update()
#     disp.after_render = dtcore.debug_drawer.clear
#     disp.show(scene)
#     run()

# if __name__ == "__main__":
#     thread_start()
#     dpg_thread = threading.Thread(target=start_dearpygui)
#     pygfx_thread = threading.Thread(target=start_pygfx)

#     dpg_thread.start()
#     pygfx_thread.start()

#     dpg_thread.join()
#     pygfx_thread.join()