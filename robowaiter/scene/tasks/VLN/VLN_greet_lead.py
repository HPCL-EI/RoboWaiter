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
            (2, self.customer_say, (0, "请问哪里有空位啊？")),
            (6, self.customer_say, (0, "我想坐高凳子。")),
            (6, self.customer_say, (0, "你带我去吧。")),
            (13, self.control_walker, (0, False,100, -250, 480,-90)),
            (-1, self.customer_say, (0, "谢谢你！这儿还不错！")),
        ]

    def _reset(self):
        self.gen_obj()
        self.add_walkers([
                [29, 60, 520], #顾客 0
                [23, 0, 220], #秃头老头子  1
                [0, -55, 150], #小男孩d走来走去 2
                [10, -55, 750], # 3
                [19, 70, -200],  #后门站着不动的 4
                [21, 65, 1000, -90], #大胖男占了一号桌 5
                [5, 230, 1200], #小女孩 6
                [26, -28, 0, 90] , #在设置一个在后门随机游走的 7
            # 设置为 26, 60, 0, 90]
                [31, 280, 1200, -45] # 8
             ])
        self.control_walker(2, True, 200, -55, 155, 90) #飞速奔跑的小男孩
        # self.control_walker(7, True, 80, -25, -150, 90)
        self.control_walker(5, True, 65, 995, 520, 90)
        self.control_walker(4, True, 65, 70, -200, 90)
        pass

    def _run(self):
        pass
    
    def _step(self):
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLM(robot)
    task.reset()
    task.run()
