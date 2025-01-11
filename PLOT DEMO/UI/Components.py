import dearpygui.dearpygui as dpg
import UI.Language.Language as language
import UI.Theme as theme
import BASE.CallBack as callback
import BASE.DataFactory as data

label = language.languages[theme.current_language]
class PLOT: 
    def line(data_x,data_y,height,width):
        with dpg.plot(height=height, width=width):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="TimeShape",tag="xaxis")
            dpg.add_plot_axis(dpg.mvYAxis, label="y",tag = "yaxis")
            dpg.add_line_series(data_x, data_y, parent="yaxis",tag="line_series")
# 顶部菜单
def top_menu():
    # 创建菜单栏
    with dpg.menu_bar():
        # 视图菜单
        with dpg.menu(label=label["view_menu"],tag = "view_menu"):
            # 主题
            with dpg.menu(label=label["theme_menu"],tag = "theme_menu"):
                dpg.add_menu_item(label=label["dark_theme"], tag = "dark_theme",callback=lambda: theme.set_theme("Dark"))
                dpg.add_menu_item(label=label["light_theme"], tag = "light_theme",callback=lambda: theme.set_theme("Light"))
            # 语言
            with dpg.menu(label=label["language_label"],tag = "language_label"):
                dpg.add_menu_item(label=label["chineseS_menu"], tag = "chineseS_menu",callback=lambda: theme.choose_lanuage("zh"))
                dpg.add_menu_item(label=label["english_menu"], tag = "english_menu",callback=lambda: theme.choose_lanuage("en"))



def viewport_group(data_x,data_y):
    PLOT.line(data_x,data_y)
# 边菜单
def side_menu():
    # 左侧边栏

    with dpg.child_window(tag="side_menu",width=200,pos=(10,30),autosize_y=True, show=True):
        with dpg.group(tag="not_found"):
            dpg.add_text("Serial port not found！",color=(255,0,0))
        with dpg.group(tag = "found_port",show=False):
            dpg.add_text("Baud Rate:",tag="baudrate_text")
            dpg.add_combo(items=["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"],default_value=str(data.burt_rate),tag="baud_rate_combox",callback=callback.rade_combo)
            dpg.add_text("Port:",tag="port_text")
            dpg.add_listbox(items=[], tag="port_list",width=-1)
        
        # with dpg.collapsing_header(label="Port"):
        #     with dpg.group(horizontal=True):
        #         dpg.add_text("Port:")
        # dpg.add_button(label="T_ViewPort",width=175,callback=lambda: callback.show_viewport())
        # dpg.add_button(label="T_HOME",width=175,callback=lambda: callback.show_home())


    # 右主内容
    with dpg.child_window(tag="side_menu_right", autosize_x=True,autosize_y=True,pos=(215,30),show=True,drop_callback=callback.add_plot_time_shape,payload_type='Drag&Drop'):

        with dpg.group(tag="viewport_group"):

            PLOT.line([0,1,2,3],[0,1,2,3],-1,-1)

        with dpg.group(tag="home_group",show=False):
            dpg.add_text("HOME")

# 画图组件窗口
def plot_components_window():
    with dpg.child_window(label="T_console_window",tag="plot_components_window"):
            with dpg.collapsing_header(label="Normal"):
                with dpg.group(horizontal=True):
                    with dpg.plot(height=200, width=200,label="T_Time_Shape",tag="T_Time_Shape") as plot:
                        dpg.add_drag_payload(parent=dpg.last_item(), payload_type='Drag&Drop')
                        pass
                    with dpg.plot(height=200, width=200,label="T_2D",tag="T_2D") as plot:
                        dpg.add_drag_payload(parent=dpg.last_item(), payload_type='Drag&Drop')
                        pass

# 控制台窗口
def console_window(): 
    with dpg.child_window(label="T_console_window",tag="console_window"):
            dpg.add_text("Console:")
            dpg.add_input_text(multiline=True,width=-1, height=-1)

# 底部菜单
def bottom_menu():
    with dpg.window(label="T_console_window",tag="console_windosdw"):
        with dpg.tab_bar():
            with dpg.tab(label="T_Console"):
                console_window()
            with dpg.tab(label="T_Components"):
                plot_components_window()
