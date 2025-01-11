import Logger as logger
import VISION.vision_detection_pb2 as detection
from VISION.vision_detection_pb2 import Vision_DetectionBall
import log_pb2

# log = logger.Logger()
# for i in range(30):
#     res = 0
#     if i > 10:
#         res = 10
#     ball = Vision_DetectionBall()
#     ball.vel_x = res
#     ball.vel_y = res
#     ball.area = res
#     ball.x = res
#     ball.y = res
#     ball.height = res
#     ball.ball_state = res
#     ball.last_touch = res
#     ball.valid = True
#     ball.raw_x = res
#     ball.raw_y = res
#     ball.chip_predict_x = res
#     ball.chip_predict_y = res
#     ball.SerializeToString()
#     log.log(message_data=ball,message_type=log_pb2.MessageType.MESSAGE_PROTO,energy_saving=True)

log_player = logger.LogPlayer("/home/umbrella/桌面/dpg demo/dpg_ssl_demo/logs/Rec_2024-08-31_16-12-17-642219.log")

msg = log_player.read_log()

print(msg)
