import os
import glob
import time
import BASE.FunctionData as data
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib.util
import re
import inspect
from typing import get_type_hints


def get_file_name(input_string):
    # 使用正则表达式提取"/"和"."之间的内容
    pattern = r'/(?P<content>[^/\.]+)\.'
    matches = re.findall(pattern, input_string)
    return matches[0]

def list_py_files(directory):
    """列出指定目录下所有的 .py 文件"""
    # 使用 glob 模块匹配 .py 文件
    py_files = glob.glob(os.path.join(directory, '**', "*.py"), recursive=True)
    return py_files

class ChangeHandler(FileSystemEventHandler):
    """自定义事件处理程序，处理文件系统事件"""
    def __init__(self):
        super().__init__()
        self.changed = False

    def on_any_event(self, event):
        # 任何文件系统事件都会触发该方法
        if "__pycache__" not in event.src_path:
            self.changed = True

        
def monitor_directory(path):
    def lode_func():
        func_list = []
        PathList = list_py_files(path)
        for func in PathList:
            func_p = load_module_from_file(func)
            func_message = list_functions_in_module(func_p)
            node_name = get_file_name(func)
            for function in func_message:
                data.NodeData[node_name] = {
                "INPUT" :function["INPUT"],
                "OUTPUT":function["OUTPUT"],
                "FUNC":func_p
            }
        data.NodeList = func_list

    """监控指定目录"""
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        lode_func()
        while True:
            if event_handler.changed:
                lode_func()
                event_handler.changed = False  # 重置标志
            time.sleep(1.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def load_module_from_file(file_path):
    """从文件加载模块"""
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# func message get
def get_function_input_params(func):
    """获取函数的输入参数信息，包括名称和类型"""
    sig = inspect.signature(func)
    params_info = []
    type_hints = get_type_hints(func)  # 获取类型提示
    for param_name, param in sig.parameters.items():
        param_type = type_hints.get(param_name, None)  # 获取参数类型
        params_info.append({
            'param_name': param_name,
            'param_type': param_type
        })
    return params_info

def get_function_output_type(func):
    """获取函数的输出数据类型"""
    type_hints = get_type_hints(func)
    return type_hints.get('return', None)

def list_functions_in_module(module):
    """列出模块中的所有函数"""
    functions_info = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name == "main":
            input_params = get_function_input_params(obj)
            output_type = get_function_output_type(obj)
            functions_info.append({
                'NAME': name,
                'INPUT': input_params,
                'OUTPUT': output_type
            })
    return functions_info