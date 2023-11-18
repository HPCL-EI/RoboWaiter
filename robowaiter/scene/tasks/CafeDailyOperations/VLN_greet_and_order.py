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

        self.scene_flag = 1
        self.st1 = 3
        self.st2 = self.st1 + 30

        self.new_event_list = [

            # 场景1：带小女孩找阳光下的空位
            (3, self.add_walker, (5, 230, 1200)),
            (3, self.control_walker, (0, False, 200, 60, 520, 0)),
            (10, self.customer_say, (0, "早上好呀，我想找个能晒太阳的地方。")),
            (10, self.customer_say, (0,"可以带我过去嘛？")),
            (20, self.control_walker, (0, False, 50, 140, 1200, 180)), # 小女孩站在了 BrightTable1 旁边就餐啦

            # 场景2：有个胖胖男人点单交流并要咖啡，帮他送去角落的桌子
            # (3, self.add_walker, (5, 230, 1200)), # 小女孩
            # 上述准备
            (self.st2, self.add_walker, (26, 60,-140)),
            (self.st2, self.add_walker, (10, -80, -180,-45)),  # （-150 -250）
            (self.st2, self.control_walker, (1, False, 100, 70, 520, 0)), #3
            (self.st2+15, self.customer_say, (1, "你们这有什么饮料嘛？")), # 10
            (self.st2+15, self.customer_say, (1, "咖啡有哪些呢？")),# 10
            (self.st2+15+5, self.customer_say, (1,"来杯卡布奇诺吧，我在靠窗边的高脚桌那。")), # 15
            (self.st2+15+5+5, self.control_walkers_and_say, ([[[1, False, 100, -30, -200, -90, "麻烦啦！"]]])), # 20 胖胖男到了 BrightTable6




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


        if self.scene_flag == 1:
            # 如果机器人不在 吧台
            if self.walker_followed:
                return
            end = [self.status.location.X, self.status.location.Y]
            if end[1]>=600 or end[1]<=450 or end[0]>=250:
            # if int(self.status.location.X)!=247 or  int(self.status.location.X)!=520:
                self.walker_followed = True
                self.control_walkers_and_say([[0,False,150,end[0],end[1],90,"wd！"]])
                self.scene_flag += 1

        pass

if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLM(robot)
    task.reset()
    task.run()
