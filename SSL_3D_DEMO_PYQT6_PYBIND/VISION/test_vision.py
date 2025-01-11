import vision_module

vm = vision_module.VisionModule()

while True:
    debug_dict = vm.get_detection_dict()
    print(debug_dict)