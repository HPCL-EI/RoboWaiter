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
        self.signal_event_list = [
            (5, self.customer_say, (5, "给我来杯咖啡，哦对，再倒一杯水。")),
            (1, self.control_walker_ls,([[[5, False, 100, -250, 480, 0],[6, False, 100, 60, 520, 0]]])),
            (-1, self.customer_say, (5, "感谢，这些够啦，你去忙吧。")),
            (10, self.customer_say, (6, "我想来份点心和酸奶。")),
            (-1, self.customer_say, (6, "真美味啊！")),
        ]

    def _reset(self):
        self.gen_obj()
        self.add_walkers([ [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
        self.control_walker(1, True, 100, 60, 720, 0)
        self.control_walker(4, True, 100, 60, -120, 0)
        self.add_walkers([[16,60, 520], [47,-40, 520]])
        self.state["condition_set"] = { 'At(Robot,Bar)', 'Is(AC,Off)',
                          'Holding(Nothing)', 'Exist(Yogurt)', 'Exist(BottledDrink)',
                          'On(BottledDrink,Bar)',
                          'Exist(VacuumCup)', 'On(VacuumCup,Table2)',
                          'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
                          'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
        pass

    def _run(self, op_type=10):
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
