import dearpygui.dearpygui as dpg
import BASE.DataFactory as data
# 保存页面布局
def save_callback(sender, app_data, user_data):
    dpg.save_init_file("dpg_layout.ini")

def plot_animation(sender, app_data, user_data):
    data.update_plot = not data.update_plot
    print(data.update_plot)
# 返回鼠标点击位置
def get_mouse_click_coordinates(sender, app_data):
    x, y = dpg.get_mouse_pos()
    print(f"Mouse clicked at: ({x}, {y})")

def show_components(tags,is_show=True):
    dpg.configure_item(tags,show=is_show)

def show_viewport():
    dpg.configure_item("viewport_group",show=True)
    dpg.configure_item("home_group",show=False)
def show_home():
    dpg.configure_item("viewport_group",show=False)
    dpg.configure_item("home_group",show=True)
def add_plot_time_shape():
    dpg.add_plot(label="Time Shape", parent="viewport_group")
def rade_combo(sender, app_data, user_data):
    data.burt_rate = app_data
