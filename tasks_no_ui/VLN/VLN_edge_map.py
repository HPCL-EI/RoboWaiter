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
        # with open(map_file, 'rb') as file:D
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
        # self.walk_to(-60, 0, velocity=150, dis_limit=10)


        # 3. 导航
        goal = (10000, 10000)
        self.navigator.navigate(goal=goal, animation=True)

        # self.walk_to(goal[0], goal[1], velocity=150, dis_limit=10)


if __name__ == '__main__':

    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLN(robot)
    task.reset()
    task.run()

