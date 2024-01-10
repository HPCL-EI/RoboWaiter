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
        self.signal_event_list = [
            # (3, self.add_walker, (5, 230, 1200)),
            # (3, self.add_walker, (26, -30, -200, -90)),
            # (3, self.add_walker, (10, -80, -180, -45)),
            (3, self.add_walkers,
             ([[[21, 65, 1000, -90], [32, -80, 850, 135], [1, 60, 420, 135], [29, -290, 400, 180]]])),
            (0, self.control_walker, (5, True, 50, 250, 1200, 180)),  # 设置id=4 的2小男孩随机游走红随机游走
            (0, self.add_walker, (48, 60, 520, 0)),  # 生成他妈妈
            (0, self.add_walkers, ([[[48, 60, 520, 0], [31, 60, 600, -90], [20, 60, 680, -90], [9, 60, 760, -90]]])),
            (3, self.control_walker, (4, False, 50, -250, 480, 0)),  # #290, 400

            (10, self.control_walkers_and_say, ([[[5, False, 100, 60, 520, 0, #180
                                                   "I think I left my VacuumCup in your café yesterday, have you seen it?"]]])),
            (5, self.customer_say, (5, "Can you bring it to me? I'm waiting at the table near the front door.")),
            (1, self.control_walker, (5, False, 80, -10, 520, 90)),  # 红女士在吧台前后退一步
            (1, self.control_walker, (5, False, 80, 240, 1000, -45)),  # 红女士走到Table1前
            (1, self.control_walker, (6, False, 100, 60, 600, -90)),  # 大胖男排队往前走一步
            (2, self.control_walker, (7, False, 100, 60, 680, -90)),  # 男灰黑色排队往前走一步
            (20, self.customer_say, (5, "That's the one! Found it, I'm so happy!")),  # 红女士在Table1前
            (5, self.customer_say, (5, "No need anymore.")),  # 红女士在Table1前
        ]

    def _reset(self):
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
