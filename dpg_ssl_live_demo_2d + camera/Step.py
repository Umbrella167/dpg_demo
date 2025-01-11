import numpy as np
import dearpygui.dearpygui as dpg
import UI.Theme as theme
import UI.Language.Language as language
import UI.Components as components
import UI.HotKey as hotkey
import BASE.CallBack as callback
import BASE.GlobalData as data
import BASE.Utils as utils
import VISION.vision_data as vision 
import threading
import VISION.Camera as camera
from BASE.GlobalData import PARAM as param 


def init_all(obj):
    print("Initializing...")
    # 初始化
    dpg.create_context()
    #相机初始化
    camera.init_creame()
    # 设置字体
    theme.set_font()
    # 当前语言
    label = components.label
    # 设置主题
    theme.set_theme("Dark")
    # 创建主窗口
    with dpg.window(tag = "main_window",label=label["main_window"],no_close=True,no_collapse=True):
        components.side_menu()
        components.config_window()
        # components.plot_window()
    # 注册热建
    with dpg.handler_registry():
        dpg.add_key_release_handler(callback=hotkey.on_key_release)
        dpg.add_mouse_drag_handler(button = dpg.mvMouseButton_Left,callback=lambda:callback.left_mouse_drag_callback(obj))
        dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Middle,callback=lambda:callback.middle_mouse_drag_callback())
        dpg.add_mouse_wheel_handler(callback=callback.mouse_wheel_handler)
        dpg.add_mouse_click_handler(callback=lambda:callback.mouse_click_callback(obj))
        dpg.add_mouse_move_handler(callback=callback.mouse_move_callback)
        dpg.set_viewport_resize_callback(callback= lambda: callback.window_resize_callback())
    param.canvs.scale_matrix = dpg.create_scale_matrix(param.canvs.scale)
    param.canvs.translation_matrix = dpg.create_translation_matrix([500,500])
    print("Initialization successful")

def thread_start(obj):
    # 接收数据线程
    print("Thread Starting...")
    vision_thread = threading.Thread(target=lambda:vision.get_vision_data(obj), daemon=True)
    debug_thread = threading.Thread(target=lambda:vision.get_debug_data(obj), daemon=True)
    camera_thread = threading.Thread(target=lambda:camera.get_frame(), daemon=True)
    camera_thread.start()
    debug_thread.start()
    vision_thread.start()
    print("Thread Started Successfully")

def dpg_start_setup():
    #初始化
    dpg.configure_app(docking=True, docking_space=True, init_file="dpg_layout.ini", load_init_file=True)
    dpg.create_viewport(title="LIVE SYSTEM", width=1920, height=1080)
    dpg.setup_dearpygui()
    dpg.set_primary_window("main_window", False)
    dpg.show_viewport()
    # # 纹理创建
    with dpg.texture_registry(show=False):
        texture_data = utils.get_texture_data(data.camera)
        dpg.add_raw_texture(data.camera.shape[1], data.camera.shape[0], texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)
        # dpg.add_raw_texture(800, 600, texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)
        
def update_param_data():
    param.mouse.pos_last = param.mouse.pos
    # 获取窗口大小
    width, height = dpg.get_item_rect_size("side_menu_right")
    param.canvs.width = width
    param.canvs.height = height
    # 获取鼠标信息
    x,y = dpg.get_drawing_mouse_pos()
    data.PARAM.mouse.ssl_pos = utils.mouse2ssl(x,y,param.canvs.translation_matrix,param.mouse.scale)
    data.PARAM.mouse.ssl_pos = data.PARAM.mouse.ssl_pos[0],-1*data.PARAM.mouse.ssl_pos[1]
    x_ssl,y_ssl = data.PARAM.mouse.ssl_pos
    # 设置画布宽高
    dpg.set_item_width("drawlist", width)
    dpg.set_item_height("drawlist", height - 20)
    param.mouse.pos = [x,y]
    # 组合变换矩阵
    param.canvs.transform = param.canvs.translation_matrix * param.canvs.scale_matrix
    # 绘制FPS 和 ssl坐标信息
    dpg.draw_text([width - 120, 10],  color=[255, 255, 255, 200], size=25,text="FPS：" + str(int(dpg.get_frame_rate())),parent="config")
    dpg.draw_text([10, 10],  color=[255, 255, 255, 200], size=25,text=f"({x_ssl} , {y_ssl})",parent="config")

# 主循环

def main(obj):
    while dpg.is_dearpygui_running():
        # #清空画布
        obj.clean_canvs()
        # # 更新一些全局参数
        update_param_data()
        # 绘制全部内容
        obj.draw_all()

        # 应用变换矩阵
        dpg.apply_transform("canvs", param.canvs.transform)
        # 渲染
        dpg.render_dearpygui_frame()
