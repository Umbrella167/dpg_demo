"""dearpyguiのリアルタイムプロット例

参考URL
https://dearpygui.readthedocs.io/en/latest/documentation/render-loop.html
https://dearpygui.readthedocs.io/en/latest/documentation/plots.html#updating-series-data
https://github.com/hoffstadt/DearPyGui/issues/303
"""
import dearpygui.dearpygui as dpg
import numpy as np

# ################# プロットデータ作成 #################
data_len: int = 100
x_data: np.ndarray = np.linspace(0, data_len - 1, data_len)
y_data = np.empty(data_len)
y_data[:] = np.nan

# ################# 時間経過判定用　#################
elapsed_time: float = 0.0
interval: float = 0.05


def update_array(data: np.ndarray) -> np.ndarray:
    """np.ndarrayの末尾に新しい値を追加

    Parameters
    ----------
    data: np.ndarray
        データ入力するnp.ndarray

    Returns
    -------
    result: np.ndarray
        追加後のデータ
    """

    new_y = np.random.randint(0, 100)  # 追加する値
    data[:data_len - 1] = data[1:data_len]
    data[data_len - 1] = new_y

    return data


def plot_callback() -> None:
    """データをプロットする"""

    global x_data, y_data
    y_data = update_array(y_data)

    # 第1引数は値を入力したいアイテムのtag (= dpg.add_line_series(tag='line'))
    dpg.set_value('line', [x_data, y_data])


# ##################### 描画設定 #####################
dpg.create_context()
with dpg.window(label='Plot window', width=-1, height=-1):
    with dpg.plot(label=f"Real time plot \n interval: {interval} sec", width=400, height=250):
        pass
        # dpg.add_plot_legend()  # 凡例追加
        # # x, y軸追加
        # dpg.add_plot_axis(dpg.mvXAxis, label='x', tag='xaxis')
        # dpg.add_plot_axis(dpg.mvYAxis, label='y', tag='yaxis')
        # # データ線追加, 親は最後に追加したアイテム (=y軸)
        # dpg.add_line_series(x_data, y_data, label='data', parent=dpg.last_item(), tag='line')
        



dpg.create_viewport(title='Plot view port', width=420, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.start_dearpygui()
dpg.destroy_context()

# while dpg.is_dearpygui_running():
#     total_time = dpg.get_total_time()  # 画面が開いてからのトータル時間 (秒)
#     # interval 秒経過したらグラフ更新
#     if total_time - elapsed_time >= interval:
#         elapsed_time = total_time
#         plot_callback()
#     dpg.render_dearpygui_frame()

dpg.destroy_context()

