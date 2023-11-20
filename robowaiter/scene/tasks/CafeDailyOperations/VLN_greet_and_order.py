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
            # (3, self.add_walker, (5, 230, 1200)), # 0号"Girl02_C_3"
            # (1, self.control_walker, (0, False, 200, 60, 520, 0)),
            # (9, self.customer_say, (0, "早上好呀，我想找个能晒太阳的地方。")),
            # (-1, self.customer_say, (0,"可以带我过去嘛？")),
            # (0, self.control_walker, (0, False, 50, 140, 1200, 180)), # 小女孩站在了 BrightTable1 旁边就餐啦



            # # 场景2：有个胖胖男人点单交流并要咖啡，帮他送去角落的桌子
            (3, self.add_walker, (5, 230, 1200)), # 小女孩
            # # # 上述准备
            (10, self.add_walker, (26, -28, -150, 90)),
            (0, self.add_walker, (10, -70, -200, -45)),
            (6, self.customer_say, (1, "嘿，RoboWaiter，过来一下！")),
            (8, self.control_walkers_and_say, ([[[1, False, 100, -18, -200, -90, "你们这有什么饮料嘛？"]]])), # 20 胖胖男到了 BrightTable6
            (2, self.customer_say, (1, "咖啡有哪些呢？")),# 10
            (2, self.customer_say, (1,"来杯卡布奇诺吧。")), # 15


            # # 场景3：有位女士要杯水和冰红茶
            # (30, self.add_walker, (5, 230, 1200)),
            # (0, self.add_walker, (26, -30, -200, -90)),
            # (0, self.add_walker, (10, -80, -180, -45)),
            # # # # 上述准备
            # (0, self.add_walker, (21, 65, 1000, -90)),  # 男 'BrightTable2': (65, 1000, 135),
            # (0, self.add_walker, (32, -80, 850, 135)),  # 女 'BrightTable3': (-80, 850, 135),
            # (0, self.add_walker, (1, 60, 420, 135)), # 生成小男孩随机游走
            (0,self.add_walkers,([[[21, 65, 1000, -90],[32, -80, 850, 135],[1, 60, 420, 135]]])),
            (0, self.control_walker, (5, True, 50, 250, 1200, 180)), #设置id=4 的2小男孩随机游走红随机游走
            (0, self.add_walker, (48, 60, 520,0)),# 生成他妈妈
            # (0, self.add_walker, (31, 60, 600, -90)),  # 女红色排队 7号
            # (0, self.add_walker, (20, 60, 680, -90)),  # 大胖男色排队 8号
            # (0, self.add_walker, (9, 60, 760, -90)),  # 男灰黑排队 9号
            # (0, self.add_walker, (29, -290, 400, 180)),  # 青色女人占了位置 BrightTable5
            (0, self.add_walkers, ([[[48, 60, 520,0], [31, 60, 600, -90], [20, 60, 680, -90],[9, 60, 760, -90],[29, -290, 400, 180]]])),
            #
            # # (5, self.customer_say, (6, "哎呦，今天这么多人，还有空位吗？")),# 女士问
            # # (15, self.customer_say, (6, "我带着孩子呢，想要宽敞亮堂的地方。")),  # 女士问
            # # 好的，我明白了，那么您可以选择我们的家庭亲子座，这样可以容纳您的孩子，并且更加宽敞舒适。
            # # 这里可以加一下自主导航和探索，找到一个位置
            # # 好的，我明白了，那么我们推荐您到大厅的桌子，那里的空间比较宽敞，环境也比较明亮，适合带着孩子一起用餐。
            # (8, self.customer_say, (6, "大厅的桌子好啊，快带我去呀！")),
            # (15, self.control_walker, (6, False, 50,-250, 480, 0)), #  #290, 400
            # # (3, self.customer_say, (6, "我想来杯水，帮我孩子拿个酸奶吧。")),
            # # ### 9号灰色男 排队排着排着，不排了
            # (0, self.control_walker, (9, False, 100, 100, 760, 180)),
            # (0, self.control_walker, (9, True, 100, 0, 0, 180)),
            # # # ### 增加场景，孩子说热要开空调 或者9号随机游走和说
            # # (90, self.customer_say, (6, "谢谢！")), #倒水+取放酸奶 90s
            # (3, self.customer_say, (6, "谢谢！")),



            # # # 场景4：三人排队点单，女士要保温杯
            # (3, self.add_walker, (5, 230, 1200)),
            # (0, self.add_walker, (26, -30, -200, -90)),
            # (0, self.add_walker, (10, -80, -180, -45)),
            # (0, self.add_walker, (21, 65, 1000, -90)),  # 男 'BrightTable2': (65, 1000, 135),
            # (0, self.add_walker, (32, -80, 850, 135)),
            # (0, self.add_walker, (1, 60, 220, 135)),
            # (0, self.add_walker, (48, 60, 320, 0)),
            # (0, self.add_walker, (31, 60, 600, -90)), # 女红色排队 7号找保温杯的顾客
            # (0, self.add_walker, (20, 60, 680, -90)),  # 大胖男排队
            # (0, self.add_walker, (9, 60, 760, -90)), # 男灰黑色排队
            # (0, self.add_walker, (29, -290, 400, 180)), # # 青色女人占了位置 BrightTable5
            # # # # # # 上述准备
            # # (5, self.control_walkers_and_say, ([[[7, False, 100, 60, 520, 180, "我昨天保温杯好像落在你们咖啡厅了，你看到了吗？"]]])), #13
            # (0, self.control_walkers_and_say, ([[[7, False, 100, 60, 520, 180, "我昨天保温杯好像落在你们咖啡厅了，你看到了吗？"]]])),
            # (5, self.customer_say, (7,"你可以帮我拿来吗，我在前门的桌子前等你。")),
            # (1, self.control_walker,(7, False, 80, -10, 520, 90)),# 红女士在吧台前后退一步
            # (1, self.control_walker, (7, False, 80, 240, 1000, -45)), # 红女士走到Table1前
            # (1, self.control_walker, (8, False, 100, 60, 600, -90)), # 大胖男排队往前走一步
            # (2, self.control_walker, (9, False, 100, 60, 680, -90)), # 男灰黑色排队往前走一步
            # (6, self.customer_say, (7,"就是这个杯子！找到啦，好开心！")), # 红女士在Table1前
            # (5, self.customer_say, (7, "不用了。")),  # 红女士在Table1前



            # # # 场景5：三人排队点单，一人要冰红茶，一个要点心，一个没座位了赠送保温杯
            # (3, self.add_walker, (5, 230, 1200)),
            # (0, self.add_walker, (26, -30, -200, -90)),
            # (0, self.add_walker, (10, -80, -180, -45)),
            # (0, self.add_walker, (21, 65, 1000, -90)),  # 男 'BrightTable2': (65, 1000, 135),
            # (0, self.add_walker, (32, -80, 850, 135)),
            # (0, self.add_walker, (1, 60, 220, 135)),
            # (0, self.add_walker, (48, 60, 320, 0)), # 生成他妈妈
            # (0, self.add_walker, (31, 280, 1200, -45)), # # 女红色排队 7号找保温杯的顾客
            # (0, self.add_walker, (20, 60, 680, -90)),  # 大胖男排队
            # (0, self.add_walker, (9, 60, 760, -90)), # 男灰黑色排队
            # (0, self.add_walker, (29, -290, 400, 180)), # # 青色女人占了位置 BrightTable5
            # # # 上述准备
            # # # 场景6：大胖男点了外卖，离开啦
            # # (9, self.control_walkers_and_say, ([[[8, False, 100, 60, 520, 0, "给我来份午餐套餐。"]]])), #原来写了26s
            # (0, self.animation_reset,()), #重置任务
            # # (6, self.customer_say, (8, "打包吧，快点！")),
            # # (2, self.control_walker, (9, False, 100, 60, 620, -90)),  # 男灰黑色排队往前走一步
            # # # (100, self.customer_say, (8, "谢啦，我赶时间！")), #100这个时间很合适
            # # (2, self.control_walker, (8, False, 250, 20, 520, -90)), # 大胖男着急得离开啦
            # # (2, self.control_walker, (8, False, 250, 240, -150, -90)),
            # (5, self.remove_walkers, ([[0,7,8]])),
            # # (2, self.control_walker, (6, False, 100, 60, 520, 0)),  # 9号变7号 男灰黑色排队往前,轮到他
            #
            #
            # # 场景7：最后排队那个随机游走 9号变为6号，随机游走。
            # # 机器人自主发现任务，走一圈去擦桌子/拖地，碰到灰色男问好，灰色男说“太阳大，要关窗帘和空调调低”
            # # 开了空调
            # (2, self.control_walker, (6, False, 100, 60, 520, 0)), # 10号变7号 男灰黑色排队往前,轮到他
            # # (2, self.customer_say, (6, "好热呀！太阳也好大！")),
            # # (10, self.control_walkers_and_say, ([[[6, True, 100, 60, 520, 0, "谢谢，这下凉快了"]]])),
            #
            #
            # # 场景8 结束了，删除所有顾客。此处增加自主探索发现空间比较暗，打开大厅灯
            # (3, self.clean_walkers, ()),
            # (1, self.add_walker, (17, 60, 1000)),# 增加警察，提醒下班啦
            # (3, self.control_walkers_and_say, ([[[0, False, 150, 60, 520, 0, "下班啦！别忘了打扫卫生。"]]])),
            # (3, self.control_walkers_and_say, ([[[0, False, 150, 60, 520, 0, "不用了。"]]])),




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
