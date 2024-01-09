"""
人提出请求，机器人完成任务
1. 做咖啡（固定动画）：接收到做咖啡指令、走到咖啡机、拿杯子、操作咖啡机、取杯子、送到客人桌子上
2. 倒水
3. 夹点心

具体描述：设计一套点单规则（如菜单包含咖啡、水、点心等），按照规则拟造随机的订单。在收到订单后，通过大模型让机器人输出合理的备餐计划，并尝试在模拟环境中按照这个规划实现任务。

"""
import time

# todo: 接收点单信息，大模型生成任务规划

from robowaiter.scene.scene import Scene

class SceneOT(Scene):

    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件
        # self.event_list = [
        #     # (3, self.set_goal("On(VacuumCup,Bar)"))
        #     (3, self.set_goal("On(Yogurt,Bar)"))
        # ]
        self.signal_event_list =[
            # (3, self.set_goal,("On(Yogurt,Bar)",)),
            # (3, self.customer_say, ("System", "把盒装冰红茶放到水桌")),
            (3, self.customer_say, ("System", "打开空调并降低空调温度")),
            # (3, self.customer_say, ("System", "点心")),
            # (3, self.customer_say, ("System", "把咖啡放到水桌")),
            # (3, self.customer_say, ("System", "把咖啡放到吧台上")),
            # (3, self.customer_say, ("System", "把咖啡放到吧台上，再拿一杯咖啡放到6号桌")),
            # (3, self.customer_say, ("System", "把咖啡放到3号桌")),
            # (3, self.customer_say, ("System", "我想来份点心和酸奶。")),

            # (3, self.customer_say, ("System", "把咖啡或者酸奶放到吧台")),
            # (3, self.customer_say, ("System", "给我来杯咖啡，哦对，再倒一杯水。")),

            # (3, self.customer_say, ("System", "Don't stand at table 6. Please wipe down table 1 or mop the floor, and don't set the air conditioning temperature too low.")),
            # (3, self.customer_say, (" System",
            #                         "Don't stand at table 6. Please wipe down table 1, and don't set the air conditioning temperature too low.")),

        ]

    def _reset(self):
        self.gen_obj()
        scene = self.add_walkers([[0, 0], [250, 1200], [-55, 750], [70, -200]])
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
