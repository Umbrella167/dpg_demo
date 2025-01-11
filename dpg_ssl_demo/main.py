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

from BASE.GlobalData import PARAM as param 
# 初始化
dpg.create_context()
config = data.ConfigData
obj = components.obj

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
    components.plot_window()

with dpg.handler_registry():
    dpg.add_key_release_handler(callback=hotkey.on_key_release)
    dpg.add_mouse_drag_handler(button = dpg.mvMouseButton_Left,callback=lambda:callback.left_mouse_drag_callback(obj))
    dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Middle,callback=lambda:callback.middle_mouse_drag_callback())
    dpg.add_mouse_wheel_handler(callback=callback.mouse_wheel_handler)
    dpg.add_mouse_click_handler(callback=lambda:callback.mouse_click_callback(obj))
    dpg.add_mouse_move_handler(callback=callback.mouse_move_callback)
    dpg.set_viewport_resize_callback(callback= lambda: callback.window_resize_callback())

# width, height = dpg.get_item_rect_size("side_menu_right")
# param.canvs.translation = [width,height,0]
vision_thread = threading.Thread(target=lambda:vision.get_vision_data(obj), daemon=True)
debug_thread = threading.Thread(target=lambda:vision.get_debug_data(obj), daemon=True)
debug_thread.start()
vision_thread.start()
dpg.configure_app(docking=True, docking_space=True, init_file="dpg_layout.ini", load_init_file=True)
dpg.create_viewport(title=label["main_window"], width=1920, height=1080)
dpg.setup_dearpygui()
dpg.set_primary_window("main_window", False)
dpg.show_viewport()
dir = 0


param.canvs.scale_matrix = dpg.create_scale_matrix(param.canvs.scale)
param.canvs.translation_matrix = dpg.create_translation_matrix([500,500])
# 主循环
while dpg.is_dearpygui_running():
    param.mouse.pos_last = param.mouse.pos
    # 获取窗口大小
    width, height = dpg.get_item_rect_size("side_menu_right")
    param.canvs.width = width
    param.canvs.height = height
    obj.clean_canvs()
    components.show_layer(obj)
    dpg.set_value("line_series",[list(obj.ball_data_time),list(obj.ball_data_vel)])
    dpg.fit_axis_data("xaxis")
    
    
    utils.get_fps()
    dpg.draw_text([width - 120, 10],  color=[255, 255, 255, 200], size=25,text="FPS：" + str(int(dpg.get_frame_rate())),parent="config")
    dpg.set_item_width("drawlist", width)
    dpg.set_item_height("drawlist", height - 20)
    x,y = dpg.get_drawing_mouse_pos()
    x_ssl,y_ssl = utils.mouse2ssl(x,y,param.canvs.translation_matrix,param.mouse.scale)
    dpg.draw_text([10, 10],  color=[255, 255, 255, 200], size=25,text="(" + str(x_ssl) + ", " + str(y_ssl) + ")",parent="config")
    param.mouse.pos = [x,y]
    param.canvs.transform = param.canvs.translation_matrix * param.canvs.scale_matrix
    dpg.apply_transform("canvs", param.canvs.transform)
    obj.draw_all()
    dpg.render_dearpygui_frame()
    
dpg.destroy_context()
