import dearpygui.dearpygui as dpg
import BASE.TBKApi as tbkapi
from typing import Union
import BASE.Utils as utils
import UI.LayoutManager as LayoutManager
import UI.Theme as theme
import math
import time


class UiData:
    def __init__(self):
        self.layout_manager = LayoutManager.LayoutManager()
        self.drawlist_height = 0
        self.drawlist_width = 0
        self.mouse_pos = [0, 0]
        self.mouse_pos_transform = [0, 0]
        self.click_obj = "canvas"
        self.mouse_pos_last = [0, 0]
        self.mouse_move = [0, 0]
        self.translation = [1920 // 2, 1080 // 2, 0]
        self.translation_matrix = dpg.create_translation_matrix(self.translation)
        self.scale = 1
        self.scale_matrix = dpg.create_scale_matrix([self.scale, self.scale, 1])
        self.transform = self.translation_matrix * self.scale_matrix
        self.collision_device = []
        self.collision_device_last = []


class DRAWOBJ:
    def __init__(self, data: UiData) -> None:
        self._data = data
        self.objects = {}
        self.objects_current = {}
        self.breath_count = 0
        self.increasing = True
        self.pause_start_time = None
        self.wave_start_times = [time.time()]
        self.wave_radii = [0]
        self.radar_angle = 0
        self.wave_pos = [0, 0]

    def draw_gradient_circle(
        self,
        center,
        max_radius,
        color_start,
        color_end,
        steps,
        parent,
        breath=False,
        fill=False,
        in_cluster=False,
    ):

        if breath:
            if self.pause_start_time is None:  # 正在呼吸
                if self.increasing:
                    self.breath_count += 0.006
                else:
                    self.breath_count -= 0.006

                if self.breath_count >= 5:
                    self.increasing = False
                    self.pause_start_time = time.time()
                elif self.breath_count <= 0:
                    self.increasing = True

            else:  # 正在暂停
                if time.time() - self.pause_start_time >= 1:
                    self.pause_start_time = None

            max_radius += self.breath_count
        else:
            max_radius = steps - 50

        for i in range(steps):
            radius = max_radius * (i / steps)
            # 线性插值计算颜色
            t = i / steps
            color = [
                int(color_start[0] * (1 - t) + color_end[0] * t),
                int(color_start[1] * (1 - t) + color_end[1] * t),
                int(color_start[2] * (1 - t) + color_end[2] * t),
                int(color_start[3] * (1 - t) + color_end[3] * t),
            ]
            if fill:
                fill = color

            dpg.draw_circle(
                center=center,
                radius=radius * self._data.scale,
                color=color,
                fill=fill,
                thickness=3,
                parent=parent,
            )
        if in_cluster:
            dpg.draw_circle(
                center=center,
                radius=max_radius * self._data.scale,
                color=[20, 20, 255, 150],
                thickness=3,
                parent=parent,
            )

    def draw_self(
        self,
        in_cluster: bool,
        lable: str,
        center: list[int, int],
        radius: float,
        status: str,
        parent: Union[int, str],
        breath: bool,
        tag: Union[int, str],
        name: str = "",
    ):

        # color = {
        #     "running": [[0, 0, 0, 0], [100, 200, 100, 100]],
        #     "stopped": [[0, 0, 0, 0], [255, 0, 0, 30]],
        #     "unknown": [[0, 0, 0, 0], [100, 100, 100, 100]],
        # }
        color = {
            "running": [[0, 0, 0, 0], [25, 135, 84, 80]],
            "stopped": [[0, 0, 0, 0], [180, 52, 69, 80]],
            "unknown": [[0, 0, 0, 0], [108, 117, 125, 80]],
        }
        # status_to_image = {
        #     "running": "tbkgreen_image",
        #     "stopped": "tbkorange_image",
        # }
        # image_radius = 50 if radius == 100 else 25

        # if status != "unknown":
        #     image = status_to_image[status]
        #     if in_cluster:
        #         image = "tbkblue_image"
        #     dpg.draw_image(
        #         image,
        #         [center[0] - image_radius, center[1] - image_radius],
        #         [center[0] + image_radius, center[1] + image_radius],
        #         parent=parent,
        #     )

        dpg.add_draw_node(parent=parent, tag=tag)

        # self.draw_gradient_circle(
        #     center,
        #     radius,
        #     color[status][0],
        #     color[status][1],
        #     100,
        #     parent=tag,
        #     breath=breath,
        #     in_cluster=in_cluster,
        # )

        color = {
            "running": [[25, 135,84, 200]],
            "stopped": [[220, 52, 69, 200]],
            "unknown": [[108, 117, 125, 200]],
        }

        dpg.draw_circle(center=center,radius=radius * self._data.scale,color=color[status][0],fill=color[status][0],parent=tag)
        if in_cluster:
            dpg.draw_circle(
                center=center,
                radius=radius * self._data.scale,
                color=[12, 110, 253, 150],
                thickness=5,
                parent=tag,
            )
        size_text_lable = dpg.get_text_size(lable)
        if size_text_lable is not None:
            size_text_lable = size_text_lable[0]
        else:
            size_text_lable = 0
        if lable != "":
            lable = lable

        dpg.draw_text(
            pos=[center[0] - (size_text_lable / 2), center[1] - 35],
            text=lable,
            size=20 * self._data.scale,
            parent=tag,
            color=[255, 255, 255, 180],
        )

        size_text = dpg.get_text_size(name)
        if size_text is not None:
            size_text = size_text[0]
        else:
            size_text = 0
        if name != "":
            name = f"({name})"

        dpg.draw_text(
            pos=[center[0] - (size_text / 2) - 3, center[1]],
            text=name,
            size=20 * self._data.scale,
            parent=tag,
            color=[255, 255, 255, 255],
        )

    def draw_init(self, device_table):
        lenth = len(device_table) - 1
        angle_between_devices = 360 / lenth
        objects = {}
        for index, device in enumerate(device_table):

            ip = device["ip"]
            status = device["status"]
            is_current = device["is_current"]
            in_cluster = device["in_cluster"]
            breath = True if status != "unknown" else False

            tag = f"{ip}"

            if status == "running":
                color = [0, 255, 0, 255]
            elif status == "stopped":
                color = [255, 0, 0, 255]
            else:
                color = [0, 0, 0, 255]
            if is_current:
                self.draw_self(
                    center=[0, 0],
                    lable=ip,
                    radius=100,
                    status=status,
                    parent="canvas",
                    breath=breath,
                    tag=tag,
                    in_cluster=in_cluster,
                )
                objects[tag] = {
                    "pos": [0, 0],
                    "radius": 100,
                    "status": status,
                    "is_current": True,
                    "in_cluster": in_cluster,
                    "name": self._data.layout_manager.get_device_name(ip),
                }
                self.objects_current = objects[tag]
                self.objects_current["ip"] = tag
            else:
                radius = 120 if in_cluster else 300
                fill_color = [0, 255, 255, 80] if in_cluster else [200, 200, 200, 30]
                angle_degrees = index * angle_between_devices
                angle_radians = math.radians(angle_degrees)
                x = radius * math.cos(angle_radians)
                y = radius * math.sin(angle_radians)
                self.draw_self(
                    center=[x, y],
                    lable=ip,
                    radius=50,
                    status=status,
                    parent="canvas",
                    breath=breath,
                    tag=tag,
                    in_cluster=in_cluster,
                )
                objects[tag] = {
                    "pos": [x, y],
                    "radius": 50,
                    "status": status,
                    "is_current": False,
                    "in_cluster": in_cluster,
                    "name": self._data.layout_manager.get_device_name(ip),
                }
        self.objects = objects
        self._data.collision_device_last = utils.collision(
            self.objects_current["ip"], self.objects
        )

    def draw_wave(self, center, parent, color_start, color_end, speed=50):
        current_time = time.time()
        new_wave_start_time = self.wave_start_times[-1] + 2  # 每秒钟创建一个新波纹
        if current_time >= new_wave_start_time:
            self.wave_start_times.append(current_time)
            self.wave_radii.append(0)

        # Update and draw each wave
        for i in range(len(self.wave_start_times)):
            elapsed_time = current_time - self.wave_start_times[i]
            self.wave_radii[i] = elapsed_time * speed
            self.draw_gradient_circle(
                center=center,
                max_radius=self.wave_radii[i],
                color_start=color_start,
                color_end=color_end,
                steps=10,
                parent=parent,
                breath=True,
                fill=True,
            )
        # Remove waves that have exceeded the maximum radius
        self.wave_start_times = [
            start_time
            for start_time, radius in zip(self.wave_start_times, self.wave_radii)
            if radius <= 300
        ]
        self.wave_radii = [radius for radius in self.wave_radii if radius <= 300]

    def draw_all(self):
        self.draw_wave(
            center=self.wave_pos,
            parent="canvas",
            color_start=[0, 0, 0, 0],
            color_end=[100, 100, 100, 10],
        )

        for obj in self.objects:
            pos = self.objects[obj]["pos"]
            radius = self.objects[obj]["radius"]
            status = self.objects[obj]["status"]
            breath = True if status != "unknown" else False
            is_current = self.objects[obj]["is_current"]
            in_cluster = self.objects[obj]["in_cluster"]
            name = self.objects[obj]["name"]

            if obj != "current":
                self.draw_self(
                    center=pos,
                    lable=obj,
                    radius=radius,
                    status=status,
                    parent="canvas",
                    breath=breath,
                    tag=obj,
                    in_cluster=in_cluster,
                    name=name,
                )
                if is_current:
                    self.wave_pos = pos


class CallBack:
    def __init__(self, data: UiData, drawobj: DRAWOBJ):
        self._data = data
        self._layout_manager = self._data.layout_manager
        self._drawobj = drawobj
        self.fllow_rate = 5

    def on_key_release(self, sender, app_data):
        if dpg.is_key_down(dpg.mvKey_Control) and app_data == dpg.mvKey_S:
            self._layout_manager.save_layout()
        if app_data == dpg.mvKey_Escape:
            if dpg.does_item_exist("login_window"):
                dpg.delete_item("login_window")
            if dpg.does_item_exist("rightmenu_window"):
                dpg.delete_item("rightmenu_window")
        if app_data == dpg.mvKey_Return or app_data == 335:
            if dpg.does_item_exist("login_window"):
                self.login(
                    None, None, dpg.get_item_user_data("login_window_login_button")
                )
            if dpg.does_item_exist("rightmenu_window"):
                dpg.delete_item("rightmenu_window")

    def mouse_wheel_handler(self, sender, app_data):
        if dpg.get_item_alias(dpg.get_focused_item()) == "main_drawlist":
            step = 0.05
            mouse_x, mouse_y = self._data.mouse_pos
            translation_x, translation_y, _ = self._data.translation
            world_mouse_x = (mouse_x - translation_x) / self._data.scale
            world_mouse_y = (mouse_y - translation_y) / self._data.scale
            # 更新缩放比例
            self._data.scale += step if app_data > 0 else -step
            self._data.scale = max(0.3, self._data.scale)
            self._data.scale = min(1.5, self._data.scale)
            self._data.scale_matrix = dpg.create_scale_matrix(
                [self._data.scale, self._data.scale, 1]
            )
            # 计算新的平移值
            new_translation_x = mouse_x - world_mouse_x * self._data.scale
            new_translation_y = mouse_y - world_mouse_y * self._data.scale
            self._data.translation = [new_translation_x, new_translation_y, 0]
            self._data.translation_matrix = dpg.create_translation_matrix(
                self._data.translation
            )

    def mouse_move_callback(self):
        if dpg.is_mouse_button_down(dpg.mvMouseButton_Middle):
            translation_x, translation_y, _ = self._data.translation
            move_x, move_y = self._data.mouse_move
            new_x, new_y = utils.clamp(
                translation_x + move_x, 0, self._data.drawlist_width
            ), utils.clamp(translation_y + move_y, 0, self._data.drawlist_height)
            self._data.translation = [new_x, new_y, 0]
            self._data.translation_matrix = dpg.create_translation_matrix(
                self._data.translation
            )

    def window_resize_callback(self):
        self._data.translation = [
            self._data.drawlist_width // 2,
            self._data.drawlist_height // 2,
            0,
        ]
        self._data.translation_matrix = dpg.create_translation_matrix(
            self._data.translation
        )

    def left_mouse_down_callback(self):

        if dpg.get_item_alias(dpg.get_focused_item()) == "main_drawlist":
            self.fllow_rate = 9 if not any(self._data.mouse_move) else 2

            if self._data.click_obj != "canvas":
                obj_pos = self._drawobj.objects[self._data.click_obj]["pos"]
                x_error = self._data.mouse_pos_transform[0] - obj_pos[0]
                y_error = self._data.mouse_pos_transform[1] - obj_pos[1]
                obj_pos[0] += x_error / self.fllow_rate
                obj_pos[1] += y_error / self.fllow_rate
            else:
                if dpg.does_item_exist("login_window"):
                    dpg.delete_item("login_window")
                if dpg.does_item_exist("rightmenu_window"):
                    dpg.delete_item("rightmenu_window")

    def left_mouse_release_callback(self, sender, app_data, user_data):
        pop_login_window = user_data
        if dpg.get_item_alias(dpg.get_focused_item()) == "main_drawlist":
            current = self._drawobj.objects_current
            self._data.collision_device = utils.collision(
                current["ip"], self._drawobj.objects
            )
            set_now = set(self._data.collision_device)
            set_last = set(self._data.collision_device_last)
            remove_device = set_last - set_now
            if remove_device != set() and set_last != set():
                self.login_out(list(remove_device))

            for device in self._data.collision_device:
                if not self._drawobj.objects[device]["in_cluster"]:
                    pos = self._drawobj.objects[current["ip"]]["pos"]
                    pop_login_window(dpg.get_mouse_pos(), device)
            self._data.collision_device_last = self._data.collision_device

    def Right_mouse_release_callback(self, sender, app_data, user_data):
        pop_right_menu = user_data
        if self._data.click_obj != "canvas":
            pop_right_menu(self._data.click_obj)
        else:
            if dpg.does_item_exist("login_window"):
                dpg.delete_item("login_window")
            if dpg.does_item_exist("rightmenu_window"):
                dpg.delete_item("rightmenu_window")

    def remember_callback(self, sender, app_data, user_data):
        ip = user_data
        if app_data:
            self._data.layout_manager.save_input_data(
                ip=ip, input_tag="login_window_username_input"
            )
            self._data.layout_manager.save_input_data(
                ip=ip, input_tag="login_window_password_input"
            )
        else:
            dpg.set_value("login_window_username_input", "")
            dpg.set_value("login_window_password_input", "")
            self._data.layout_manager.save_input_data(
                ip=ip, input_tag="login_window_username_input"
            )
            self._data.layout_manager.save_input_data(
                ip=ip, input_tag="login_window_password_input"
            )

        self._data.layout_manager.save_input_data(
            ip=ip, input_tag="login_window_remember_checkbox"
        )

    def device_rename(self, sender, app_data, user_data):
        ip = user_data
        tag = dpg.get_item_alias(sender)
        self._drawobj.objects[user_data]["name"] = app_data
        self._layout_manager.save_input_data(ip, tag)

    # 登陆加入集群
    def login(self, sender, app_data, user_data):
        ip = user_data
        username = dpg.get_value("login_window_username_input")
        password = dpg.get_value("login_window_password_input")

        if username == "123" and password == "123":
            self._drawobj.objects[ip]["in_cluster"] = True
            dpg.delete_item("login_window")
        else:
            self._drawobj.objects[ip]["in_cluster"] = False
            dpg.configure_item("login_window_spacer", width=50)
            dpg.set_value("login_window_text", "Login failed")

    # 退出集群
    def login_out(self, devices):

        for ip in devices:

            self._drawobj.objects[ip]["in_cluster"] = False

    # 右键菜单 - 开始
    def device_start(self, sender, app_data, user_data):
        ip = user_data
        pass

    # 右键菜单 - 停止
    def device_stop(self, sender, app_data, user_data):
        ip = user_data
        pass

    # 右键菜单 - 初始化
    def device_init(self, sender, app_data, user_data):
        ip = user_data
        pass

    # 右键菜单 - 重置
    def device_reset(self, sender, app_data, user_data):
        ip = user_data
        pass


class UI:
    def __init__(self, data: UiData, tbkapi: tbkapi.TBKAPI):
        self._data = data
        self._tbkapi = tbkapi
        self._layout_manager = self._data.layout_manager
        self._drawobj = DRAWOBJ(self._data)
        self._callback = CallBack(self._data, self._drawobj)
        self._theme = theme
        self.load_image()

    def load_image(self):
        pass
        # width_blue, height_blue, channels, data_blue = dpg.load_image(
        #     "UI/Image/tbk_blue.png"
        # )
        # width_orange, height_orange, channels1, data_orange = dpg.load_image(
        #     "UI/Image/tbk_orange.png"
        # )
        # width_green, height_green, channels, data_green = dpg.load_image(
        #     "UI/Image/tbk_green.png"
        # )

        # with dpg.texture_registry():
        #     dpg.add_static_texture(
        #         width_blue, height_blue, data_blue, tag="tbkblue_image"
        #     )
        #     dpg.add_static_texture(
        #         width_orange, height_orange, data_orange, tag="tbkorange_image"
        #     )
        #     dpg.add_static_texture(
        #         width_green, height_green, data_green, tag="tbkgreen_image"
        #     )

    def show_ui(self):
        self._layout_manager.load_layout()
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def run_loop(self, func=None):
        if func is not None:
            while dpg.is_dearpygui_running():
                func()
                dpg.render_dearpygui_frame()
        else:
            dpg.start_dearpygui()

    def create_viewport(self):
        self.create_global_handler()
        # dpg.configure_app(
        #     docking=False,
        #     docking_space=True,
        #     init_file="dpg_layout.ini",
        #     load_init_file=True,
        # )
        dpg.create_viewport(
            title="CONNECTOR", width=1920, height=1080, clear_color=(0, 0, 0, 0)
        )

    def create_global_handler(self):
        with dpg.handler_registry() as global_hander:
            dpg.add_key_release_handler(callback=self._callback.on_key_release)
            dpg.add_mouse_wheel_handler(callback=self._callback.mouse_wheel_handler)
            dpg.add_mouse_move_handler(callback=self._callback.mouse_move_callback)
            dpg.add_mouse_click_handler(
                button=dpg.mvMouseButton_Right,
                callback=self._callback.Right_mouse_release_callback,
                user_data=self.pop_right_menu,
            )
            dpg.add_mouse_release_handler(
                button=dpg.mvMouseButton_Left,
                callback=self._callback.left_mouse_release_callback,
                user_data=self.pop_login_window,
            )
            dpg.add_mouse_down_handler(
                button=dpg.mvMouseButton_Left,
                callback=self._callback.left_mouse_down_callback,
            )
            dpg.set_viewport_resize_callback(
                callback=self._callback.window_resize_callback
            )

    def create_draw_window(self):
        with dpg.window(label="Draw", width=1920, height=1080, tag="draw_window"):
            with dpg.drawlist(width=0, height=0, tag="main_drawlist"):
                # with dpg.draw_node(tag= "background"):
                #     dpg.draw_image("background_image", [-912, -484], [912, 484])
                #     pass
                with dpg.draw_node(tag="canvas"):
                    pass

        w, h = self._layout_manager.get_window_size("draw_window")
        self._data.translation = [w // 2, h // 2, 0]
        self._data.translation_matrix = dpg.create_translation_matrix(
            self._data.translation
        )

    def update_draw_window(self, device_table):
        self._data.click_obj = utils.get_close_mouse_device(
            self._drawobj.objects, self._data.mouse_pos_transform
        )
        dpg.delete_item("canvas", children_only=True)
        width, height = dpg.get_item_rect_size("draw_window")
        self._data.drawlist_width, self._data.drawlist_height = width, height
        dpg.set_item_width("main_drawlist", width)
        dpg.set_item_height("main_drawlist", height - 18)
        self._data.mouse_pos = (
            dpg.get_mouse_pos()
            if (dpg.get_item_alias(dpg.get_focused_item()) == "main_drawlist")
            else [-99999, -99999]
        )

        self._data.mouse_pos_transform = utils.mouse2transfrom(
            self._data.mouse_pos, self._data.translation_matrix, self._data.scale
        )
        self._data.mouse_move = [
            self._data.mouse_pos[0] - self._data.mouse_pos_last[0],
            self._data.mouse_pos[1] - self._data.mouse_pos_last[1],
        ]

        self._data.transform = self._data.translation_matrix * self._data.scale_matrix
        dpg.apply_transform("canvas", self._data.transform)
        # dpg.apply_transform("background", self._data.transform)

        dpg.draw_circle(
            center=self._data.mouse_pos_transform,
            radius=5,
            color=[255, 255, 255, 255],
            fill=[255, 255, 255, 255],
            parent="canvas",
        )
        self._drawobj.draw_all()
        self._data.mouse_pos_last = self._data.mouse_pos

    def pop_login_window(self, pos, ip):
        if not dpg.does_item_exist("login_window"):
            input_width = 100
            uuid = "login_window"
            dpg.add_window(
                label=f"Login to {ip}",
                width=240,
                height=200,
                tag=uuid,
                no_collapse=True,
                no_title_bar=True,
                no_resize=True,
                pos=pos,
                # popup=True,
            )
            with dpg.group(horizontal=True, parent=uuid):
                dpg.add_spacer(width=20, tag="login_window_spacer")
                dpg.add_text(f"Login to {ip}", tag="login_window_text")
                # dpg.add_spacer(width=100)
            dpg.add_input_text(
                default_value="",
                width=-1,
                hint="Username",
                parent=uuid,
                tag="login_window_username_input",
                callback=self._callback.remember_callback,
            )

            dpg.add_input_text(
                default_value="",
                width=-1,
                hint="Password",
                password=True,
                parent=uuid,
                tag="login_window_password_input",
                callback=self._callback.remember_callback,
            )
            group_id = dpg.generate_uuid()

            dpg.add_button(
                label="Login",
                width=-1,
                parent=uuid,
                callback=self._callback.login,
                user_data=ip,
                tag="login_window_login_button",
            )
            dpg.add_spacer(height=1, parent=uuid)

            with dpg.group(horizontal=True, parent=uuid, tag=group_id):
                dpg.add_text("Remember me")
                dpg.add_spacer(width=72)
                dpg.add_checkbox(
                    tag="login_window_remember_checkbox",
                    callback=self._callback.remember_callback,
                    user_data=ip,
                )

            self._layout_manager.load_input_data(ip, "login_window_username_input")
            self._layout_manager.load_input_data(ip, "login_window_password_input")
            self._layout_manager.load_input_data(ip, "login_window_remember_checkbox")
            if not dpg.get_value("login_window_remember_checkbox"):
                dpg.focus_item("login_window_username_input")

    # 右键菜单UI
    def pop_right_menu(self, ip):
        if not dpg.does_item_exist("rightmenu_window"):
            uuid = "rightmenu_window"
            dpg.add_window(
                # width=240,
                # height=140,
                tag=uuid,
                no_collapse=True,
                no_title_bar=True,
                no_resize=True,
                popup=True,
                no_scrollbar=True,
            )
            dpg.add_button(
                label="Start",
                width=-1,
                parent=uuid,
                callback=self._callback.device_start,
                user_data=ip,
                tag="rightmenu_start_button",
            )
            dpg.add_button(
                label="Stop",
                width=-1,
                parent=uuid,
                callback=self._callback.device_stop,
                user_data=ip,
                tag="rightmenu_stop_button",
            )
            dpg.add_button(
                label="Init",
                width=-1,
                parent=uuid,
                callback=self._callback.device_init,
                user_data=ip,
                tag="rightmenu_init_button",
            )
            dpg.add_button(
                label="Reset",
                width=-1,
                parent=uuid,
                callback=self._callback.device_reset,
                user_data=ip,
                tag="rightmenu_reset_button",
            )
            dpg.add_input_text(
                width=-1,
                parent=uuid,
                callback=self._callback.device_rename,
                tag="rightmenu_rename_input",
                hint="Rename",
                user_data=ip,
            )
            self._layout_manager.load_input_data(ip, "rightmenu_rename_input")
