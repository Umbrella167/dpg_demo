
import pygfx as gfx
import BASE.Utils as utils
import BASE.GlobalData as data
import pylinalg as la
from PyQt6.QtGui import QPainter, QColor, QImage, QPen, QFont
from PyQt6.QtCore import QPoint,QRect,QRectF
import numpy as np
import imageio.v3 as iio
import math
import time
class Draw2D:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = QColor(50, 50, 50,1)
        self.image = QImage(width, height, QImage.Format.Format_RGB32)
        self.image.fill(self.background_color)
        self.painter = QPainter(self.image)
        self.color_transform = [[255, 255, 255,255],[255, 0, 0,255],[255, 165, 0,255],[255, 255, 0,255],[0, 255, 0,255],[0, 255, 255,255],[0, 0, 255,255],[160, 32, 240,255],[128, 128, 128,255],[0, 0, 0,255]]
    def draw_start(self):
        self.painter = QPainter(self.image)
    def translate(self, dx, dy):
        self.painter.translate(dx, dy)
    def scale(self, sx, sy):
        self.painter.scale(sx, sy)
    def draw_line(self, start, end, color, width: int):
        start = QPoint(int(start[0]),int(start[1]))
        end = QPoint(int(end[0]),int(end[1]))
        pen = QPen(QColor(color[0], color[1], color[2], color[3]), width)
        self.painter.setPen(pen)
        self.painter.drawLine(start, end)
    def draw_arc(self, rect_points, start_angle, span_angle, color, width: int):
        # 将传入的点转换为 QPoint
        top_left = QPoint(int(rect_points[0][0]), int(rect_points[0][1]))
        bottom_right = QPoint(int(rect_points[1][0]), int(rect_points[1][1]))
        # 创建矩形
        rect = QRect(top_left, bottom_right)
        # 设置画笔
        pen = QPen(QColor(color[0], color[1], color[2], color[3]), width)
        self.painter.setPen(pen)
        # 由于 QPainter 使用 1/16 度作为单位，需要转换角度并确保它们是整数
        start_angle_16 = int(start_angle * 16)
        span_angle_16 = int(span_angle * 16)
        # 绘制弧
        self.painter.drawArc(rect, start_angle_16, span_angle_16)
    def draw_rect(self, rect_points, color, width: int):
        # 将传入的点转换为 QPoint
        top_left = QPoint(int(rect_points[0][0]), int(rect_points[0][1]))
        bottom_right = QPoint(int(rect_points[1][0]), int(rect_points[1][1]))
        # 创建矩形
        rect = QRect(top_left, bottom_right)
        # 设置画笔
        pen = QPen(QColor(color[0], color[1], color[2], color[3]), width)
        self.painter.setPen(pen)
        # 绘制矩形
        self.painter.drawRect(rect)
    def draw_text(self, pos, text, size, color):
        # 设置字体
        font = QFont()
        font.setPointSize(int(size))
        self.painter.setFont(font)
        # 设置画笔
        pen = QPen(QColor(color[0], color[1], color[2], color[3]))
        self.painter.setPen(pen)

        # 将传入的点转换为 QPoint
        position = QPoint(int(pos[0]), int(pos[1]))
        # 绘制文本
        self.painter.drawText(position, text)
    def to_texture(self):
        ptr = self.image.constBits()
        ptr.setsize(self.image.sizeInBytes())
        arr = np.frombuffer(ptr, np.uint8).reshape(self.height, self.width, 4)
        arr = arr[:, :, [2, 1, 0, 3]]
        texture = gfx.Texture(arr, dim=2)
        return texture
    def clear(self):
        self.image.fill(self.background_color)  # Assuming white as the default background color
class Car3D:
    def __init__(self, scene):
        self.scene = scene
        self.car = None
    def create(self):
        # Create a box geometry
        self.car = gfx.Group(visible=True)
        self.car_body = gfx.Mesh(
            gfx.box_geometry(130, 130, 130),
            gfx.MeshPhongMaterial(color=(0, 0, 1, 1), flat_shading=True),
        )
        self.car_eye = gfx.Mesh(
            gfx.box_geometry(10, 120, 50),
            gfx.MeshPhongMaterial(color=(0, 0, 1, 1), flat_shading=True),
        )

        self.car_eye.local.position = [70, 0, 50]
        self.car.add(self.car_body,self.car_eye)
        self.scene.add(self.car)
    def delete(self):
        self.scene.remove(self.car)
        self.car = None
    def set_position(self, pos):
        x, y = pos
        z = data.ball_radius
        # print(x,y)
        self.car.local.position = [x,y,z]
        # self.car.local.position.y = y
    def set_rotation(self, dir):
        rot = la.quat_from_euler((-dir), order="Z")
        self.car.local.rotation = rot
    def set_color(self, color):
        self.car_body.material.color = color
        self.car_eye.material.color = [1,1,1,1] if color == "BLUE" else [0,0,0,1]
