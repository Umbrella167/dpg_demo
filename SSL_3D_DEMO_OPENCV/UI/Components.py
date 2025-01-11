import UI.Language.Language as language
import UI.Theme as theme
import BASE.CallBack as callback
import math
import numpy as np
import BASE.GlobalData as data
import collections
import BASE.Utils as utils
import VISION.Camera as camera
import cv2

class Object2D():
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
        self.layer_final = ["field_layer","car_layer","ball_layer","debug_layer"]
        self.color_transform = [[255, 255, 255,255],[255, 0, 0,255],[255, 165, 0,255],[255, 255, 0,255],[0, 255, 0,255],[0, 255, 255,255],[0, 0, 255,255],[160, 32, 240,255],[128, 128, 128,255],[0, 0, 0,255]]
        self.ball_data={
            "pos":[0,0],
            "vel_x":0,
            "vel_y":0,
            "vel":0,
            "valid":True
            }
        self.ball_data_vel = collections.deque(maxlen=self.DEQUE_MAX_LEN)
        self.ball_data_time = collections.deque(maxlen=self.DEQUE_MAX_LEN)
        self.debug_text = []
        self.debug_line = []
        self.debug_arc = []

        self.height = 600
        self.width = 400
        self.canvas_data = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        self.canvas_data[:] = [0, 100, 0]
        self.canvas = self.canvas_data.copy()
    def initialize_car_data(self):
        car_data = {}
        for team in self.teams:
            for i in range(self.num_cars):
                key = f"{team}_{i}"
                car_data[key] = {
                    "tag"  : key,
                    "pos"  : [0, 0],
                    "dir"  : 0,
                    "team" : team,
                    "show" : False,
                    "num"  : i
                }
        return car_data

    def set_ball(self, pos, vel_x, vel_y, valid):
        vel = math.hypot(vel_x, vel_y)  # 使用hypot函数计算欧几里得距离
        self.ball_data.update({
            "pos": pos,
            "vel_x": vel_x,
            "vel_y": vel_y,
            "vel": vel,
            "valid": valid
        })
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
                color = [0, 0, 255,255] if tag[0] == "B" else [255, 255, 0,255]
                self.show_car_tag.append(tag)
                self.show_car_data[tag] = car
                # if tag in self.layer_car_show_control:
                self.draw_car(pos,data.PARAM.car.radius,dir,color,tag)
        if self.show_car_tag_last == self.show_car_tag:
            self.layer_change = False
        else:
            self.layer_change = True
        # data.car_data = self.show_car_data
        self.show_car_tag_last = self.show_car_tag
    def draw_circle_P(self,center, radius, color, thickness,parent,fill=None,perspective = True):
        start_angle = 0
        end_angle = 360
        # 将角度转换为弧度
        start_radians = np.radians(start_angle)
        end_radians = np.radians(end_angle)
        # 计算每个分段的角度
        angles = np.linspace(start_radians, end_radians, 30)
        # 计算弧线上的点
        x = center[0] + radius * np.cos(angles)
        y = center[1] - radius * np.sin(angles)
        # 将点转换为列表格式
        points = np.column_stack((x, y)).tolist()
        if perspective:
            points = camera.perspective_transform_s(points)
        points = np.array(points, dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        color = color[2::-1] + color[3:]
        cv2.polylines(self.canvas,[points],True,color,1)
        # cv2.fillPoly(self.canvas,[points],color)

        # dpg.draw_polygon(points, color=color, thickness=thickness,parent=parent,fill=fill)
        # dpg.draw_arrow(p1=[x2,y2],p2 = pos, parent="canvas",size=15,thickness= 2.5,color=[0,255,255,80])
    def draw_ball(self):
        pos = self.ball_data["pos"]
        # color = [255,165,0,255]
        color = [0,165,255,255]
        self.draw_circle_P(center=pos,radius=47 * data.PARAM.mouse.scale*3,parent="canvas",color = color,thickness = 2,fill=color)
    def draw_car(self,pos, radius, dir,  color, tag):
        angle =  dir * (180 / math.pi)
        start_angle = 45 + angle
        end_angle = 315 + angle
        # 将角度转换为弧度
        start_radians = np.radians(start_angle)
        end_radians = np.radians(end_angle)
        # 计算每个分段的角度
        angles = np.linspace(start_radians, end_radians, 30)

        # 计算弧线上的点
        x = pos[0] + radius * np.cos(angles)
        y = pos[1] - radius * np.sin(angles)
        
        # 将点转换为列表格式
        points = np.column_stack((x, y)).tolist()

        points = camera.perspective_transform_s(points)
        points = np.array(points, dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        # color = color[2::-1] + color[3:]
        cv2.polylines(self.canvas,points,True,color)
        # dpg.draw_arrow(p1=[x2,y2],p2 = pos, parent="canvas",size=15,thickness= 2.5,color=[0,255,255,80])

    def plot_line(data_x,data_y,height,width):
        with dpg.plot(height=height, width=width):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis,tag="xaxis",no_tick_labels=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis,tag = "yaxis",no_tick_labels=True)
            ticks = [0, 1300, 2700, 4000, 5300, 6500, 8000]
            tick_labels = [[f"{x}", x, (255, 0, 0, 255)] if x == 6500 else [f"{x}", x, (255, 255, 0, 255)] for x in ticks]
            dpg.set_axis_ticks(x_axis, tick_labels)
            dpg.set_axis_limits(y_axis, 0, 8000)
            dpg.add_line_series(data_x, data_y, parent="yaxis",tag="line_series",label="Ball Vel")
    def draw_field(self):
        color = [0,255,0,100]
        thickness = 10 * data.PARAM.mouse.scale
        p0 = data.PARAM.field.p[0]
        p1 = data.PARAM.field.p[1]
        p2 = data.PARAM.field.p[2]
        p3 = data.PARAM.field.p[3]
        dpg.draw_line(p1=p0,p2=p1,parent="canvas",color = color,thickness = thickness)
        dpg.draw_line(p1=p0,p2=p3,parent="canvas",color = color,thickness = thickness)
        dpg.draw_line(p1=p1,p2=p2,parent="canvas",color = color,thickness = thickness)
        dpg.draw_line(p1=p2,p2=p3,parent="canvas",color = color,thickness = thickness)

        dpg.draw_line(p1=camera.perspective_transform([-4500,0]),p2=camera.perspective_transform([4500,0]),parent="canvas",color = color,thickness = thickness)

        dpg.draw_line(p1=camera.perspective_transform([0,3000]),p2=camera.perspective_transform([0,-3000]),parent="canvas",color = color,thickness = thickness)
        
        self.draw_circle_P(center=[0,0],radius=500,parent="canvas",color = color,thickness = thickness,perspective =True)

        dpg.draw_line(p1=camera.perspective_transform([-4500,1000]),p2=camera.perspective_transform([-3500,1000]),parent="canvas",color = color,thickness = thickness)
        dpg.draw_line(p1=camera.perspective_transform([-3500,1000]),p2=camera.perspective_transform([-3500,-1000]),parent="canvas",color = color,thickness = thickness)
        dpg.draw_line(p1=camera.perspective_transform([-3500,-1000]),p2=camera.perspective_transform([-4500,-1000]),parent="canvas",color = color,thickness = thickness)

        dpg.draw_line(p1=camera.perspective_transform([4500,1000]),p2=camera.perspective_transform([3500,1000]),parent="canvas",color = color,thickness = thickness)
        dpg.draw_line(p1=camera.perspective_transform([3500,1000]),p2=camera.perspective_transform([3500,-1000]),parent="canvas",color = color,thickness = thickness)
        dpg.draw_line(p1=camera.perspective_transform([3500,-1000]),p2=camera.perspective_transform([4500,-1000]),parent="canvas",color = color,thickness = thickness)
    #清空画布
    def draw_debug(self):
        # self.draw_text()
        self.draw_line()
        self.draw_arc()
    def clean_canvas(self):
        self.canvas = self.canvas_data.copy()
    def draw_arc(self):
        if self.layer_show_debug_arc:
            for arc in self.debug_arc:
                # print(arc)
                posx,posy = utils.middle_pos(arc[0],arc[1])
                pos = [posx,-1*posy]
                radius = utils.calculate_distance([arc[0][0],-1*arc[0][1]],[arc[1][0],-1*arc[0][1]]) / 2
                start_angle = arc[2]
                end_angle =  arc[3]
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
                points = camera.perspective_transform_s(points)
                # dpg.draw_polygon(points, color=self.color_transform[color], thickness=1 * data.PARAM.mouse.scale)
                points = np.array(points, dtype=np.int32)
                points = points.reshape((-1, 1, 2))
                cv2.polylines(self.canvas,points,True,self.color_transform[color],2)
    def draw_line(self):
        if self.layer_show_debug_line and self.debug_line:
            data_len = len(self.debug_line)
            points = np.array([point for sublist in self.debug_line for point in sublist[:2]])
            debug_line = camera.perspective_transform_s(points)
            for i in range(0, data_len, 2):
                if i // 2 < data_len:
                    line = self.debug_line[i // 2]
                    # dpg.draw_line(p1=debug_line[i], p2=debug_line[i+1], color=self.color_transform[line[2]])
                    color = self.color_transform[line[2]]
                    # color = color[2::-1] + color[3:]
                    cv2.line(self.canvas, tuple((int(debug_line[i][0]),int(debug_line[i][1]))),tuple((int(debug_line[i+1][0]),int(debug_line[i+1][1]))), color, 2) 

    def draw_text(self):
        if self.layer_show_debug_text:
            with dpg.draw_node(tag="debug_text_node",parent="canvas"):
                for text in self.debug_text:
                    p1 = camera.perspective_transform(text[0])
                    dpg.draw_text(pos=p1,text=text[1],size=text[2] * data.PARAM.mouse.scale * 0.8,color=self.color_transform[text[3]])
    def draw_camera(self):
            # 获取相机数据
            texture_data = utils.get_texture_data(data.camera)
            dpg.set_value("texture_tag",texture_data)
            dpg.draw_image("texture_tag",[-4500,-3000],[4500,3000],parent="canvas")
    def draw_set_view_point(self):
        # 添加调整图像的四个点
        data.PARAM.field.p_radius = 8 * (1-data.PARAM.mouse.scale)
        for i in range(4):
            dpg.draw_circle(center=data.PARAM.field.p[i],radius=data.PARAM.field.p_radius,fill=[0,255,0,200],parent="canvas",tag=f"p{i}")
    def draw_all(self):
        
        # self.draw_camera()
        # self.draw_field()
        # self.draw_set_view_point()
        # self.show_car()
        self.draw_debug()
        self.draw_ball()
def config_window():
    with dpg.window(tag="PARAM",label="PARAM"):
        with dpg.tab_bar():
            with dpg.tab(label="Config"):
                with dpg.collapsing_header(label="Camera Param"):
                        dpg.add_text("Gain:")
                        dpg.add_input_float(default_value=20, min_value=0.0, max_value=23.0,min_clamped=True,max_clamped=True,callback=callback.change_Gain_value,tag = "Gain_input")
                        dpg.add_slider_float(default_value=20, min_value=0.0, max_value=23.0,callback=callback.change_Gain_value,tag = "Gain_slider_input") 
                        dpg.add_text("ExposureTime:")
                        dpg.add_input_float(default_value=20, min_value=20.0, max_value=20000.0,min_clamped=True,max_clamped=True,callback=callback.change_ExposureTime_value,tag = "ExposureTime_input")
                        dpg.add_slider_float(default_value=10000, min_value=20.0, max_value=20000.0,callback=callback.change_ExposureTime_value,tag = "ExposureTime_slider_input") 
        # 边菜单
def side_menu():
    # 右主内容 
    with dpg.child_window(tag="side_menu_right", width=-1,height=-1,pos=(10,15),show=True,drop_callback=callback.add_plot_time_shape,payload_type='Drag&Drop'):
        draw_window()
def plot_window():
    with dpg.window(tag="PLOT",label="PLOT"):
        Object.plot_line([],[],-1,-1)
# 画布
def draw_window():
    with dpg.drawlist(width=0, height=0,tag ="drawlist",delay_search=True):
        with dpg.draw_node(tag="bg"):
            pass
        
        with dpg.draw_node(tag="canvas"):
            pass
        with dpg.draw_node(tag="config"):
            dpg.draw_text([10, 10],  color=[255, 255, 255, 255], size=40, tag="fps",text="Hello, world!")
def console_window():
    with dpg.child_window(label="T_console_window",tag="console_window"):
        dpg.add_text("Console:")
        dpg.add_input_text(multiline=True,width=-1, height=-1)
label = language.languages[theme.current_language]
obj = Object2D()