"""
视觉语言导航
识别顾客（NPC）靠近、打招呼、对话、领位导航到适合人数的空闲餐桌
开始条件：监测到顾客靠近
结束条件：完成领位，语音：“请问您想喝点什么？”，并等待下一步指令
"""
import os
import pickle
import time
import random

import matplotlib.pyplot as plt
import numpy as np

from robowaiter.scene.scene import Scene,init_world  # TODO: 文件名改成Scene.py

from robowaiter.scene.scene import Scene
from robowaiter.utils import get_root_path
from robowaiter.algos.navigate.navigate import Navigator
from robowaiter.algos.navigate import test

class SceneVLN(Scene):
    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件， (事件发生的时间，事件函数)
        self.event_list = [
            (5, self.create_chat_event("测试VLN：前往2号桌")),
        ]

    def _reset(self):
        root_path = get_root_path()
        file_name = os.path.join(root_path,'robowaiter/algos/navigate/map_5.pkl')
        with open(file_name, 'rb') as file:
            map = pickle.load(file)

        self.state['map']['2d'] = map
        self.state['map']['obj_pos']['Table'] = np.array((-100, 700))

    def _run(self):
        file_name = '../../algos/navigate/map_5.pkl'
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                map = pickle.load(file)

        # self.init_world(1, 11)
        # scene = self.status

        navigator = Navigator(scene=self, area_range=[-350, 600, -400, 1450], map=map)

        '''场景1: 无行人环境 robot到达指定目标'''
        # goal = np.array((-100, 700))

        '''场景2: 静止行人环境 robot到达指定目标'''
        # scene.clean_walker()
        # scene.add_walker(50, 300, 0)
        # scene.add_walker(-50, 500, 0)
        # goal = np.array((-100, 700))

        '''场景3: 移动行人环境 robot到达指定目标'''
        self.walk_to(100, 0, -90, dis_limit=10)
        self.clean_walker()
        self.add_walkers([[50, 300], [-50, 500], [0, 700]])
        # scene.add_walker(50, 300, 0)
        # scene.add_walker(-50, 500, 0)
        # scene.add_walker(0, 700, 0)
        self.control_walker(
            [self.walker_control_generator(walkerID=0, autowalk=False, speed=50, X=-50, Y=600, Yaw=0)])
        self.control_walker(
            [self.walker_control_generator(walkerID=1, autowalk=False, speed=50, X=100, Y=150, Yaw=0)])
        self.control_walker([self.walker_control_generator(walkerID=2, autowalk=False, speed=50, X=0, Y=0, Yaw=0)])

        # goal = (-100, 700)
        # goal = (-300)
        # goal = (340.0, 900.0)

        # goal = (240.0, 1000.0)
        # goal = (340.0, 900.0)
        goal = (240.0, 1160.0)

        '''场景4: 行人自由移动 robot到达指定目标'''
        # # TODO: autowalk=True仿真器会闪退 ???
        # scene.clean_walker()
        # scene.add_walker(50, 300, 0)
        # scene.add_walker(-50, 500, 0)
        # scene.control_walker([scene.walker_control_generator(walkerID=0, autowalk=True, speed=20, X=0, Y=0, Yaw=0)])
        # scene.control_walker([scene.walker_control_generator(walkerID=1, autowalk=True, speed=20, X=0, Y=0, Yaw=0)])
        # time.sleep(5)
        # goal = np.array((-100, 700))

        navigator.navigate(goal, animation=False)

        self.clean_walker()
        print(self.status.collision)  # TODO: 不显示碰撞信息 ???
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLN(robot)
    task.reset()
    task.run()
