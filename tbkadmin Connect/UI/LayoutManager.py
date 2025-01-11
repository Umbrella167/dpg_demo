import dearpygui.dearpygui as dpg
import json


class LayoutManager:
    def __init__(self, settings_file="UI/layout_settings.json",input_data_file = "UI/input_data.json"):
        # 初始化布局管理器，设置保存布局的文件名
        self.settings_file = settings_file
        self.input_data_file = input_data_file
        try:
            with open(self.input_data_file, "r") as file:
                self.save_objects = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_objects = {}
    def save_layout(self):
        # 保存当前布局设置到文件
        layout_data = {}

        # 将当前布局保存到临时文件"dpg_layout.ini"
        dpg.save_init_file("UI/dpg_layout.ini")

        # 遍历所有项目，获取其别名和类型
        for item in dpg.get_all_items():
            item = dpg.get_item_alias(item)
            if item:
                _type = item.split("_")[-1]
                # 如果项目是复选框类型，保存其当前值
                if _type == "checkbox":
                    layout_data[item] = {
                        "value": dpg.get_value(item),
                    }
                if _type == "window" or _type == "drawlist":
                    layout_data[item] = {
                        "size": dpg.get_item_rect_size(item),
                    }

                if _type == "radiobutton":
                    layout_data[item] = {
                        "value": dpg.get_value(item),
                    }
                if _type == "treenode":
                    layout_data[item] = {
                        "value": dpg.get_value(item),
                    }
        # 获取视口的当前高度和宽度
        viewport_height = dpg.get_viewport_height()
        viewport_width = dpg.get_viewport_width()
        layout_data["viewport"] = {
            "height": viewport_height,
            "width": viewport_width,
        }

        # 将布局数据保存到JSON文件中
        with open(self.settings_file, "w") as file:
            json.dump(layout_data, file)
    
    def save_input_data(self, ip, input_tag):
        # 确保字典中的键存在
        if ip not in self.save_objects:
            self.save_objects[ip] = {}
        # 获取输入值并保存到字典
        self.save_objects[ip][input_tag] = dpg.get_value(input_tag)
        # 持久化数据到文件
        with open(self.input_data_file, "w") as file:
            json.dump(self.save_objects, file)
            
            
            
    def load_input_data(self,ip,input_tag):
        device_data = None
        with open(self.input_data_file, "r") as file:
                device_data = json.load(file)
        if dpg.does_alias_exist(input_tag):
            if device_data[ip].get(input_tag):
                dpg.set_value(input_tag,device_data[ip][input_tag])

    def get_device_name (self,ip):
        name = self.get_device_input_msg(ip,"rightmenu_rename_input")
        name = name if name else ""
        return name
    def get_device_input_msg(self,ip,input_tag):
        with open(self.input_data_file, "r") as file:
            device_data = json.load(file)
        return device_data[ip].get(input_tag)
                
    def get_window_size(self,tag):
        try:
            with open(self.settings_file, "r") as file:
                layout_data = json.load(file)
            for item, properties in layout_data.items():
                if item == tag:
                    return properties["size"]
        except:
            pass
        return [0, 0]

    def load_layout(self):
        # 从文件中加载布局设置
        try:
            with open(self.settings_file, "r") as file:
                layout_data = json.load(file)

            for item, properties in layout_data.items():
                # 设置视口的高度和宽度
                if item == "viewport":
                    dpg.set_viewport_height(properties["height"])
                    dpg.set_viewport_width(properties["width"])
                # 如果项目存在，设置其值
                if dpg.does_item_exist(item):
                    # 如果项目是复选框类型，设置之前保存的值
                    type = item.split("_")[-1]
                    if type == "checkbox":
                        dpg.set_value(item, properties["value"])
                    if type == "radiobutton":
                        dpg.set_value(item, properties["value"])
                    if type == "treenode":
                        dpg.set_value(item, properties["value"])
                    # 如果项目有回调函数，尝试执行回调函数
                    func = dpg.get_item_callback(item)
                    if func:
                        try:
                            func()
                        except Exception as e:
                            print(f"Error while executing callback for {item}: {e}")

            print("Layout loaded")
        except FileNotFoundError:
            print("No layout settings found")
