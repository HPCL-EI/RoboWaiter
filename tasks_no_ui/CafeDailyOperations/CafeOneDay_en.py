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

        self.scene_flag = 2
        self.st1 = 3
        # self.st2 = self.st1 + 30
        # self.st3 = self.st2 + 65
        self.st2 = 3
        self.st3 = 3
        self.st4 = 3

        self.signal_event_list = [

            # 场景1：带小女孩找阳光下的空位
            # (3, self.add_walker, (5, 230, 1200)),  # 0号"Girl02_C_3"
            # (1, self.control_walker, (0, False, 200, 60, 520, 0)),
            # (9, self.customer_say, (0, "Good morning! I'm looking for a place where I can enjoy the sunshine.")),
            # (1, self.customer_say, (0, "Could you take me there?")),#可以带我过去嘛？
            # (13, self.control_walker, (0, False, 50, 140, 1200, 180)),  # 小女孩站在了 BrightTable1 旁边就餐啦

            # # 场景2：有个胖胖男人点单交流并要咖啡，帮他送去角落的桌子
            (3, self.add_walker, (5, 230, 1200)), # 小女孩
            # # # # 上述准备
            (10, self.add_walker, (26, -28, -150, 90)),
            (0, self.add_walker, (10, -70, -200, -45)),
            (5, self.customer_say, (1, "Hey, RoboWaiter, come here for a moment!")),
            (20, self.control_walkers_and_say, ([[[1, False, 100, -18, -200, -90, "What drinks do you have here?"]]])), #6
            # 20 胖胖男到了 BrightTable6
            (2, self.customer_say, (1, "What kinds of coffee do you have?")),  # 10
            (2, self.customer_say, (1, "I'll have a cappuccino, please.")),  # 15

            # # 场景3：有位女士要杯水和冰红茶
            (3, self.add_walker, (5, 230, 1200)),
            (3, self.add_walker, (26, -30, -200, -90)),
            (3, self.add_walker, (10, -80, -180, -45)),
            ######
            (3, self.add_walkers,
             ([[[21, 65, 1000, -90], [32, -80, 850, 135], [1, 60, 420, 135], [29, -290, 400, 180]]])),
            (0, self.control_walker, (5, True, 50, 250, 1200, 180)),  # 设置id=4 的2小男孩随机游走红随机游走
            (0, self.add_walker, (48, 60, 520, 0)),  # 生成他妈妈
            (0, self.add_walkers, ([[[48, 60, 520, 0], [31, 60, 600, -90], [20, 60, 680, -90], [9, 60, 760, -90]]])),
            (55, self.customer_say, (7, "Wow, it's so crowded today, are there any seats available?")),  # 女士问 38
            (10, self.customer_say, (7, "I'm with my child, I'd like a spacious and well-lit spot.")),  # 女士问
            (8, self.customer_say, (7, "The tables in the hall look good, please take me there!")),
            (15, self.control_walker, (7, False, 50, -250, 480, 0)),  # #290, 400
            (3, self.customer_say, (7, "I'd like a glass of water, and please get a yogurt for my child.")),
            # # ### 9号灰色男 排队排着排着，不排了
            (0, self.control_walker, (10, False, 100, 100, 760, 180)),
            (0, self.control_walker, (10, True, 100, 0, 0, 180)),
            (90, self.customer_say, (7, "Thank you for the water and yogurt!")),  # 倒水+取放酸奶 90s


            (10, self.control_walkers_and_say, ([[[8, False, 100, 60, 520, 180, "I think I left my VacuumCup in your café yesterday, have you seen it?"]]])),
            (5, self.customer_say, (8,"Can you bring it to me? I'm waiting at the table near the front door.")),
            (1, self.control_walker,(8, False, 80, -10, 520, 90)),# 红女士在吧台前后退一步
            (1, self.control_walker, (8, False, 80, 240, 1000, -45)), # 红女士走到Table1前
            (1, self.control_walker, (9, False, 100, 60, 600, -90)), # 大胖男排队往前走一步
            (2, self.control_walker, (10, False, 100, 60, 680, -90)), # 男灰黑色排队往前走一步
            (6, self.customer_say, (8,"That's the one! Found it, I'm so happy!")), # 红女士在Table1前
            (5, self.customer_say, (8, "No need anymore.")),  # 红女士在Table1前


            (8, self.remove_walkers, ([[0, 7, 8]])),
            (3, self.control_walker, (6, False, 100, 60, 520, 0)), # 10号变7号 男灰黑色排队往前,轮到他
            (2, self.customer_say, (6, "It's so hot! The sun is so intense! Can we turn on the air conditioning?")),
            (20, self.control_walkers_and_say, ([[[6, True, 100, 60, 520, 0, "Thank you, it's much cooler now."]]])),


            # # 场景8 结束了，删除所有顾客。此处增加自主探索发现空间比较暗，打开大厅灯
            (24, self.clean_walkers, ()),
            (1, self.add_walker, (17, 60, 1000)),# 增加警察，提醒下班啦
            (3, self.control_walkers_and_say, ([[[0, False, 150, 60, 520, 0, "It's time to get off work! Don't forget to clean, tidy up the tables and chairs, mop the floor, and manage the curtains, air conditioning, and lights."]]])),

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
            if end[1] >= 600 or end[1] <= 450 or end[0] >= 250:
                # if int(self.status.location.X)!=247 or  int(self.status.location.X)!=520:
                self.walker_followed = True
                self.control_walkers_and_say([[0, False, 150, end[0], end[1], 90, "谢谢！"]])
                self.scene_flag += 1

        # 获得所有顾客的名字
        # print("=================")
        # for cus in self.status.walkers:
        #     print(cus)
        # print("=================")
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLM(robot)
    task.reset()
    task.run()