class World:
    def __init__(self):
        self.scene = gfx.Group()
        self.objz = 50
        self.plane = gfx.Mesh(
            gfx.plane_geometry(12000, 9000),
            gfx.MeshBasicMaterial(color=(0, 1, 0, 0), flat_shading=True),
        )
        self.plane.local.position = [0, 0, 0]
        self.scene.add(self.plane)
        self.goal([0,0,1,1],center=[-4500,0],width=1000,depth=200)
        self.goal([1,1,0,255],center=[4500,0],width=1000,depth=200)
        self.field_boundary([0,0],10000,7000,[0.2,0.2,0.2,1])
    def load_image(self,path):        # 读取并调整图像形状
        im = iio.imread(path)
        if len(im.shape) == 2:  # 如果图像是灰度图像，将其转换为RGB
            im = np.stack((im,) * 3, axis=-1)
        if im.shape[2] == 3:  # 如果图像没有Alpha通道，添加一个全不透明的Alpha通道
            im = np.concatenate([im, 255 * np.ones((*im.shape[:2], 1), dtype=np.uint8)], axis=2)
        width = im.shape[1]
        height = im.shape[0]
        # 确保调整后的形状是正确的
        im = im.reshape((height, width, 4))
        tex_size = (width, height, 1)  # 更改为2D纹理大小
        tex = gfx.Texture(im, dim=2, size=tex_size)
        return tex
    def add_background(self,path):
        # 读取并调整图像形状
        tex = self.load_image(path)
        
        background = gfx.Background(None, gfx.BackgroundSkyboxMaterial(map=tex))
        self.scene.add(background)
    def goal(self,color,center,width,depth):
        # 球门的三个板面
        z = 60
        dir = -1 if center[0] > 0 else 1
        goal_up = gfx.Mesh(
            gfx.box_geometry(10, depth,140),
            gfx.MeshBasicMaterial(color=color, flat_shading=True),
        )
        rot = la.quat_from_euler((math.pi/2), order="Z")
        goal_up.local.rotation = rot
        goal_up.local.position = [center[0] - dir * (depth / 2), center[1] + dir * (width / 2), z]

        goal_middle = gfx.Mesh(
            gfx.box_geometry(10, width,140),
            gfx.MeshBasicMaterial(color=color, flat_shading=True),
        )
        goal_middle.local.position = [center[0] - dir * depth, center[1], z]
        goal_down = gfx.Mesh(
            gfx.box_geometry(10, depth,140),
            gfx.MeshBasicMaterial(color=color, flat_shading=True),
        )
        rot = la.quat_from_euler((-math.pi/2), order="Z")
        goal_down.local.rotation = rot
        goal_down.local.position = [center[0] - dir * (depth / 2), center[1] - dir * (width / 2), z]
        self.scene.add(goal_up,goal_middle,goal_down)
    def field_boundary(self,center,width,height,color):
        
        thickness =  30
        height_boundary = 1000
        z = self.objz + height_boundary / 2
        dir = -1 if center[0] > 0 else 1
        tx = self.load_image("g1.png")

        boundary_up = gfx.Mesh(
            gfx.box_geometry(width, thickness,height_boundary),
            gfx.MeshBasicMaterial(map = tx,color=color, flat_shading=True),
        )
        boundary_up.local.position = [center[0], center[1] + dir * (height / 2), z]
        rot = la.quat_from_euler((-math.pi), order="X")
        boundary_up.local.rotation = rot


        boundary_down = gfx.Mesh(
            gfx.box_geometry(width, thickness,height_boundary),
            gfx.MeshBasicMaterial(map = tx,color=color, flat_shading=True),
        )
        rot = la.quat_from_euler((-math.pi), order="X")
        boundary_down.local.rotation = rot
        boundary_down.local.position = [center[0], center[1] - dir * (height / 2), z]


        boundary_left = gfx.Mesh(
            gfx.box_geometry(thickness, height,height_boundary),
            gfx.MeshBasicMaterial(map = tx,color=color, flat_shading=True),
        )
        rot = la.quat_from_euler((-math.pi), order="X")
        boundary_left.local.rotation = rot
        boundary_left.local.position = [center[0] + dir * width / 2, center[1], z]


        boundary_right = gfx.Mesh(
            gfx.box_geometry(thickness, height,height_boundary),
            gfx.MeshBasicMaterial(map = tx,color=color, flat_shading=True),
        )
        rot = la.quat_from_euler((-math.pi), order="X")
        boundary_up.local.rotation = rot
        boundary_right.local.position = [center[0] - dir * width / 2, center[1], z]

        self.scene.add(boundary_up,boundary_down,boundary_left,boundary_right)
class Camera:
    def __init__(self,scence):
        self.camera = gfx.PerspectiveCamera(60, 1, 1, 10000)
        self.camera.local.position = [0, 0, 1000]
        self.camera.local.rotation = la.quat_from_euler((math.pi / 2), order="Z")
        self.scene = scence

