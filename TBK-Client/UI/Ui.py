import dearpygui.dearpygui as dpg
import BASE.TBKApi as tbkapi
import UI.Theme as theme
import re
import traceback
from collections import deque
import UI.LayoutManager as LayoutManager
import BASE.Utils as utils
from contextlib import contextmanager
from typing import Generator, Union
import tbkpy._core as tbkpy

class UiData:
    
    def __init__(self):
        self.layout_manager = LayoutManager.LayoutManager()
        self.intname = [
            "int",
            "int32",
            "int64",
            "int16",
            "int8",
            "uint",
            "uint32",
            "uint64",
            "uint16",
            "uint8",
            "整形",
            "整数形",
        ]
        self.floatname = [
            "float",
            "double",
            "float32",
            "float64",
            "浮点",
            "浮点数",
            "浮点型",
            "单浮点",
            "双浮点",
            "单精度",
            "双精度",
        ]
        self.boolname = ["bool", "布尔", "布尔值"]
        self.enumname = ["enum", "枚举", "list", "列表"]


class DiyComponents:
    def __init__(self, data: UiData, param: tbkapi.TBKAPI):
        self._param = param
        self._data = data

    def set_input_color(self, change_item, color):
        with dpg.theme() as theme_id:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, (0, 0, 0, 0), category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgHovered,
                    (0, 0, 0, 0),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgActive,
                    (0, 0, 0, 0),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(dpg.mvThemeCol_Text, color)

        try:
            dpg.bind_item_theme(item=change_item, theme=theme_id)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            file_name, line_number, func_name, text = tb[-1]
            print(
                f"ERROR(bind_item_theme)：\n    Item:{change_item}\n    File:{file_name}\n    Line:{line_number}\n    Function:{func_name}\n    Text:{text}"
            )

    def add_input(self, _type, tag, default_value, max_value, min_value, step):

        if _type == "int":

            # dpg.add_drag_int(clamped = True,tag=self.__tag,default_value=value,width=-1,max_value=int(self.max),min_value=int(self.min),speed=int(self.step),callback=self.change_param_input_callback)
            with dpg.group():
                dpg.add_drag_int(
                    tag=tag,
                    clamped=True,
                    width=-1,
                    default_value=int(default_value),
                    max_value=int(max_value),
                    min_value=int(min_value),
                    speed=int(step),
                )
                dpg.add_slider_int(height=10, width=-1)
    
    class TABLETREE:
        def __init__(self):
            self.param_tag = ""
            pass

        def on_row_clicked(self,sender, value, user_data):
            # Make sure it happens quickly and without flickering
            with dpg.mutex():
                # We don't want to highlight the selectable as "selected"
                dpg.set_value(sender, False)

                table, row = user_data
                root_level, node = dpg.get_item_user_data(row)

                # First of all let's toggle the node's "expanded" status
                is_expanded = not dpg.get_value(node)
                dpg.set_value(node, is_expanded)
                # All children *beyond* this level (but not on this level) will be hidden
                hide_level = 10000 if is_expanded else root_level

                # Now manage the visibility of all the children as necessary
                rows = dpg.get_item_children(table, slot=1)
                root_idx = rows.index(row)
                # We don't want to look at rows preceding our current "root" node
                rows = rows[root_idx + 1:]
                for child_row in rows:

                    child_level, child_node = dpg.get_item_user_data(child_row)
                    if child_level <= root_level:
                        break

                    if child_level > hide_level:
                        dpg.hide_item(child_row)
                    else:
                        dpg.show_item(child_row)
                        hide_level = 10000 if dpg.get_value(
                            child_node) else child_level

        @contextmanager
        def table_tree_node(self,*cells: str, leaf: bool = False,tag = 0) -> Generator[Union[int, str], None, None]:
            table = dpg.top_container_stack()
            cur_level = dpg.get_item_user_data(table) or 0
    
            node = dpg.generate_uuid()
            INDENT_STEP = 30
            with dpg.table_row(user_data=(cur_level, node)) as row:
                with dpg.group(horizontal=True, horizontal_spacing=0):
                    span_columns = True if cells[1] == "--" else False
                    dpg.add_selectable(span_columns=span_columns,
                                    callback=self.on_row_clicked, user_data=(table, row))
                    dpg.add_tree_node(
                        tag=node,
                        label=cells[0],
                        # indent=cur_level*INDENT_STEP,
                        selectable=False,
                        leaf=leaf,
                        default_open=True)

                for label in cells[1:]:
                    # print(label)
                    dpg.add_text(label,tag=tag)
            try:
                dpg.set_item_user_data(table, cur_level + 1)
                yield node
            finally:
                dpg.set_item_user_data(table, cur_level)

        def add_table_tree_leaf(self,*cells: str,tag = 0) -> Union[int, str]:
            with self.table_tree_node(*cells, leaf=True,tag = tag) as node:
                pass
            return node
        def build_dpg_tree(self,tree):
            for key, value in tree.items():
                if isinstance(value, dict):
                    if 'info' in value and 'type' in value and 'value' in value:
                        print(value['info'], value['type'], value['value'])
                        self.add_table_tree_leaf(key, value['info'], value['type'], value['value'])
                    else:
                        with self.table_tree_node(key, "--", "--", "--"):
                            self.build_dpg_tree(value)
                            # self.param_tag = self.param_tag + "/" + value
                else:
                    print(key)
                    
                    self.add_table_tree_leaf(key, "--", "--", str(value))

    class param_input:
        
        def __init__(self, outer_instance, data: UiData, param: tbkapi.TBKAPI) -> None:
            self._outer_instance = outer_instance
            self.__tag = None
            self.__value = None
            self.__data = data
            self.__param = param
            self.__type = None
            self.__info = None
            self.__parent = None
            self.min = None
            self.max = None
            self.enum = []
            self.step = 1.0

        def get_limit(self):
            if self.__info:
                self.enum = self.__info
                pattern = r"\[(.*?)\]"
                match = re.search(pattern, self.__info)
                if match:
                    content = match.group(1).split(",")
                    if len(content) == 3:
                        self.min = content[0]
                        self.max = content[1]
                        self.step = content[2]
                    elif len(content) == 2:
                        self.min = content[0]
                        self.max = content[1]
                    self.enum = content
                    
        # 创建主题

        def create_theme(self):
            with dpg.theme() as theme_id:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBg,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Core,
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBgHovered,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Core,
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBgActive,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Core,
                    )
            return theme_id

        def new_input(self, tag, value: str, type="str", info=None, parent=0):
            self.__init_input(tag=tag, value=value, type=type, info=info, parent=parent)
            self.get_limit()
            theme_id = self.create_theme()
            # if self.__type in self.__data.intname:
            if any(item in self.__type for item in self.__data.intname):

                self.create_input_int()
            # elif self.__type in self.__data.floatname:
            elif any(item in self.__type for item in self.__data.floatname):

                self.create_input_float()
            # elif self.__type in self.__data.boolname:
            elif any(item in self.__type for item in self.__data.boolname):

                self.create_check_box()
            # elif self.__type in self.__data.enumname:
            elif any(item in self.__type for item in self.__data.enumname):
                self.create_enum()
            else:
                self.create_input_text()
            dpg.bind_item_theme(item=tag, theme=theme_id)

        def __init_input(self, tag, value: str, type="str", info=None, parent=0):
            self.__value = value
            try:
                self.__type = type.lower()
            except:
                self.__type = type
            self.__info = info
            self.__parent = parent
            self.__tag = tag

        def change_param_input_callback(self, sender, app_data):
            split_data = sender.split("_")[-1]
            end = split_data[0]
            head = sender[: -1 * (len(split_data) + 1)]
            param = f"{head}/__{end}__"
            value = "None" if app_data == "" else app_data
            if value == "None" or value == "":
                dpg.set_value(sender, value)
                self._outer_instance.set_input_color(sender, [255, 0, 0, 255])
            self.__param.put_param(param, str(value))

        # 正整数输入框
        def create_input_int(self):
            try:
                value = int(self.__value)
            except:
                value = 0
            if self.max and self.min:
                print(self.max, self.min)
                # self._outer_instance.add_input( "int",self.__tag,50,100,0,10)
                # dpg.add_drag_int(
                #     clamped=True,
                #     tag=self.__tag,
                #     default_value=value,
                #     width=-1,
                #     max_value=int(self.max),
                #     min_value=int(self.min),
                #     speed=int(self.step),
                #     callback=self.change_param_input_callback,
                # )
                dpg.add_slider_int(
                    clamped=True,
                    tag=self.__tag,
                    default_value=value,
                    width=-1,
                    max_value=int(self.max),
                    min_value=int(self.min),
                    # speed=int(self.step),
                    callback=self.change_param_input_callback,
                )
                    
            else:
                dpg.add_input_int(
                    tag=self.__tag,
                    default_value=value,
                    width=-1,
                    callback=self.change_param_input_callback,
                )

        # 浮点数输入框

        def create_input_float(self):
            try:
                value = float(self.__value)
            except:
                value = 0
            if self.max and self.min:
                dpg.add_drag_double(
                    clamped=True,
                    tag=self.__tag,
                    default_value=value,
                    width=-1,
                    max_value=float(self.max),
                    min_value=float(self.min),
                    speed=float(self.step),
                    callback=self.change_param_input_callback,
                )
            else:
                dpg.add_input_double(tag=self.__tag, default_value=value, width=-1)

        # 文本输入框

        def create_input_text(self):
            dpg.add_input_text(
                tag=self.__tag,
                default_value=self.__value,
                width=-1,
                callback=self.change_param_input_callback,
            )

        # 布尔输入框

        def create_check_box(self):
            def checkbos_callbak(sender, app_data):
                value = app_data
                split_data = sender.split("_")[-1]
                end = split_data[0]
                head = sender[: -1 * (len(split_data) + 1)]
                param = f"{head}/__{end}__"
                dpg.configure_item(sender, label=str(value))
                self.__param.put_param(param, str(value))

            try:
                value = int(self.__value)
                if value > 0:
                    value = True
                else:
                    value = False
            except:
                try:
                    value = self.__value.lower()
                    value = True if value == "true" else False
                except:
                    value = False
            with dpg.group():
                dpg.add_checkbox(
                    tag=self.__tag,
                    default_value=value,
                    label=str(value),
                    callback=checkbos_callbak,
                )

        # 枚举输入框

        def create_enum(self):
            enum = self.enum
            try:
                split_choose = self.enum.split("|")
                if len(split_choose) > 1:
                    enum = []
                    for item in split_choose:
                        enum.append(item)
                else:
                    enum = []
            except:
                pass 
            if enum:
                dpg.add_combo(
                    tag=self.__tag,
                    items=enum,
                    width=-1,
                    default_value=self.__value,
                    callback=self.change_param_input_callback,
                )
            else:
                self.create_input_text()

