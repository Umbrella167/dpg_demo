import BASE.GlobalData as data
import dearpygui.dearpygui as dpg
import math
import numpy as np
def get_close_mouse_car(obj):
    min_distance = 99999
    closest_tag = "canvas"
    mouse_pos = data.PARAM.mouse.ssl_pos
    for i in  range(4) :
        pos = data.PARAM.field.p[i]
        distance = calculate_distance(mouse_pos, pos)
        if distance < min_distance:
            min_distance = distance
            if min_distance <= data.PARAM.field.p_radius + 100:
                closest_tag = f"p{i}"
    data.PARAM.mouse.click_obj = closest_tag
    return closest_tag
def calculate_distance( pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
def middle_pos( pos1, pos2):
    return [(pos1[0] + pos2[0]) / 2,(pos1[1] + pos2[1]) / 2]
def calculate_center_point(points):
    """
    计算四边形的中心点
    :param points: 四边形四个点的坐标列表 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    :return: 四边形中心点的坐标 (x, y)
    """
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    
    center_x = sum(x_coords) / 4
    center_y = sum(y_coords) / 4
    
    return center_x, center_y

def apply_transform(matrix, point):
    # 将 DearPyGui 矩阵转换为 NumPy 矩阵
    np_matrix = np.array(matrix).reshape(3, 3)
    # 确保 point 是 [x, y, 1]
    point = np.array([point[0], point[1], 1])
    # 进行矩阵乘法
    transformed_point = np_matrix @ point
    return transformed_point[:2]  # 返回 [x, y]

def matrix2list_mouse(matrix):
    transform = []
    for i in range(16):
        transform.append(matrix[i])
    data_array = np.array(transform)
    matrix = data_array.reshape(4, 4)
    matrix[0, 3] = -1 * matrix[-1, 0]
    matrix[1, 3] = -1 * matrix[-1, 1]
    matrix[-1, 0] = 0
    matrix[-1, 1] = 0
    return np.array(matrix)
def matrix2list(matrix):
    transform = []
    for i in range(16):
        transform.append(matrix[i])
    data_array = np.array(transform)
    matrix = data_array.reshape(4, 4)
    matrix[0, 3] = matrix[-1, 0]
    matrix[1, 3] = matrix[-1, 1]
    matrix[-1, 0] = 0
    matrix[-1, 1] = 0
    return np.array(matrix)
# def get_texture_data(image):
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image = cv2.flip(image,2)
#     texture_data = image.ravel().astype('float32') / 255
#     return texture_data
def mouse2ssl(x,y,translation_matrix,scale):
    x1,y1 = (matrix2list_mouse(translation_matrix) @ np.array([x,y,1,1]))[:2]
    return int(x1 / scale),int(-1 * y1 / scale)

def get_fps():
    delta_time =  dpg.get_delta_time()
    if delta_time:
        data.time.delta_time += delta_time
        data.time.total_time += delta_time
        if data.time.delta_time > 1:
            data.ConfigData.fps = 1 / delta_time
            data.time.delta_time = 0

def swap_elements(lst, element1, element2):
    try:
        # 找到元素的索引
        index1 = lst.index(element1)
        index2 = lst.index(element2)
        # 交换元素
        lst[index1], lst[index2] = lst[index2], lst[index1]
    except ValueError:
        print("其中一个元素不在列表中")
def compare_dicts(dict1, dict2):
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())

    added_keys = keys2 - keys1
    removed_keys = keys1 - keys2
    common_keys = keys1 & keys2
    modified_items = {key: dict2[key] for key in common_keys if dict1[key] != dict2[key]}
    return added_keys, removed_keys, modified_items
