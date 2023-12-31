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

        self.new_event_list = [

            # 场景1：带小女孩找阳光下的空位
            # (3, self.add_walker, (5, 230, 1200)),
            # (3, self.control_walker, (0, False, 200, 60, 520, 0)),
            # (12, self.customer_say, (0, "早上好呀，我想找个能晒太阳的地方。")),
            # (12, self.customer_say, (0,"可以带我过去嘛？")),
            # (20, self.control_walker, (0, False, 50, 140, 1200, 180)), # 小女孩站在了 BrightTable1 旁边就餐啦

            # 场景2：有个胖胖男人点单交流并要咖啡，帮他送去角落的桌子
            # (3, self.add_walker, (5, 230, 1200)), # 小女孩
            # 上述准备
            # (self.st2, self.add_walker, (26, -28, -150, 90)),
            # (self.st2, self.add_walker, (10, -70, -200, -45)),
            # (self.st2, self.customer_say, (1, "嘿，RoboWaiter，过来一下！")),
            # (self.st2+10, self.control_walkers_and_say, ([[[1, False, 100, -18, -200, -90, "你们这有什么饮料嘛？"]]])), # 20 胖胖男到了 BrightTable6
            # (self.st2+15, self.customer_say, (1, "咖啡有哪些呢？")),# 10
            # (self.st2+15+5, self.customer_say, (1,"来杯卡布奇诺吧。")), # 15

            # 场景3：有位女士要杯水和冰红茶
            # (3, self.add_walker, (5, 230, 1200)),
            # (3, self.add_walker, (26, -30, -200, -90)),
            # (3, self.add_walker, (10, -80, -180, -45)),
            # # # 上述准备
            # (self.st3, self.add_walker, (21, 65, 1000, -90)),  # 男 'BrightTable2': (65, 1000, 135),
            # (self.st3, self.add_walker, (32, -80, 850, 135)),  # 女 'BrightTable3': (-80, 850, 135),
            #
            # (self.st3, self.add_walker, (1, 60, 420, 135)), # 生成小男孩随机游走
            # (self.st3, self.control_walker, (5, True, 50, 250, 1200, 180)), #设置id=4 的2小男孩随机游走红随机游走
            # (self.st3, self.add_walker, (48, 60, 520,0)),# 生成他妈妈
            #
            # (self.st3, self.add_walker, (31, 60, 600, -90)),  # 女红色排队 7号
            # (self.st3, self.add_walker, (9, 60, 680, -90)),  # 男灰黑色排队 8号
            # (self.st3, self.add_walker, (20, 60, 760, -90)),  # 大胖男排队 9号
            #
            # (self.st3 + 3, self.customer_say, (6, "哎呦，今天这么多人，还有空位吗？")),# 女士问
            # (self.st3 + 10, self.customer_say, (6, "我带着孩子呢，想要宽敞亮堂的地方。")),  # 女士问
            # # 好的，我明白了，那么您可以选择我们的家庭亲子座，这样可以容纳您的孩子，并且更加宽敞舒适。
            # # 这里可以加一下自主导航和探索，找到一个位置
            # # 好的，我明白了，那么我们推荐您到大厅的桌子，那里的空间比较宽敞，环境也比较明亮，适合带着孩子一起用餐。
            # (self.st3 + 15, self.customer_say, (6, "大厅的桌子好啊，快带我去呀！")),
            # (self.st3 + 25, self.control_walker, (6, False, 50,-250, 480, 0)), #  #290, 400
            # (self.st3 + 25, self.customer_say, (6, "我想来杯水，帮我孩子拿个酸奶吧。")),
            # (self.st3 + 60, self.customer_say, (6, "谢谢！")),


            # 场景4：三人排队点单，一人要冰红茶，一个要点心，一个没座位了赠送保温杯
            (3, self.add_walker, (5, 230, 1200)),
            (3, self.add_walker, (26, -30, -200, -90)),
            (3, self.add_walker, (10, -80, -180, -45)),
            (3, self.add_walker, (21, 65, 1000, -90)),  # 男 'BrightTable2': (65, 1000, 135),
            (3, self.add_walker, (32, -80, 850, 135)),
            (3, self.add_walker, (1, 60, 220, 135)),
            (3, self.add_walker, (48, 60, 320, 0)),
            (3, self.add_walker, (31, 60, 600, -90)), # 女红色排队
            (3, self.add_walker, (9, 60, 680, -90)), # 男灰黑色排队
            (3, self.add_walker, (20, 60, 760, -90)),  # 大胖男排队

            (3, self.add_walker, (6, -55, 750,180)),

            # # # 上述准备
            (self.st4+5, self.control_walkers_and_say, ([[[7, False, 100, 60, 520, 0, "我昨天保温杯好像落在你们咖啡厅了，你看到了吗？"]]])),
            (self.st4 + 10, self.customer_say, (7,"你可以帮我拿来吗，我在前门的桌子前等你。")),
            (self.st4 + 13, self.control_walker,(7, False, 80, -10, 520, 90)),# 红女士在吧台前后退一步
            (self.st4 + 14, self.control_walker, (7, False, 80, 240, 1000, -45)), # 红女士走到Table1前
            (self.st4 + 15, self.control_walker, (8, False, 100, 60, 600, -90)),
            (self.st4 + 17, self.control_walker, (9, False, 100, 60, 680, -90)),
            (self.st4 + 25, self.customer_say, (7,"就是这个杯子！找到啦，好开心！")), # 红女士在Table1前
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
                self.control_walkers_and_say([[0,False,150,end[0],end[1],90,"谢谢！"]])
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
