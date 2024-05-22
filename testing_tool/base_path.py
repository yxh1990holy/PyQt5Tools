import os

# 项目根目录
_root_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# 日志路径
log_path = os.path.join(_root_path, 'logs/')
if not os.path.exists(log_path):
    os.makedirs(log_path)
