import UI.Ui as ui
import Object.Object as obj

def loop():
    pass

if __name__ == '__main__':
    SIZE_3D=(1200,900)
    SIZE_2D=(1800,1200)
    data = ui.ShareData()
    CORE = obj.DrawCore(SIZE_3D,SIZE_2D=SIZE_2D)
    UI = ui.UI(data)
    data.ui_loop_hook["DRAW_2D"]["func"] = CORE.update_2D
    data.ui_loop_hook["DRAW_3D"]["func"] = CORE.update_3D
    # UI.create_context()
    UI.create_texture(SIZE_3D,SIZE_2D)
    UI.create_viewport()
    UI.show_ui()
    UI.run_loop(loop)