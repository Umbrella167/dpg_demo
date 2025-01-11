import dearpygui.dearpygui as dpg
import UI.Language.Language as language
import UI.Theme as theme
import BASE.CallBack as callback
import BASE.FunctionData as data

label = language.languages[theme.current_language]


def node_select_window():
    with dpg.window(label="NODE",tag="node_select"):
        pass
def node_editor_window():
    with dpg.group(drop_callback=callback.draw_node,tag="node_editor_group"):
        with dpg.node_editor(tag="node_editor",minimap=True,minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,tracked=True,track_offset=0.5,show=True,callback=callback.link_callback, delink_callback=callback.delink_callback):
            with dpg.node(label="",draggable=False):
                    pass

class NODE():
    def __init__(self) -> None:
        self.node = {}
    def add_node(self,node_data):
        for node in node_data:
            data_split =node_data[node]["PATH"].split("/")
            dir_name = data_split[1:-1][0]
            node_name = data_split[-1][:-3]
            if not dpg.does_item_exist(dir_name):
                dpg.add_collapsing_header(label=dir_name,parent="node_select",tag = dir_name)
            if not dpg.does_item_exist(node_name):
                dpg.add_button(label=node_name,parent=dir_name,tag = node_name,width=-1,height=30,drag_callback=callback.set_select_node_name,user_data=node_name)
                dpg.add_drag_payload(parent=dpg.last_item())
                dpg.add_text(node_name,parent=dpg.last_item())
            