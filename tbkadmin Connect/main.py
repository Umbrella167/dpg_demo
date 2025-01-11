#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import UI.Ui as ui
import dearpygui.dearpygui as dpg
import BASE.TBKApi as tbkapi

dpg.create_context()
tbkapi = tbkapi.TBKAPI()
ui_data = ui.UiData()


def get_device_info():
    device_table = [
        {"ip": "192.168.31.11", "status": "running", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.12", "status": "running", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.13", "status": "stopped", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.14", "status": "stopped", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.15", "status": "unknown", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.16", "status": "unknown", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.166", "status": "unknown", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.17", "status": "unknown", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.18", "status": "unknown", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.19", "status": "unknown", "is_current": False, "in_cluster": False},
        {"ip": "192.168.31.10", "status": "running", "is_current": True, "in_cluster": True},
    ]
    return device_table

def loop():
    device_table = get_device_info()
    UI.update_draw_window(device_table)

if __name__ == "__main__":
    UI = ui.UI(ui_data, tbkapi)
    UI._theme.set_theme("Dark")
    UI._theme.set_font(20)
    UI.create_viewport()
    UI.create_draw_window()
    ## 初始化需要
    device_table = get_device_info()
    UI._drawobj.draw_init(device_table)
    
    dpg.set_primary_window("draw_window", True)
    UI.show_ui()
    UI.run_loop(loop)
