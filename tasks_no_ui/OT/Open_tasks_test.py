"""
人提出请求，机器人完成任务
1. 做咖啡（固定动画）：接收到做咖啡指令、走到咖啡机、拿杯子、操作咖啡机、取杯子、送到客人桌子上
2. 倒水
3. 夹点心

具体描述：设计一套点单规则（如菜单包含咖啡、水、点心等），按照规则拟造随机的订单。在收到订单后，通过大模型让机器人输出合理的备餐计划，并尝试在模拟环境中按照这个规划实现任务。

"""

# todo: 接收点单信息，大模型生成任务规划

from robowaiter.scene.scene import Scene

class SceneOT(Scene):

    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件
        self.signal_event_list = [
            # (3, self.customer_say, ("System", "有多少盒装饮料")),
            # (3, self.customer_say, ("System", "桌子有几张")),
            # (3, self.customer_say, ("System", "你们这儿有军棋吗")),
            # (3, self.customer_say, ("System", "军棋有几个")),
            # (3, self.customer_say, ("System", "有几把椅子呀")),
            # (3, self.customer_say, ("System", "有多少顾客")),
            # (3, self.customer_say, ("System", "你们这儿有多少军棋")),

            # (3, self.customer_say, ("System", "哪里有盒装饮料？")),
            # (3, self.customer_say, ("System", "洗手间在哪里？")),#卫生间
            # (3, self.customer_say, ("System", "卫生间在哪里？")),

            # (3, self.customer_say, ("System", "你们这里有棋吗，在哪里")),
            # (3, self.customer_say, ("System", "棋在哪里"))
            # (3, self.customer_say, ("System", "有几副棋")),
            # (3, self.customer_say, ("System", "我的手镯，你有看到吗")),
            # (3, self.customer_say, ("System", "你们这有小说吗？")),
            # (3, self.customer_say, ("System", "我昨天保温杯落在你们咖啡厅了，你看到了吗？")),
            # (3, self.customer_say, ("System", "你们这有魔方吗？")),
            # (3, self.customer_say, ("System", "垃圾桶在哪呀？")),

            # (3, self.customer_say, ("System", "这有小说吗？在哪里")),

            # (3, self.customer_say, ("System", "还有空位吗")),

            (3, self.customer_say, ("System", "有空桌子吗")),


            # (3, self.customer_say, ("System", "把盒装冰红茶放到水桌")),
            # (3, self.customer_say, ("System", "冰红茶")),
            # (3, self.customer_say, ("System", "酸奶。")),
            # (3, self.customer_say, ("System","来一号桌")),
            # (-1, self.customer_say, ("System","回去吧")),
            # (5, self.set_goal("At(Robot,BrightTable4)"))
        ]
        # self.event_list = [
        #     # (3, self.set_goal("On(VacuumCup,Bar)"))
        #     (3, self.set_goal("On(Yogurt,Bar)"))
        # ]

    def _reset(self):
        self.add_walkers([[0, 880], [250, 1200]])
        self.gen_obj()
        pass


    def _run(self):
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneOT(robot)
    task.reset()
    task.run()
