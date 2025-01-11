import numpy as np
vision = None
camera = np.zeros((1920, 1080,3), np.uint8)
car_data = {}
ball_data = {}
ball_radius = 43
class ConfigData:
    fps = 0
    zoomrate = 5
class PARAM:
    class field:
        # p = [[300,300],
        #      [900,300],
        #      [900,600],
        #      [300,600]]
        p = [[0,400],
             [600,400],
             [600,0],
             [0,0]]
        p_radius = 1
        width = 9000
        height = 6000
        size = [9000,6000]
    class canvas:
        width = 0
        height = 0
        size = [0,0]
        translation = [960,540,0]
        scale = [1,1,1]
        transform = 0
        translation_matrix = None
        scale_matrix = None
    class car:
        radius = 67
    class color:
        yellow = [255,255,0]
    class mouse:
        pos = [0,0]
        scale = 1
        click_obj = "canvas"
        click_pos = [0,0]
        pos_last = [0,0]
        ssl_pos = [0,0]

class time:
    delta_time = 0
    total_time = 0
    
