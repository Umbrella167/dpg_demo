import time
import random
import dearpygui.dearpygui as dpg
import serial
import serial.tools.list_ports
import math
from collections import deque
ports = []
data_now = []
time_shape = []
DEQUE_MAX_LEN = 50
burt_rate = 115200
# data_log = list(deque(maxlen=DEQUE_MAX_LEN))
data_x = list(deque(maxlen=DEQUE_MAX_LEN))
data_y = list(deque(maxlen=DEQUE_MAX_LEN))
data_dimensions = 1
 
update_plot = True
# 切割数据
def split_data(split_symbol, data):
    data_str = str(data)
    data_str = data_str.strip('[]')
    split_result = data_str.split(split_symbol)
    return [item.strip() for item in split_result]
 
def data_receiver():
    while True:
        # 模拟接收数据
        countx = time.time()
        county = random.random()
        data_x.append(countx)
        data_y.append(county)
        time.sleep(0.001)
        # dpg.set_value("line_series", [data_x, data_y])
        # dpg.fit_axis_data("xaxis")
 
def list_serial_ports():
    """ 列出当前系统上的所有串口 """
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port, desc, hwid in sorted(ports):
        available_ports.append({
            "port": port,
            "description": desc,
            "hardware_id": hwid
        })
    return available_ports
 
# 获取串口
def get_port_name(s):
    ports = []
    for port in s:
        ports.append(port["port"])
    return ports
 
def signal_generator(mode,time):
    y = 0
    if mode == "sin":
        return math.sin(time)
    else:
        return math.cos(time)
    
 
def get_data(time):
    global data_now
    global data_log
    data_now = signal_generator("sin",time)
    data_now += random.random()*0.5
    data_y.append(data_now)
        # data_now = 
# # 读取串口数据
# def read_serial_data(port, baudrate, timeout):
#     try:
#         ser = serial.Serial(port, baudrate, timeout=timeout)
#         print(f"Connected to {port} at {baudrate} baud.")
#         while ser.in_waiting > 0:
#             data = ser.readline().decode('utf-8').rstrip()
#             print(f"Received: {data}")
    
#     except serial.SerialException as e:
#         print(f"Error: {e}")
    # finally:
    #     if ser.is_open:
    #         print(ser.is_open)
    #         print("Serial connection closed.")
 