"""
视觉语言操作
机器人根据指令人的指令调节空调，自主探索环境导航到目标点，通过手臂的运动规划能力操作空调，比如开关按钮、调温按钮、显示面板
"""

import time
from scene_utils import control

# control.init_world(1, 3)

scene = control.Scene(sceneID=0)

scene.reset()

# 空调操作
scene.walk_to(950, 1260, 90)  # 没法转向？
# todo: 手臂操作
time.sleep(5)
scene.walk_to(947, 1900, 0)

# 物品挪动
# todo: 视觉导航至目标点，操作手臂至可抓位置
"""
scene.grasp(1, your_objectID)
"""
# todo: 视觉导航至目标点，找准释放位置
"""
scene.release(1)
"""
