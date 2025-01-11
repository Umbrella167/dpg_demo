import dearpygui.dearpygui as dpg
import BASE.GlobalData as data
from BASE.GlobalData import PARAM as param
import numpy as np
import BASE.Utils as utils
import math
import UI.Components as components
import VISION.Camera as camera
import cv2
# 保存页面布局
def save_callback(sender, app_data, user_data):
    dpg.save_init_file("dpg_layout.ini")

# 左键拖动事件
def left_mouse_drag_callback(obj):
    click_name = data.PARAM.mouse.click_obj
    if data.PARAM.mouse.click_obj == "canvs":
        pass
    else:

        data.PARAM.field.p[int(click_name[-1])] = data.PARAM.mouse.ssl_pos

# 中键拖动事件
def middle_mouse_drag_callback():
    pass
def mouse_move_callback():
    # dpg.is_key_pressed
    if dpg.is_mouse_button_down(dpg.mvMouseButton_Middle):
        click_name = data.PARAM.mouse.click_obj
        center_x = param.canvs.width / 2
        center_y = param.canvs.height / 2
        translation_x ,translation_y,_ = param.canvs.translation
        move_x = param.mouse.pos[0] - param.mouse.pos_last[0] 
        move_y = param.mouse.pos[1] - param.mouse.pos_last[1]
        move_x,move_y = [move_x,move_y]

        if data.PARAM.mouse.click_obj == "canvs":
            # if param.mouse.pos == [mouse_x,mouse_y]:
            param.canvs.translation = [translation_x+move_x, translation_y+move_y, 0]
            param.canvs.translation_matrix = dpg.create_translation_matrix(param.canvs.translation)
        else:
            pass

def window_resize_callback():
    param.canvs.translation = [param.canvs.width /2,param.canvs.height /2,0]
    param.canvs.translation_matrix = dpg.create_translation_matrix(param.canvs.translation)

def mouse_click_callback(obj):
    param.mouse.click_pos = param.mouse.pos
    utils.get_close_mouse_car(obj)

def add_plot_time_shape():
    dpg.add_plot(label="Time Shape", parent="viewport_group")
def mouse_drag_callback():
    pass

def set_field_size(sender, app_data, user_data):
    w = int(app_data[0:2]) * 1000
    h = int(app_data[-1]) * 1000
    param.field.width = w
    param.field.height = h
    param.field.size = [w,h]

def mouse_wheel_handler(sender, app_data):
    mouse_x, mouse_y = dpg.get_mouse_pos()
    use_draw_pos =  not (abs(mouse_y) < 10000 and abs(mouse_x) < 10000)
    if use_draw_pos:
        mouse_x, mouse_y = dpg.get_drawing_mouse_pos()
    dpg.focus_item("canvs")
    if mouse_x < param.canvs.width and mouse_y < param.canvs.height:
        # 计算当前鼠标在世界坐标系中的位置
        world_mouse_x = (mouse_x - param.canvs.translation[0]) / data.PARAM.mouse.scale
        world_mouse_y = (mouse_y - param.canvs.translation[1]) / data.PARAM.mouse.scale
        # 根据滚轮值调整缩放比例
        if data.PARAM.mouse.scale >= 0.3:
            step = 0.15
        else:
            step = 0.05
        if app_data > 0:
            data.PARAM.mouse.scale += step
        else:
            data.PARAM.mouse.scale -= step
        data.PARAM.mouse.scale = max(0.03, data.PARAM.mouse.scale)
        data.PARAM.mouse.scale = min(5.2, data.PARAM.mouse.scale)
        param.canvs.scales = [data.PARAM.mouse.scale, data.PARAM.mouse.scale, 1]
        param.canvs.scale_matrix = dpg.create_scale_matrix(param.canvs.scales)
        # 计算新的平移量，以使缩放后的鼠标位置与缩放前相同
        new_translation_x = mouse_x - world_mouse_x * param.canvs.scales[0]
        new_translation_y = mouse_y - world_mouse_y * param.canvs.scales[1]
        param.canvs.translation = [new_translation_x, new_translation_y, 0]
        param.canvs.translation_matrix = dpg.create_translation_matrix(param.canvs.translation)

def window_resize_handler():
    pass

def layer_car_checkbox(sender,app_data,user_data):
    car_tag = sender[6:]
    obj = user_data
    if app_data:
        obj.layer_car_show_control.append(car_tag)
    else:
        obj.layer_car_show_control.remove(car_tag)

def layer_debug_text_checkbox(sender,app_data,user_data):
    obj = user_data
    if app_data:
        obj.layer_show_debug_text = True
    else:
        obj.layer_show_debug_text = False

def layer_debug_line_checkbox(sender,app_data,user_data):
    obj = user_data
    if app_data:
        obj.layer_show_debug_line = True
    else:
        obj.layer_show_debug_line = False

def layer_debug_arc_checkbox(sender,app_data,user_data):
    obj = user_data
    if app_data:
        obj.layer_show_debug_arc = True
    else:
        obj.layer_show_debug_arc = False



def layer_drop(sender, app_data, user_data):
    swap_item = dpg.get_value("dragged_item")
    swap_items(sender,swap_item)

def layer_get_drag_item(sender):
    dpg.set_value(item="dragged_item",value=sender)
# 交换两个项目的位置
def swap_items(item1, item2):
    parent1 = dpg.get_item_parent(item1)
    parent2 = dpg.get_item_parent(item2)
    dpg.move_item(item=item1,parent=parent2)
    dpg.move_item(item=item2,parent=parent1)
    utils.swap_elements(components.obj.layer_final,item1,item2)
    print(components.obj.layer_final)

def change_Gain_value(sender, app_data, user_data):
    dpg.set_value("Gain_slider_input",app_data)
    dpg.set_value("Gain_input",app_data)
    camera.set_gain(app_data)
def change_ExposureTime_value(sender, app_data, user_data):
    dpg.set_value("ExposureTime_slider_input",app_data)
    dpg.set_value("ExposureTime_input",app_data)
    camera.set_exposuretime(app_data)