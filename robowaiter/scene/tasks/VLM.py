"""
视觉语言操作
机器人根据指令人的指令调节空调，自主探索环境导航到目标点，通过手臂的运动规划能力操作空调，比如开关按钮、调温按钮、显示面板
"""

import time
from robowaiter.scene.scene import Scene

class SceneVLM(Scene):
    def __init__(self, robot):
        super().__init__(robot)

    def _reset(self):
        pass

    def _run(self, op_type=1):

        self.move_task_area(op_type)
        self.op_task_execute(op_type)

    def _step(self):
        pass