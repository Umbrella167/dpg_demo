import pyglet
from pyglet import shapes
from pyglet import image
from pyglet.gl import *
from PIL import Image  # 需要安装PIL库：pip install pillow
import numpy as np
import cv2
# config = pyglet.gl.Config(sample_buffers=1, samples=16)  # 请求4x MSAA
window = pyglet.window.Window(960, 540,visible=False)
# # 启用线和多边形的平滑处理
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable(GL_POLYGON_SMOOTH)
glHint(GL_POLYGON_SMOOTH_HINT, GL_DONT_CARE)

batch = pyglet.graphics.Batch()
circle = shapes.Circle(700, 150, 100, segments = 1000,color=(50, 225, 30), batch=batch)
circle.position = (50, 50)
rectangle = shapes.Rectangle(250, 300, 400, 200, color=(255, 22, 20), batch=batch)
rectangle.opacity = 128
rectangle.rotation = 33
line = shapes.Line(100, 100, 100, 200, width=1, batch=batch)
line.position = (200, 200)
line2 = shapes.Line(150, 150, 444, 111, width=1, color=(200, 20, 20), batch=batch)
star = shapes.Star(800, 400, 60, 40, num_spikes=5, color=(255, 255, 0), batch=batch)

def draw2texture(batch,width, height):
    def attach_texture_to_framebuffer(framebuffer, texture):
        glBindFramebuffer(GL_FRAMEBUFFER, framebuffer.id)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture.id, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    framebuffer = pyglet.image.Framebuffer()
    # 创建Framebuffer和Texture
    texture = pyglet.image.Texture.create(width, width)
    # 直接使用OpenGL函数来附加Texture
    attach_texture_to_framebuffer(framebuffer, texture)
    framebuffer.bind()
    # 清除Framebuffer内容
    glClear(GL_COLOR_BUFFER_BIT)
    # 绘制batch到Framebuffer
    batch.draw()
    # 读取Framebuffer内容
    buffer = (GLubyte * (4 * width * height))(0)
    glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
    # 解绑Framebuffer
    framebuffer.unbind()
    # 绘制Texture到窗口
    # texture.blit(0, 0)
    img_data = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
    return img_data

img = draw2texture(batch,960, 540)