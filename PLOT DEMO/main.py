import dearpygui.dearpygui as dpg
import dearpygui_ext.themes
import UI.Theme as theme
import UI.Language.Language as language
import UI.Components as component
import UI.HotKey as hotkey
import BASE.DataFactory as data
import threading
import dearpygui_ext

def data_receiver():
    print(1)
# 初始化
dpg.create_context()
# 设置字体
theme.set_font()
# 当前语言
label = component.label
# 设置主题
theme.set_theme("Dark")
# 创建主窗口
with dpg.window(tag = "main_window",label=label["main_window"],no_close=True,no_collapse=True):
    component.top_menu()
    component.side_menu()
    component.bottom_menu()
    # dpg.add_image("texture_tag")
# 注册热建
with dpg.handler_registry():
    dpg.add_key_release_handler(callback=hotkey.on_key_release)


# 启动数据接收线程
# data_thread = threading.Thread(target=data.data_receiver, daemon=True)
# data_thread.start()

dpg.configure_app(docking=True, docking_space=True, init_file="dpg_layout.ini", load_init_file=True)
dpg.create_viewport(title=label["main_window"], width=800, height=600)
dpg.setup_dearpygui()
dpg.set_primary_window("main_window", False)

dpg.show_viewport()
# 主循环
count = 0
while dpg.is_dearpygui_running():
    ports_read = data.list_serial_ports()
    count += dpg.get_delta_time()
    if ports_read:
        ports = data.get_port_name(ports_read)
        dpg.configure_item("found_port",show=True)
        dpg.configure_item("not_found",show=False)
        dpg.configure_item("port_list", items=ports)
    else:
        dpg.configure_item("found_port",show=False)
        dpg.configure_item("not_found",show=True)
    data.get_data(count)
    data.data_x.append(count)
    dpg.set_value("line_series",[data.data_x,data.data_y])
    if data.update_plot:
        dpg.fit_axis_data("xaxis")

    dpg.render_dearpygui_frame()



dpg.start_dearpygui()
dpg.destroy_context()

