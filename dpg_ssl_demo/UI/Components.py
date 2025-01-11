import dearpygui.dearpygui as dpg
import UI.Language.Language as language
import UI.Theme as theme
import BASE.CallBack as callback
import math
import numpy as np
import BASE.GlobalData as data
import collections
import BASE.Utils as utils
from typing import Dict, List


class Object:
    def __init__(self):
        # 定义常量
        self.DEQUE_MAX_LEN = 800
        self.teams = ["BLUE", "YELLOW"]
        self.num_cars = 16
        # 初始化 car_data 字典
        self.car_data = self.initialize_car_data()
        self.show_car_data = {}
        self.show_car_tag = []
        self.show_car_tag_last = {}
        self.layer_change = False
        self.layer_car_show_control = {}
        self.layer_show_debug_text = True
        self.layer_show_debug_line = True
        self.layer_show_debug_arc = True
        self.layer_final = ["field_layer", "car_layer", "ball_layer", "debug_layer"]
        self.color_transform = [
            [255, 255, 255, 255],
            [255, 0, 0, 255],
            [255, 165, 0, 255],
            [255, 255, 0, 255],
            [0, 255, 0, 255],
            [0, 255, 255, 255],
            [0, 0, 255, 255],
            [160, 32, 240, 255],
            [128, 128, 128, 255],
            [0, 0, 0, 255],
        ]
        self.ball_data = {
            "pos": [0, 0],
            "vel_x": 0,
            "vel_y": 0,
            "vel": 0,
            "valid": True,
        }
        self.ball_data_vel = collections.deque(maxlen=self.DEQUE_MAX_LEN)
        self.ball_data_time = collections.deque(maxlen=self.DEQUE_MAX_LEN)
        self.debug_text = []
        self.debug_line = []
        self.debug_arc = []

    def initialize_car_data(self):
        car_data = {}
        for team in self.teams:
            for i in range(self.num_cars):
                key = f"{team}_{i}"
                car_data[key] = {
                    "tag": key,
                    "pos": [0, 0],
                    "dir": 0,
                    "team": team,
                    "show": False,
                    "num": i,
                }
        return car_data

    def set_ball(self, pos, vel_x, vel_y, valid):
        vel = math.hypot(vel_x, vel_y)  # 使用hypot函数计算欧几里得距离
        self.ball_data.update(
            {"pos": pos, "vel_x": vel_x, "vel_y": vel_y, "vel": vel, "valid": valid}
        )
        self.ball_data_vel.append(vel)

    def set_car(self, tag, pos=None, dir=None, show=None):
        if pos is not None:
            self.car_data[tag]["pos"] = pos
        if dir is not None:
            self.car_data[tag]["dir"] = dir
        if show is not None:
            self.car_data[tag]["show"] = show

    def show_car(self):
        self.show_car_tag = []
        self.show_car_data = {}
        for car in self.car_data.values():
            if car["show"]:
                pos = car["pos"]
                dir = car["dir"]
                tag = car["tag"]
                color = [0, 0, 255, 255] if tag[0] == "B" else [255, 255, 0, 255]
                self.show_car_tag.append(tag)
                self.show_car_data[tag] = car
                if tag in self.layer_car_show_control:
                    self.draw_car(pos, data.PARAM.car.radius, dir, color, tag)
        if self.show_car_tag_last == self.show_car_tag:
            self.layer_change = False
        else:
            self.layer_change = True
        self.show_car_tag_last = self.show_car_tag

    def draw_ball(self):
        pos = self.ball_data["pos"]
        color = [255, 165, 0, 255]
        dpg.draw_circle(
            center=pos,
            radius=47 * data.PARAM.mouse.scale,
            parent="canvs",
            color=color,
            thickness=3,
            fill=color,
        )

    def draw_car(self, pos, radius, dir, color, tag):
        angle = dir * (180 / math.pi)
        start_angle = 45 + angle
        end_angle = 315 + angle
        # 将角度转换为弧度
        start_radians = np.radians(start_angle)
        end_radians = np.radians(end_angle)
        # 计算每个分段的角度
        angles = np.linspace(start_radians, end_radians, 30 + 1)
        # 计算弧线上的点
        x = pos[0] + radius * np.cos(angles)
        y = pos[1] - radius * np.sin(angles)
        # 将点转换为列表格式
        points = np.column_stack((x, y)).tolist()
        with dpg.draw_node(tag=tag, parent="canvs"):
            dpg.draw_polygon(points, color=color, fill=color, thickness=2)
            dpg.draw_text(
                text=self.car_data[tag]["num"],
                pos=np.array(pos) + (np.array([-147, -220])),
                size=200 * data.PARAM.mouse.scale,
            )
        # dpg.draw_arrow(p1=[x2,y2],p2 = pos, parent="canvs",size=15,thickness= 2.5,color=[0,255,255,80])

    def plot_line(data_x, data_y, height, width):
        with dpg.plot(height=height, width=width):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, tag="xaxis", no_tick_labels=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, tag="yaxis", no_tick_labels=True)
            ticks = [0, 1300, 2700, 4000, 5300, 6500, 8000]
            tick_labels = [
                (
                    [f"{x}", x, (255, 0, 0, 255)]
                    if x == 6500
                    else [f"{x}", x, (255, 255, 0, 255)]
                )
                for x in ticks
            ]
            dpg.set_axis_ticks(x_axis, tick_labels)
            dpg.set_axis_limits(y_axis, 0, 8000)
            dpg.add_line_series(
                data_x, data_y, parent="yaxis", tag="line_series", label="Ball Vel"
            )

    def draw_field(self):
        color = [255, 255, 255, 150]
        thickness = 20 * data.PARAM.mouse.scale
        x, y = data.PARAM.field.size
        x = x / 2
        y = y / 2
        dpg.draw_rectangle(
            pmax=[-x, y], pmin=[x, -y], parent="canvs", color=color, thickness=thickness
        )
        dpg.draw_line(
            p1=[0, y], p2=[0, -y], parent="canvs", color=color, thickness=thickness
        )
        dpg.draw_line(
            p1=[x, 0], p2=[-x, 0], parent="canvs", color=color, thickness=thickness
        )
        dpg.draw_circle(
            center=[0, 0],
            radius=500 * data.PARAM.mouse.scale,
            parent="canvs",
            color=color,
            thickness=thickness,
        )
        if x == 4500:
            dpg.draw_rectangle(
                pmax=[-4500, 1000],
                pmin=[-3500, -1000],
                parent="canvs",
                color=color,
                thickness=thickness,
            )
            dpg.draw_rectangle(
                pmax=[3500, 1000],
                pmin=[4500, -1000],
                parent="canvs",
                color=color,
                thickness=thickness,
            )

    # 清空画布
    def draw_debug(self):
        self.draw_text()
        self.draw_line()
        self.draw_arc()

    def clean_canvs(self):
        dpg.delete_item("canvs", children_only=True)
        dpg.delete_item("config", children_only=True)

    def draw_arc(self):
        if self.layer_show_debug_arc:
            with dpg.draw_node(tag="debug_arc_node", parent="canvs"):
                for arc in self.debug_arc:
                    # print(arc)
                    posx, posy = utils.middle_pos(arc[0], arc[1])
                    pos = [posx, -1 * posy]
                    radius = (
                        utils.calculate_distance(
                            [arc[0][0], -1 * arc[0][1]], [arc[1][0], -1 * arc[0][1]]
                        )
                        / 2
                    )
                    start_angle = arc[2]
                    end_angle = arc[3]
                    color = arc[4]
                    # 将角度转换为弧度
                    start_radians = np.radians(start_angle)
                    end_radians = np.radians(end_angle)
                    # 计算每个分段的角度
                    angles = np.linspace(start_radians, end_radians, 40)
                    # 计算弧线上的点
                    x = pos[0] + radius * np.cos(angles)
                    y = pos[1] - radius * np.sin(angles)
                    # 将点转换为列表格式
                    points = np.column_stack((x, y)).tolist()
                    dpg.draw_polygon(
                        points,
                        color=self.color_transform[color],
                        thickness=1 * data.PARAM.mouse.scale,
                    )

    def draw_line(self):
        if self.layer_show_debug_line:
            with dpg.draw_node(tag="debug_line_node", parent="canvs"):
                for line in self.debug_line:
                    dpg.draw_line(
                        p1=line[0], p2=line[1], color=self.color_transform[line[2]]
                    )

    def draw_text(self):
        if self.layer_show_debug_text:
            with dpg.draw_node(tag="debug_text_node", parent="canvs"):
                for text in self.debug_text:
                    dpg.draw_text(
                        pos=text[0],
                        text=text[1],
                        size=text[2] * data.PARAM.mouse.scale * 1.5,
                        color=self.color_transform[text[3]],
                    )

    def draw_all(self):
        for layer in self.layer_final:
            if layer == "ball_layer":
                obj.draw_ball()
            if layer == "car_layer":
                obj.show_car()
            if layer == "field_layer":
                obj.draw_field()
            if layer == "debug_layer":
                obj.draw_debug()


