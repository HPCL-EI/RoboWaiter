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
        self.event_list = [
            (5, self.create_chat_event("请问可以带我去空位上嘛？我想晒太阳。")),
        ]

    def _reset(self):
        self.gen_obj()
        self.add_walkers([[47, 920]])
        pass

    def _run(self, op_type=10):
        # 一个行人从门口走到 吧台
        # 打招呼需要什么
        # 行人说 哪里有位置，想晒个太阳
        # 带领行人去有太阳的地方
        # 行人说 有点热
        # 好的，这就去开空调
        pass
    
    def _step(self):

        self.control_walker(
            [self.walker_control_generator(walkerID=0, autowalk=False, speed=200, X=60, Y=520, Yaw=180)])
        time.sleep(3)
        cont = self.status.walkers[0].name+":请问可以带我去空位上嘛？我想晒太阳。"
        self.control_robot_action(0,3,cont)


        # 如果机器人不在 吧台
        # if "At(Robot,Bar)" not in self.state['condition_set']:
        end = [self.status.location.X, self.status.location.Y]
        # print("end:",end)
        if end[1]>=600 or end[1]<=450 or end[0]>=250:
        # if int(self.status.location.X)!=247 or  int(self.status.location.X)!=520:
            self.control_walker(
                    [self.walker_control_generator(walkerID=0, autowalk=False, speed=100, X=end[0], Y=end[1], Yaw=-90)])

            cont = self.status.walkers[0].name+"谢谢！"
            self.control_robot_action(0,3,cont)
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLM(robot)
    task.reset()
    task.run()
