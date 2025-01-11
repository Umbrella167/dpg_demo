import dearpygui.dearpygui as dpg
import BASE.CallBack as callback


# CTRL + S 保存
def on_key_release(sender, app_data):
    if dpg.is_key_down(dpg.mvKey_Control) and app_data == dpg.mvKey_S:
        callback.save_callback(sender, app_data, None)
    if app_data == dpg.mvKey_Spacebar:
        callback.plot_animation(sender, app_data, None)