class CallBack:
    def __init__(self, data: UiData, component: DiyComponents):
        self._data = data
        self._layout_manager = self._data.layout_manager
        self._component = component

    def on_key_release(self, sender, app_data):
        if dpg.is_key_down(dpg.mvKey_Control) and app_data == dpg.mvKey_S:
            self._layout_manager.save_layout()

    def check_message(self, sender, app_data,user_data):
        msg = user_data[0]
        text_tag = user_data[1]
        def msg_callback(msg):
            if msg:
                print(msg)
                # dpg.set_value(text_tag,msg)
        if app_data :
            suber = tbkpy.Subscriber("puber_test","test_int",msg_callback)
        else:
            suber = None
        
class UI:
    def __init__(self, data: UiData, tbkapi: tbkapi.TBKAPI):
        self._data = data
        self._tbkapi = tbkapi
        self._layout_manager = self._data.layout_manager
        self._diycomponents = DiyComponents(self._data, self._tbkapi)
        self._callback = CallBack(self._data, self._diycomponents)
        self._theme = theme
        self.maxlen = 5
        self.table_change_list = deque(maxlen=self.maxlen)

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
        dpg.configure_app(
            docking=True,
            docking_space=True,
            init_file="dpg_layout.ini",
            load_init_file=True,
        )
        dpg.create_viewport(title="TBK-ParamManager", width=1920, height=1080)
    
    def create_param_window(self):
        
        with dpg.window(
            tag="param_window", label="Param", no_close=True, no_collapse=True
        ):
            self.create_param_table()

    def create_param_table(self):

        dpg.delete_item("param_window", children_only=True)
        # 创建新的表格
        with dpg.table(
            header_row=True,
            policy=dpg.mvTable_SizingFixedFit,
            row_background=True,
            reorderable=True,
            resizable=True,
            no_host_extendX=False,
            hideable=True,
            borders_innerV=True,
            delay_search=True,
            borders_outerV=True,
            borders_innerH=True,
            borders_outerH=True,
            parent="param_window",
        ) as table_tag:
        # 添加表格列
            dpg.add_table_column(label="Param", width_fixed=True, parent=table_tag)
            dpg.add_table_column(label="Info", width_fixed=True, parent=table_tag)
            dpg.add_table_column(label="Type", width_fixed=True, parent=table_tag)
            dpg.add_table_column(label="Value", width_fixed=True, parent=table_tag)
            # table_tree = self._diycomponents.TABLETREE()
            # table_tree.build_dpg_tree(self._tbkapi.param_tree)
            # 添加表格行和内容
            for row_index, (param, value) in enumerate(self._tbkapi.param_data.items()):
                with dpg.table_row(parent=table_tag, tag=param):
                    dpg.add_text(default_value=param, tag=param + "_param")
                    _info = value["info"]
                    _type = value["type"]
                    for item in value:
                        if item == "value":
                            tag = param + "_" + item
                            self._diycomponents.param_input(
                                outer_instance=self._diycomponents,
                                data=self._data,
                                param=self._tbkapi,
                            ).new_input(
                                tag=tag,
                                value=value[item],
                                type=_type,
                                info=_info,
                                parent=param,
                            )
                            # 如果值是空的,那么设置为红色
                            if value[item] == "None":
                                self._diycomponents.set_input_color(tag, [255, 0, 0, 255])
                        else:
                            dpg.add_text(default_value=value[item], tag=param + "_" + item)

        # 更新 参数界面

    def update_param_data(self):
        change_param_data = self._tbkapi.param_change_data
        is_change = self._tbkapi.param_is_change
        if is_change:
            for change_type in change_param_data:
                if change_type == "added":
                    pass
                elif change_type == "removed":
                    pass
                elif change_type == "modified":
                    for param, _ in change_param_data[change_type].items():
                        attribute = dict(_["modified"].items())
                        attribute_type = list(attribute.keys())[0]
                        attribute_value = list(attribute.values())[0][0]
                        _type = self._tbkapi.param_data[param]["type"]
                        try:
                            _type = _type.lower()
                        except:
                            pass
                        # 获取参数类型
                        if attribute_type == "value":
                            # int类型
                            if _type in self._data.intname:
                                try:
                                    attribute_value = int(attribute_value)
                                except:
                                    attribute_value = 0
                            # float类型
                            elif _type in self._data.floatname:
                                try:
                                    attribute_value = float(attribute_value)
                                except:
                                    attribute_value = 0.0
                            # bool类型
                            elif _type in self._data.boolname:
                                attribute_value = attribute_value.lower()
                                attribute_value = (
                                    True if attribute_value == "true" else False
                                )
                            # str类型
                            else:
                                attribute_value = str(attribute_value)
                        else:
                            self.create_param_table()
                        try:
                            dpg.set_value(param + "_" + attribute_type, attribute_value)
                        except Exception as e:
                            print(
                                f"ERROR(set_value): \n    Itme:{param}_{attribute_type}\n"
                            )
                        self.table_change_list.append(param + "_" + attribute_type)

            # 逐渐改变颜色
            change_list_len = len(self.table_change_list)
            try:
                for i in range(change_list_len):
                    param = self.table_change_list[i]
                    if dpg.get_value(param) != "None":
                        self._diycomponents.set_input_color(
                            param, [0, 255 // (change_list_len - i), 0, 255]
                        )
                        if i == 0 and change_list_len == self.maxlen:
                            self._diycomponents.set_input_color(
                                param, [255, 255, 255, 255]
                            )
            except Exception as e:
                tb = traceback.extract_tb(e.__traceback__)
                file_name, line_number, func_name, text = tb[-1]
                print(
                    f"ERROR(set_input_color):\n    Item:{param} \n    File:{file_name}\n    Line:{line_number}\n    Function:{func_name}\n    Text:{text}"
                )

    def create_global_handler(self):
        with dpg.handler_registry() as global_hander:
            dpg.add_key_release_handler(callback=self._callback.on_key_release)
        # with dpg.item_handler_registry() as item_handler_registry:
        #     dpg.add_item_resize_handler(callback=self._callback.drawer_window_resize_callback)
        # dpg.bind_item_handler_registry("drawer_window", item_handler_registry)

    def create_message_window(self):
        with dpg.window(label="Message", tag="message_window"):
            self.create_message_list()
        
    def create_message_list(self):
        message_data = self._tbkapi.message_data
        pubs = message_data["pubs"]
        with dpg.collapsing_header(label="Message List", tag = f"{dpg.generate_uuid()}_treenode"):
            item = []
            message_tree = utils.build_message_tree(pubs)
            for puuid, node_name in message_tree.items():
                for theme_name, node_msgs in node_name.items():
                    with dpg.tree_node(label=f"{theme_name}({puuid})",tag = f"{dpg.generate_uuid()}_treenode"):
                        for publisher, messages in node_msgs.items():
                            with dpg.tree_node(label=publisher,tag= f"{dpg.generate_uuid()}_treenode"):
                                for msg in messages:
                                    with dpg.group(tag=f"{dpg.generate_uuid()}_group",horizontal=True):
                                        uuid = dpg.generate_uuid()
                                        dpg.add_checkbox(label=msg,tag=f"{uuid}_checkbox",callback=self._callback.check_message,user_data=(msg,uuid))
                                        dpg.add_spacer(width=80)
                                        dpg.add_text(tag=f"{uuid}_text",default_value="")
                                        
    def create_message_view(self):
        with dpg.window(label="Message View", tag="message_view"):
            with dpg.drawlist():
                pass

        # puuid -> node_name -> name -> msg_name
        
    def update_message_list(self):
        change_message_data = self._tbkapi.message_change_data
        is_change = self._tbkapi.message_is_change
        if is_change:
            for change_type in change_message_data:
                if change_type == "added":
                    pass
                elif change_type == "removed":
                    pass
                elif change_type == "modified":
                    pass

    # def create_message_draw_window(self):