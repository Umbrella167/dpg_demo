import UI.Ui as ui
import dearpygui.dearpygui as dpg
import BASE.TBKApi as tbkapi

tbkapi = tbkapi.TBKAPI()
ui_data = ui.UiData()

def loop():
    try:
        tbkapi.update_param()
        tbkapi.update_message()
        UI.update_param_data()
    except Exception as e:
        print("etcd connection failed")
if __name__ == "__main__":
    dpg.create_context()
    UI = ui.UI(ui_data, tbkapi)
    UI._theme.set_theme("Dark")
    UI._theme.set_font(20)
    # 创建参数窗口
    UI.create_param_window()
    # 创建消息窗口
    UI.create_message_window()
    UI.create_viewport()
    UI.show_ui()
    UI.run_loop(loop)