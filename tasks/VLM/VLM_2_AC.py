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
            (3, self.add_walker,  (0,0,700)),
            (1, self.control_walker, (6, False,100, 60, 520,0)), #[walkerID,autowalk,speed,X,Y,Yaw]
            (2, self.customer_say, (6, "好热呀，想开空调，想要温度调低点！")),
            (6, self.control_walker, (6, False, 200, 60, 80, 0)),
            (-1, self.customer_say, (6, "谢谢！这下凉快了！")),  #(-100,600)
        ]

    def _reset(self):
        self.gen_obj()

        self.add_walkers([[4,1, 880], [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
        self.control_walkers(walker_loc=[[-55, 750], [70, -200], [250, 1200], [0, 880]],is_autowalk = True)

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
