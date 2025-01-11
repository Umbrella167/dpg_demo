import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title=f"Test - {dpg.get_dearpygui_version()}", width=500, height=400)

dpg.setup_dearpygui()

# Zoom factor and initial scale
zoom_factor = 1.1
scale = 1.0
scale_matrix = []
# Callback function for mouse wheel event

with dpg.window(pos=(0, 30), width=500, height=350):
    dpg.add_button(label="Drag me!")
    with dpg.drag_payload(parent=dpg.last_item()):
        dpg.add_text("A new node")

    node_editor = dpg.generate_uuid()

    def on_drop():
        pos = dpg.get_mouse_pos(local=True)
        ref_node = dpg.get_item_children(node_editor, slot=1)[0]
        ref_screen_pos = dpg.get_item_rect_min(ref_node)
        ref_grid_pos = dpg.get_item_pos(ref_node)
        NODE_PADDING = (18, 18)
        pos[0] = pos[0] - (ref_screen_pos[0] - NODE_PADDING[0]) + ref_grid_pos[0]
        pos[1] = pos[1] - (ref_screen_pos[1] - NODE_PADDING[1]) + ref_grid_pos[1]
        with dpg.node(label="PI", pos=pos, parent=node_editor):
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_text(f"\n\n\n         PI         \n\n")

    with dpg.group(drop_callback=on_drop):
        with dpg.node_editor(tag=node_editor,
                             minimap=True,
                             minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,tracked=True,track_offset=0.5,show=False):

            with dpg.node(label="A real node", pos=[50, 30]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                    pass

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()