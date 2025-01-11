
vision = None
class ConfigData:
    fps = 0
    zoomrate = 5
class PARAM:
    class field:
        width = 9000
        height = 6000
        size = [9000,6000]
    class canvs:
        width = 0
        height = 0
        size = [0,0]
        translation = [960,540,0]
        scale = [1,1,1]
        transform = 0
        translation_matrix = None
        scale_matrix = None
    class car:
        radius = 67 * 1.3
    class color:
        yellow = [255,255,0]
    class mouse:
        pos = [0,0]
        scale = 1
        click_obj = "canvs"
        click_pos = [0,0]
        pos_last = [0,0]

class time:
    delta_time = 0
    total_time = 0
    
