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
        self.new_event_list = [
            (3, self.add_walker, (5, 230, 1200)),
            (5, self.control_walkers_and_say, ([[[0, False, 200, 60, 520, 0, "早上好呀，我想找个能晒太阳的地方。"]]])),# (0, 60, 520)),
            (6, self.customer_say, (0,"可以带我过去嘛？")),
        ]

    def _reset(self):
        self.gen_obj()
        # self.add_walkers([[47, 920]])
        pass

    def _run(self, op_type=10):
        # 一个行人从门口走到 吧台
        # 打招呼需要什么
        # 行人说 哪里有位置，想晒个太阳
        # 带领行人去有太阳的地方
        # 行人说 有点热
        # 好的，这就去开空调
        self.walker_followed = False
        pass
    
    def _step(self):


        # 如果机器人不在 吧台
        # if "At(Robot,Bar)" not in self.state['condition_set']:
        if self.walker_followed:
            return

        end = [self.status.location.X, self.status.location.Y]
        # print("end:",end)
        if end[1]>=600 or end[1]<=450 or end[0]>=250:
        # if int(self.status.location.X)!=247 or  int(self.status.location.X)!=520:
            self.walker_followed = True
            self.control_walkers_and_say([[0,False,300,end[0],end[1],90,"谢谢！"]])


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLM(robot)
    task.reset()
    task.run()
