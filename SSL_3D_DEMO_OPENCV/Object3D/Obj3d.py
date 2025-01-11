
import pygfx as gfx
import BASE.Utils as utils
import BASE.GlobalData as data
import pylinalg as la
import numpy as np
class Debug2D:
    def __init__(self, scene):
        self.scene = scene
        self.car = None

    def create(self):
        # Create a box geometry
        self.car = gfx.Mesh(
            gfx.box_geometry(130, 130, 130),
            gfx.MeshPhongMaterial(color=(0, 0, 1, 1), flat_shading=True),
        )
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
        self.car.material.color = color
class Car3D:
    def __init__(self, scene):
        self.scene = scene
        self.car = None

    def create(self):
        # Create a box geometry
        self.car = gfx.Mesh(
            gfx.box_geometry(130, 130, 130),
            gfx.MeshPhongMaterial(color=(0, 0, 1, 1), flat_shading=True),
        )
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
        self.car.material.color = color

class CarController:
    def __init__(self, scene):
        self.scene = scene
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
        self.ball.local.position = [0, 0, data.ball_radius]
        self.scene.add(self.ball)
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
    def update(self):
        add, remove ,modified = utils.compare_dicts( self.car_data,data.car_data)
        if data.ball_data:
            self.ball.local.position = data.ball_data["pos"]
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
            pos = data.car_data[tag]["pos"]
            dir = data.car_data[tag]["dir"]
            color = [0,0,1,1] if data.car_data[tag]["color"] == "BLUE" else [1,1,0,1]
            self.car_data[tag]["carobj"].set_position(pos)
            self.car_data[tag]["carobj"].set_rotation(dir)
            # self.car_data[tag]["carobj"].set_color(color)



