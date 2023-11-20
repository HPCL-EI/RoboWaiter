"""
视觉语言导航

测试导航算法的动态避障(Obstacle Detection and Avoidance, ODA)能力



"""
import os
import pickle
import time
import random

import matplotlib.pyplot as plt
import numpy as np

from robowaiter.scene.scene import Scene
from robowaiter.utils import get_root_path



class SceneVLN(Scene):
    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件， (事件发生的时间，事件函数)
        # self.event_list = [
        #     (5, self.create_chat_event("测试VLN：前往水台")),
        # ]

    def _reset(self):
        '''
            设置场景 (添加行人...)
        '''
        # root_path = get_root_path()
        # map_file = os.path.join(root_path, 'robowaiter/algos/navigator/map_4.pkl')
        # with open(map_file, 'rb') as file:
        #     map = pickle.load(file)
        # self.state['map']['2d'] = map


        # 角1:[480, 1300, 90]
        # 窗1:[230, 1200, 135]
        # 窗2:[65, 1000, 135.0]
        # 窗3:[-80, 850, 135]
        # 窗4:[-270, 520, 150]
        # 窗5:[-20, -220, -100]
        # 角2:[250, -240, -65]


        # 1. robot位置初始化
        self.walk_to(-20, -220, velocity=150, dis_limit=10)

        # 2. 添加行人
        self.clean_walker()
        self.add_walkers([[230, 1200], [50, 600], [-20, 0], [-80, 850]])

        # walker_0: 窗1-窗3-窗5
        self.control_walker([self.walker_control_generator(walkerID=0, autowalk=False, speed=30, X=20, Y=800, Yaw=0),
                             self.walker_control_generator(walkerID=0, autowalk=False, speed=30, X=-20, Y=-220, Yaw=0)])
        # walker_1: 右-窗5
        self.control_walker([self.walker_control_generator(walkerID=1, autowalk=False, speed=30, X=0, Y=-220, Yaw=0)])

        # walker_2: 吧台前-右
        self.control_walker([self.walker_control_generator(walkerID=2, autowalk=False, speed=30, X=20, Y=800, Yaw=0)])

        # walker_3: 占据目标
        self.control_walker([self.walker_control_generator(walkerID=3, autowalk=False, speed=30, X=230, Y=1200, Yaw=0)])

        # 3. 导航
        goal = (230, 1200)
        self.navigator.navigate(goal=goal, animation=False)

        # self.walk_to(goal[0], goal[1], velocity=35, dis_limit=10)


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLN(robot)
    task.reset()
    task.run()

