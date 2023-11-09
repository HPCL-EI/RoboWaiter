import os
import pickle
import time
import random

import matplotlib.pyplot as plt
import numpy as np

from scene_utils import control  # TODO: 文件名改成Scene.py
from navigate import Navigator



if __name__ == '__main__':

    file_name = 'map_5.pkl'
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            map = pickle.load(file)

    control.init_world(1, 3)
    scene = control.Scene(sceneID=0)
    scene.reset()

    navigator = Navigator(scene=scene,  area_range=[-350, 600, -400, 1450], map=map)
    goal = (200, 1400)
    navigator.navigate(goal, animation=False)


    # scene.add_walker(1085, 2630, 220)
    # scene.control_walker([scene.walker_control_generator(0, False, 100, 755, 1900, 180)])

    # print(scene.status)
    #
    # control.init_world(1, 3)
    #
    # scene = control.Scene(sceneID=0)
    #
    # # 实现单顾客领位
    # scene.reset()
    # scene.add_walker(0, -200, 220)
    #
    # for walker in scene.status.walkers:
    #     print(walker.pose.X)
    # print('*************************')
    # time.sleep(3)
    # for walker in scene.status.walkers:
    #     print(walker.pose)
    # print('*************************')
    #
    # scene.control_walker([scene.walker_control_generator(0, False, 500, 70, 880, 120)])
    # time.sleep(0.5)
    # for walker in scene.status.walkers:
    #     print(walker.pose)
    # print('*************************')
    # time.sleep(5)
    # for walker in scene.status.walkers:
    #     print(walker.pose.X)
    # print('*************************')
    #
    # scene.remove_walker(0)
    # scene.clean_walker()


