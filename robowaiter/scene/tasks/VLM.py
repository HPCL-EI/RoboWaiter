"""
视觉语言操作
机器人根据指令人的指令调节空调，自主探索环境导航到目标点，通过手臂的运动规划能力操作空调，比如开关按钮、调温按钮、显示面板
"""

import time
from robowaiter.scene.scene import Scene

class SceneVLM(Scene):
    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件， (事件发生的时间，事件函数)
        self.event_list = [
            (5, self.create_chat_event("测试VLM：做一杯咖啡")),
        ]

    def _reset(self):
        pass

    def _run(self, op_type=1):
        # 12个操作顺序测试
        # for i in range(1,13):
        #     if i<=10:
        #         self.move_task_area(i)
        #     self.op_task_execute(i)

        # if op_type<=10:
        #     self.move_task_area(op_type)
        # self.op_task_execute(op_type)
        pass
    
    def _step(self):
        pass
