import dearpygui.dearpygui as dpg
import BASE.FunctionData as data
import BASE.Utils as utils
# 保存页面布局
def save_callback(sender, app_data, user_data):
    dpg.save_init_file("dpg_layout.ini")

# 返回鼠标点击位置
def get_mouse_click_coordinates(sender, app_data):
    x, y = dpg.get_mouse_pos()
    print(f"Mouse clicked at: ({x}, {y})")

def draw_node(name):
    pos = dpg.get_mouse_pos(local=False)
    ref_node = dpg.get_item_children("node_editor", slot=1)[0]
    ref_screen_pos = dpg.get_item_rect_min(ref_node)
    NODE_PADDING = (18, 18)
    pos[0] = pos[0] - (ref_screen_pos[0] - NODE_PADDING[0])
    pos[1] = pos[1] - (ref_screen_pos[1] - NODE_PADDING[1])
    node_name = data.select_node_button_name
    UID = dpg.generate_uuid()
    with dpg.node(label=data.select_node_button_name, pos=pos, parent="node_editor",tag = str(node_name) + "/" + "FUNCTION" + "/" + str(UID)):
        for param in data.NodeData[node_name]["INPUT"]:
                param_name = param["param_name"]
                param_type = param["param_type"]
                UID = dpg.generate_uuid()
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input,tag=str(param_type) + "/" +  "INPUT" + "/" + str(UID)):
                    dpg.add_text(f"{ param_name }  -> { param_type }")
                    
        out_put_name = data.NodeData[node_name]["OUTPUT"]
        if out_put_name:
            UID = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output,tag=str(out_put_name) + "/" + "OUTPUT" + "/" + str(UID)):
                dpg.add_text("Result:")
                dpg.add_input_text(width=150)


def set_select_node_name(user_data):
    data.select_node_button_name = user_data

# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    if app_data[1] not in data.link_output:
        data.link_output.append(app_data[1])
        line = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        
        data.line_tag[str(line)] = [app_data[0], app_data[1]]
    node_befor = dpg.get_item_children(dpg.get_item_alias(dpg.get_item_parent(app_data[0])), 1)  # 获取节点的所有属性
    node_after = dpg.get_item_children(dpg.get_item_alias(dpg.get_item_parent(app_data[1])), 1)  # 获取节点的所有属性
    connect_count = 0
    for befor in node_befor:
        print(dpg.get_item_alias(befor))
    for after in node_after:
        print(dpg.get_item_alias(after))


def delink_callback(sender, app_data):
    # app_data -> link_id
    data.link_output.remove(data.line_tag[str(app_data)][1])
    line_tag = {}
    dpg.delete_item(app_data)

