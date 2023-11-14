import os
import pickle
import time
import random
import math

import matplotlib.pyplot as plt
import numpy as np

from robowaiter.scene import scene
from navigate import Navigator




if __name__ == '__main__':

    file_name = 'map_5.pkl'
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            map = pickle.load(file)

    scene.init_world(1, 11)
    scene = scene.Scene(sceneID=0)

    navigator = Navigator(scene=scene, area_range=[-350, 600, -400, 1450], map=map)

    '''场景1: 无行人环境 robot到达指定目标'''
    # goal = np.array((-100, 700))

    '''场景2: 静止行人环境 robot到达指定目标'''
    # scene.clean_walker()
    # scene.add_walker(50, 300, 0)
    # scene.add_walker(-50, 500, 0)
    # goal = np.array((-100, 700))

    '''场景3: 移动行人环境 robot到达指定目标'''
    scene.walk_to(100, 0, -90, dis_limit=10)
    scene.clean_walker()
    scene.add_walker(50, 300, 0)
    scene.add_walker(-50, 500, 0)
    scene.add_walker(0, 700, 0)
    scene.control_walker([scene.walker_control_generator(walkerID=0, autowalk=False, speed=50, X=-50, Y=600, Yaw=0)])
    scene.control_walker([scene.walker_control_generator(walkerID=1, autowalk=False, speed=50, X=100, Y=150, Yaw=0)])
    scene.control_walker([scene.walker_control_generator(walkerID=2, autowalk=False, speed=50, X=0, Y=0, Yaw=0)])

    goal = (-100, 700)
    # goal = (-300)

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

    scene.clean_walker()
    print(scene.status.collision)  # TODO: 不显示碰撞信息 ???














