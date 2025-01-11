import dearpygui.dearpygui as dpg
import UI.LayoutManager as LayoutManager
import numpy as np
import threading
import VISION.vision_data as vision

class ShareData:
    def __init__(self):
        dpg.create_context()
        self.layout_manager = LayoutManager.LayoutManager()
        self.translation = self.layout_manager.get_drawer_window_size()
        self.translation = [item // 2 for item in self.translation]
        self.translation_matrix = dpg.create_translation_matrix(self.translation)
        self.scale = [0.15,0.15,1]
        self.scale_matrix = dpg.create_scale_matrix(self.scale)
        self.transform_matrix = self.translation_matrix * self.scale_matrix
        self.ui_loop_hook = {
            "DRAW_2D":{"func":None,"run":False},
            "DRAW_3D":{"func":None,"run":False},
        }
        self.pbmesg_thread_status = {
            "pbmesg_vision_thread":True,
            "pbmesg_debug_thread" :True
        }
        self.pbmesg_vision_thread = threading.Thread(target=lambda: vision.get_vision_data(self.get_pbmesg_thread_status,"pbmesg_vision_thread"), daemon=True)
        self.pbmesg_debug_thread  = threading.Thread(target=lambda: vision.get_debug_data(self.get_pbmesg_thread_status,"pbmesg_debug_thread"), daemon=True)
    def get_pbmesg_thread_status(self,item):
        return self.pbmesg_thread_status[item]
    def update_transform_matrix(self,translation = None,scale = None):
        if scale is not None:
            self.scale = scale
            self.scale_matrix = dpg.create_scale_matrix(self.scale)
        if translation is not None:
            self.translation = translation
            self.translation_matrix = dpg.create_translation_matrix(self.translation)
        self.transform_matrix = self.translation_matrix * self.scale_matrix
    def pbmesg_thread_start(self):
        if not self.pbmesg_vision_thread.is_alive():
            self.pbmesg_thread_status["pbmesg_vision_thread"] = True
            self.pbmesg_vision_thread = threading.Thread(target=lambda: vision.get_vision_data(self.get_pbmesg_thread_status,"pbmesg_vision_thread"), daemon=True)
            self.pbmesg_vision_thread.start()
        if not self.pbmesg_debug_thread.is_alive():
            self.pbmesg_thread_status["pbmesg_debug_thread"] = True
            self.pbmesg_debug_thread  = threading.Thread(target=lambda: vision.get_debug_data(self.get_pbmesg_thread_status,"pbmesg_debug_thread"), daemon=True)
            self.pbmesg_debug_thread.start()
    def pbmesg_thread_stop(self):
        if self.pbmesg_vision_thread.is_alive():
            self.pbmesg_thread_status["pbmesg_vision_thread"] = False
            self.pbmesg_vision_thread.join()
        if self.pbmesg_debug_thread.is_alive():
            print(1)
            self.pbmesg_thread_status["pbmesg_debug_thread"] = False
            self.pbmesg_debug_thread.join()
class DiyComponents:
    def __init__(self, data:ShareData):
        pass
    def checkbox_menu_item(self,label: str,tag: str,callback = None, **kwargs):
        def on_selectable():
            value = not dpg.get_value(tag)
            dpg.set_value(tag, value)
            if dpg.get_value(tag):
                callback()
        with dpg.group(horizontal=True, horizontal_spacing=0):
            selectable = dpg.add_selectable(disable_popup_close=True, callback=on_selectable)
            checkbox = dpg.add_menu_item(label=label,check=True,tag = tag, callback=on_selectable, **kwargs)
        return checkbox
    def checkbox_menu_true(self,label: str,tag: str,parent,callback = None, **kwargs):
        def on_selectable():
            if dpg.get_value(tag) and not (callback is None):
                callback()
        dpg.add_menu_item(label=label,check=True,tag = tag, parent=parent,callback=on_selectable)
    def radio_button(self,items,tag,callback = None):
        def on_selectable(sender,app_data,user_data):
            if not (callback is None):
                user_data(sender)
        dpg.add_radio_button(items=items,tag=tag,callback=on_selectable,user_data=callback)
class CallBack:
    def __init__(self, data:ShareData):
        self._data = data
        self._layout_manager = self._data.layout_manager
    def on_key_release(self,sender, app_data):
        if dpg.is_key_down(dpg.mvKey_Control) and app_data == dpg.mvKey_S:
            self._layout_manager.save_layout()
    def drawer_window_resize_callback(self,sender, app_data):
        item_tag = dpg.get_item_alias(app_data)
        w,h = dpg.get_item_width(item_tag),dpg.get_item_height(item_tag) - 35
        dpg.set_item_width("main_drawlist",w)
        dpg.set_item_height("main_drawlist",h)
        self._data.update_transform_matrix([w//2,h//2])
        dpg.apply_transform("canvas_node", self._data.transform_matrix)
    
    def ssl_show_menu_callback(self):
        app_data = dpg.get_value("ssl_show_menu_radiobutton")
        if app_data == "2D Show":
            self._data.pbmesg_thread_start()
            self._data.ui_loop_hook["DRAW_2D"]["run"] = True
            self._data.ui_loop_hook["DRAW_3D"]["run"] = False
            dpg.configure_item("canvas_node_2d",show=True)
            dpg.configure_item("canvas_node_3d",show=False)
        elif app_data == "3D Show":
            self._data.ui_loop_hook["DRAW_2D"]["run"] = False
            self._data.ui_loop_hook["DRAW_3D"]["run"] = True
            self._data.pbmesg_thread_start()
            dpg.configure_item("canvas_node_2d",show=False)
            dpg.configure_item("canvas_node_3d",show=True)
        elif app_data == "Close":
            self._data.ui_loop_hook["DRAW_2D"]["run"] = False
            self._data.ui_loop_hook["DRAW_3D"]["run"] = False
            self._data.pbmesg_thread_stop()
            dpg.configure_item("canvas_node_3d",show=False)
            dpg.configure_item("canvas_node_2d",show=False)

class UI:
    def __init__(self, data:ShareData):
        self._data = data
        self._layout_manager = data.layout_manager
        self._diycomponents = DiyComponents(data)
        self._callback = CallBack(data)
    def create_meun(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="Window"):
                with dpg.menu(label="SSL CANVAS"):
                        dpg.add_radio_button(items=["2D Show","3D Show","Close"],tag="ssl_show_menu_radiobutton",callback=self._callback.ssl_show_menu_callback)
                dpg.add_menu_item(label="Save",callback = self._layout_manager.save_layout)
    def show_ui(self):
        self._layout_manager.load_layout()
        dpg.setup_dearpygui()
        dpg.show_viewport()
    def run_loop(self,func = None):
        if func is not None:
            while dpg.is_dearpygui_running():
                for item in self._data.ui_loop_hook: 

                    if self._data.ui_loop_hook[item]["run"] == True and self._data.ui_loop_hook[item]["func"] is not None:
                        func_draw = self._data.ui_loop_hook[item]["func"]
                        texture_data = func_draw()
                        if item == "DRAW_3D":
                            dpg.set_value(item="texture_tag_3d",value= texture_data)
                        elif item == "DRAW_2D":
                            dpg.set_value(item="texture_tag_2d",value= texture_data)
                func()
                dpg.render_dearpygui_frame()
        else:
            dpg.start_dearpygui()
    def create_texture(self,SIZE_3D,SIZE_2D):
         height_3D, width_3D = SIZE_3D
         height_2D, width_2D = SIZE_2D
         texture_data = np.zeros((height_3D * width_3D * 4,), dtype=np.float32)
         texture_data = np.zeros((height_2D * width_2D * 4,), dtype=np.float32)
         with dpg.texture_registry(show=False):
            dpg.add_raw_texture(height_3D, width_3D, texture_data, tag="texture_tag_3d", format=dpg.mvFormat_Float_rgba)
            dpg.add_raw_texture(height_2D, width_2D, texture_data, tag="texture_tag_2d", format=dpg.mvFormat_Float_rgba)
    def create_viewport(self):
        self.create_draw_window()
        self.create_global_handler()
        self.create_meun()
        dpg.configure_app(docking=True, docking_space=True, init_file="dpg_layout.ini", load_init_file=True)
        dpg.create_viewport(title="TBK-RocosPy", width=1920, height=1080)
    def create_draw_window(self):
        with dpg.window(tag = "drawer_window",label="Drawer",no_close=True,no_collapse=True):
            with dpg.drawlist(width=1920, height=1080,tag ="main_drawlist",delay_search=True):
                with dpg.draw_node(tag="canvas_node"):
                    with dpg.draw_node(tag="canvas_node_3d",show=True):
                        dpg.draw_image("texture_tag_3d", pmin=[-6000,-4500], pmax=[6000,4500], tag="draw_image_3D",parent="canvas_node_3d")
                        dpg.draw_circle([0,0],5, color=[255,0,0,255],parent="canvas_node_3d",fill=[255,0,0,255])
                        dpg.draw_circle([-5900,-4500],5, color=[0,255,0,255],parent="canvas_node_3d",fill=[0,255,0,255])
                        # dpg.draw_circle([-4500,-3000],5, color=[0,255,0,255],parent="canvas_node_3d",fill=[0,255,0,255])
                    with dpg.draw_node(tag="canvas_node_2d",show=False):
                        dpg.draw_image("texture_tag_2d", pmin=[-6000,-4500], pmax=[6000,4500], tag="draw_image_2D",parent="canvas_node_2d")
                        dpg.draw_circle([-4500,-3000],5, color=[0,255,0,255],parent="canvas_node_2d",fill=[0,255,0,255])
                        dpg.draw_circle([4500,3000],5, color=[0,255,0,255],parent="canvas_node_2d",fill=[0,255,0,255])
                        dpg.draw_circle([0,0],5, color=[0,255,0,255],parent="canvas_node_2d",fill=[0,255,0,255])
        dpg.apply_transform("canvas_node",self._data.transform_matrix)
    def create_global_handler(self):
        with dpg.handler_registry() as global_hander:
            dpg.add_key_release_handler(callback=self._callback.on_key_release)
        with dpg.item_handler_registry() as item_handler_registry:
            dpg.add_item_resize_handler(callback=self._callback.drawer_window_resize_callback)
        dpg.bind_item_handler_registry("drawer_window", item_handler_registry)