def config_window():
    with dpg.window(tag="PARAM", label="PARAM"):
        with dpg.tab_bar():
            with dpg.tab(label="Layer", tag="layer_tab"):
                dpg.add_text("", tag="dragged_item", show=False)
                with dpg.group(tag="debug_layer_father"):
                    with dpg.collapsing_header(
                        label="Debug",
                        tag="debug_layer",
                        show=True,
                        payload_type="Layer",
                        drop_callback=callback.layer_drop,
                        drag_callback=callback.layer_get_drag_item,
                    ):
                        with dpg.drag_payload(
                            parent=dpg.last_item(), payload_type="Layer"
                        ):
                            dpg.add_text("Debug")
                with dpg.group(tag="ball_layer_father"):
                    with dpg.collapsing_header(
                        label="Ball",
                        tag="ball_layer",
                        show=True,
                        payload_type="Layer",
                        drop_callback=callback.layer_drop,
                        drag_callback=callback.layer_get_drag_item,
                    ):
                        with dpg.drag_payload(
                            parent=dpg.last_item(), payload_type="Layer"
                        ):
                            dpg.add_text("Ball")
                with dpg.group(tag="car_layer_father"):
                    with dpg.collapsing_header(
                        label="Car",
                        tag="car_layer",
                        show=False,
                        payload_type="Layer",
                        drop_callback=callback.layer_drop,
                        drag_callback=callback.layer_get_drag_item,
                    ):
                        with dpg.drag_payload(
                            parent=dpg.last_item(), payload_type="Layer"
                        ):
                            dpg.add_text("Car")

                with dpg.group(tag="field_layer_father"):
                    with dpg.collapsing_header(
                        label="Field",
                        tag="field_layer",
                        show=True,
                        payload_type="Layer",
                        drop_callback=callback.layer_drop,
                        drag_callback=callback.layer_get_drag_item,
                    ):
                        with dpg.drag_payload(
                            parent=dpg.last_item(), payload_type="Layer"
                        ):
                            dpg.add_text("Field")

            with dpg.tab(label="Config"):
                with dpg.collapsing_header(label="Field"):
                    dpg.add_text("Field Size：")
                    dpg.add_listbox(
                        items=["6 * 4", "9 * 6", "12 * 9"],
                        default_value="9 * 6",
                        tag="port_list",
                        width=-1,
                        callback=callback.set_field_size,
                    )
        # 边菜单