class DTCore:
    def __init__(self,width, height):
        self.width = width
        self.height = height
        self.scale_width = width / 12000
        self.scale_height = height / 9000

        self.world = World()
        # self. .add_background("sky.jpg")
        self.plane = self.world.plane

        self.scene = self.world.scene
        self.cars = {}
        self.car_data = {
            # tag: {
            #     "position": [0, 0],
            #     "rotation": 0,
            #     "color": (0, 0, 0, 1)
            # }
        }
        # 初始化球
        self.ball = gfx.Mesh(
            gfx.sphere_geometry(43, 43, 43),
            gfx.MeshPhongMaterial(color=(1, 0.647, 0, 1), flat_shading=True),
        )

        self.debug_drawer = Draw2D(width,height)
        self.debug_drawer.translate(int(width / 2),int(height / 2))
        self.debug_drawer.scale(self.scale_width,self.scale_height)
        self.debug_line = []
        self.debug_text = []
        self.debug_arc = []
        self.ball.local.position = [0, 0, data.ball_radius]
        self.scene.add(self.ball)
        self.draw2D()

    def draw_start(self):
        self.debug_drawer.draw_start()
        self.debug_drawer.translate(int(self.width / 2),int(self.height / 2))
        self.debug_drawer.scale(self.scale_width,self.scale_height)
    def add_car(self, tag, pos, dir, color):
        car = Car3D(self.scene)
        car.create()
        car.set_position( pos)
        car.set_rotation(dir)
        car.set_color(color)
        return car
    def remove_car(self, tag):
        if tag in self.cars:
            self.cars[tag].delete()
            del self.cars[tag]
            del self.car_data[tag]
    def draw2D(self):
        def draw_field():
            color = [255,255,255,200]
            P1 = [-4500,3000]
            P2 = [4500,3000]
            P3 = [4500,-3000]
            P4 = [-4500,-3000]
            width = 10
            self.debug_drawer.draw_line(P1, P2, color,width)
            self.debug_drawer.draw_line(P2, P3, color,width)
            self.debug_drawer.draw_line(P3, P4, color,width)
            self.debug_drawer.draw_line(P4, P1, color,width)
            self.debug_drawer.draw_line(utils.middle_pos(P1,P4), utils.middle_pos(P2,P3), color,width)
            self.debug_drawer.draw_line(utils.middle_pos(P1,P2), utils.middle_pos(P3,P4), color,width)
            self.debug_drawer.draw_arc([[-500,500],[500,-500]],0, 360, color,width)
            self.debug_drawer.draw_rect([[-4500,1000], [-3500,-1000]], color,width)
            self.debug_drawer.draw_rect([[3500,1000], [4500,-1000]], color,width)

            self.debug_drawer.draw_rect([[-4700,500], [-4500,-500]], color,width)
            self.debug_drawer.draw_rect([[4500,500], [4700,-500]], color,width)
        def draw_debug_line():
            debug_line = data.debug_line
            color_transform = self.debug_drawer.color_transform
            for line in debug_line:
                start = line[0]
                end = line[1]
                color = color_transform[line[2]]
                # self.debug_drawer.draw_line(start, end, color, 5)
        def draw_debug_arc():
            self.debug_arc = data.debug_arc
            for arc in self.debug_arc:
                rect_points = arc[0]
                start = arc[1]
                span = arc[2]
                color = self.debug_drawer.color_transform[arc[3]]
                self.debug_drawer.draw_arc(rect_points, start, span, color,5)
        def draw_text():
            self.debug_text = data.debug_text
            for texts_mesg in self.debug_text:
                pos = texts_mesg[0]
                text = texts_mesg[1]
                size = texts_mesg[2]
                color = self.debug_drawer.color_transform[texts_mesg[3]]
                self.debug_drawer.draw_text(pos, text, size,color)
        self.draw_start()
        draw_field()
        draw_debug_line()
        draw_debug_arc()
        # draw_text()
        self.debug_drawer.painter.end()
        draw_data = self.debug_drawer.to_texture()
        self.plane.material.map = draw_data

    def update(self):
        self.draw2D()
        add, remove ,modified = utils.compare_dicts( self.car_data,data.car_data)
        ball_comp = self.ball.local.position - data.ball_data["pos"]
        rate = 0.1
        self.ball.local.position.setflags(write=True)
        self.ball.local.position -= [ball_comp[0]*rate,ball_comp[1]*rate,0]
        # self.ball.local.position = data.ball_data["pos"]

        for tag in add:
            pos = data.car_data[tag]["pos"]
            dir = data.car_data[tag]["dir"]
            color = data.car_data[tag]["color"]
            carobj = self.add_car(tag, pos, dir, color)
            self.car_data[tag] = {
                "pos": pos,
                "dir": dir,
                "color": color,
                "carobj":carobj
            }
        for tag in remove:
            # self.remove_car(tag)
            self.car_data[tag]["carobj"].delete()
            del self.car_data[tag]
            pass

        for tag in modified:
            if tag in data.car_data:
                pos = data.car_data[tag]["pos"]
                dir = data.car_data[tag]["dir"]
                color = [0,0,1,1] if data.car_data[tag]["color"] == "BLUE" else [1,1,0,0]
                self.car_data[tag]["carobj"].set_position(pos)
                self.car_data[tag]["carobj"].set_rotation(dir)
                # self.car_data[tag]["carobj"].set_color(color)
