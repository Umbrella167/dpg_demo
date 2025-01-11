import os
import time
import BASE.Utils as utils
import threading
import BASE.FunctionData as data
Observer_thread = threading.Thread(target=lambda:utils.monitor_directory("NODE"), daemon=True)
Observer_thread.start()
while True:
    time.sleep(0.5)
    if data.NodeData:
        try:
            for node in data.NodeData:
                res = data.NodeData[node]["FUNC"].main(1)
                print(f"NodeName: {node},  res:{res}")
        except:
            pass
