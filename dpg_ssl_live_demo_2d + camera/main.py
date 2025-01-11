from Step import *
import UI.Components as components
import dearpygui.dearpygui as dpg

if __name__ == '__main__':
    obj = components.obj
    init_all(obj)
    thread_start(obj)
    dpg_start_setup()
    try:
        main(obj)
    except:
        print("Error")
        dpg.destroy_context()
    finally:
        dpg.destroy_context()
