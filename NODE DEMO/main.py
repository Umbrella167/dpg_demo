import dearpygui.dearpygui as dpg
import UI.Theme as theme
import UI.Language.Language as language
import UI.Components as component
import UI.HotKey as hotkey
import BASE.FunctionData as data
import BASE.Utils as utils
import time

import threading

# 初始化
dpg.create_context()
# 设置字体
theme.set_font()
# 当前语言
label = component.label
# 设置主题
theme.set_theme("Dark")
# 创建主窗口
with dpg.window(tag = "main_window",label="main window",no_close=True,no_collapse=True):
    component.node_editor_window()
    component.node_select_window()
    # dpg.add_image("texture_tag")
# 注册热建
with dpg.handler_registry():
    dpg.add_key_release_handler(callback=hotkey.on_key_release)

Observer_thread = threading.Thread(target=lambda:utils.monitor_directory("NODE"), daemon=True)
Observer_thread.start()


dpg.configure_app(docking=True, docking_space=True, init_file="dpg_layout.ini", load_init_file=True)
dpg.create_viewport(title=label["main_window"], width=800, height=600)
dpg.setup_dearpygui()
dpg.set_primary_window("main_window", False)

dpg.show_viewport()
# 主循环
count = 0
node = component.NODE()

while dpg.is_dearpygui_running():
    node.add_node(data.NodeData)
    dpg.render_dearpygui_frame()




dpg.start_dearpygui()
dpg.destroy_context()

