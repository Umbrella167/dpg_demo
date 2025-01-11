import UI.Components as components
import VISION.vision_data as vision
import threading
import Object3D.Obj3d as obj3d
import pygfx as gfx
from wgpu.gui.auto import WgpuCanvas, run
import numpy as np
import imageio.v3 as iio
import time

def thread_start(obj):
    # 启动数据接收线程
    print("Thread Starting...")
    vision_thread = threading.Thread(target=lambda: vision.get_vision_data(obj), daemon=True)
    debug_thread = threading.Thread(target=lambda: vision.get_debug_data(obj), daemon=True)
    debug_thread.start()
    vision_thread.start()
    print("Thread Started Successfully")

def caracteWorld():
    scene = gfx.Group()
    # 示例 NumPy 数组纹理数据 (这里创建一个简单的 64x64 红色图像)
    texture_data = np.zeros((64, 64, 4), dtype=np.uint8)
    texture_data[..., 1] = 255  # Red channel
    texture_data[..., 3] = 255  # Alpha channel (fully opaque)
    texture = gfx.Texture(texture_data, dim=2)
    plane = gfx.Mesh(
        gfx.plane_geometry(9000, 6000),
        gfx.MeshPhongMaterial(map=texture, color=(0, 1, 0, 1), flat_shading=True),
    )
    plane.local.position = [0, 0, 0]
    scene.add(plane)
    return scene, plane

def main(obj, plane):
    obj.draw_all()
    texture = gfx.Texture(obj.canvas, dim=2)
    plane.material.map = texture

    obj.clean_canvas()
    controller.update()

if __name__ == "__main__":
    canvas = WgpuCanvas(max_fps=180)
    obj = components.obj
    scene, plane = caracteWorld()

    # 读取并调整图像形状
    im = iio.imread("sky.jpg")
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
    background = gfx.Background(None, gfx.BackgroundSkyboxMaterial(map=tex))
    scene.add(background)

    controller = obj3d.CarController(scene)
    thread_start(obj)
    disp = gfx.Display(canvas)  # 传递 canvas 给 gfx.Display
    disp.stats = True
    disp.before_render = lambda: main(obj, plane)
    disp.show(scene)  # 显示场景
    run()  # 开始事件循环