def side_menu():
    # 右主内容
    with dpg.child_window(
        tag="side_menu_right",
        width=-1,
        height=-1,
        pos=(10, 15),
        show=True,
        drop_callback=callback.add_plot_time_shape,
        payload_type="Drag&Drop",
    ):
        draw_window()


def plot_window():
    with dpg.window(tag="PLOT", label="PLOT"):
        Object.plot_line([], [], -1, -1)


# 画布
def draw_window():
    width, height, channels, data = dpg.load_image("./UI/Image/rocos.png")
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="background_image_texture")
    with dpg.drawlist(width=0, height=0, tag="drawlist"):
        with dpg.draw_node(tag="bg"):
            dpg.draw_image("background_image_texture", [0, 0], [width, height])
        with dpg.draw_node(tag="config"):
            dpg.draw_text(
                [10, 10],
                color=[255, 255, 255, 255],
                size=40,
                tag="fps",
                text="Hello, world!",
            )
        with dpg.draw_node(tag="canvs"):
            pass


def show_layer(obj):
    if obj.show_car_data:
        dpg.configure_item("car_layer", show=True)
    else:
        dpg.configure_item("car_layer", show=False)
    if obj.layer_change:
        dpg.delete_item("car_layer", children_only=True)
        obj.layer_car_show_control = obj.show_car_tag
        with dpg.drag_payload(parent="car_layer", payload_type="Layer"):
            dpg.add_text("Ball")
        for i in obj.show_car_tag:
            dpg.add_checkbox(
                label=i,
                parent="car_layer",
                default_value=True,
                tag="layer_" + i,
                callback=callback.layer_car_checkbox,
                user_data=obj,
            )

    debug_text_valid = True if dpg.does_item_exist("layer_debug_text") else False
    debug_line_valid = True if dpg.does_item_exist("layer_debug_line") else False
    debug_arc_valid = True if dpg.does_item_exist("layer_debug_arc") else False

    if obj.debug_text:
        if not debug_text_valid:
            dpg.add_checkbox(
                label="Message",
                parent="debug_layer",
                default_value=True,
                tag="layer_debug_text",
                callback=callback.layer_debug_text_checkbox,
                user_data=obj,
            )
    else:
        if debug_text_valid:
            dpg.delete_item("layer_debug_text")
    if obj.debug_line:
        if not debug_line_valid:
            dpg.add_checkbox(
                label="Line and Point",
                parent="debug_layer",
                default_value=True,
                tag="layer_debug_line",
                callback=callback.layer_debug_line_checkbox,
                user_data=obj,
            )
    else:
        if debug_line_valid:
            dpg.delete_item("layer_debug_line")

    if obj.debug_arc:
        if not debug_arc_valid:
            dpg.add_checkbox(
                label="Arc",
                parent="debug_layer",
                default_value=True,
                tag="layer_debug_arc",
                callback=callback.layer_debug_arc_checkbox,
                user_data=obj,
            )
    else:
        if debug_arc_valid:
            dpg.delete_item("layer_debug_arc")


def console_window():
    with dpg.child_window(label="T_console_window", tag="console_window"):
        dpg.add_text("Console:")
        dpg.add_input_text(multiline=True, width=-1, height=-1)


label = language.languages[theme.current_language]
obj = Object()
