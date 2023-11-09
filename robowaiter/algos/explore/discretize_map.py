# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

import time

import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

from scene_utils import control




def draw_grid_map(grid_map):
    # 生成新的地图图像
    plt.imshow(grid_map, cmap='binary', alpha=0.5, origin='lower')  # 黑白网格

    # 绘制坐标轴
    plt.xlabel('y', loc='right')
    plt.ylabel('x', loc='top')

    # 显示网格线
    plt.grid(color='black', linestyle='-', linewidth=0.5)

    # 显示图像
    plt.show()
    #plt.pause(0.01)




if __name__ == '__main__':
    # control.init_world(scene_num=1, mapID=3)
    # scene = control.Scene(sceneID=0)
    #
    # X = int(950/5)  # 采点数量
    # Y = int(1850/5)
    # map = np.zeros((X, Y))
    #
    # for x in range(X):
    #     for y in range(Y):
    #         if not scene.reachable_check(x*5-350, y*5-400, Yaw=0):
    #             map[x, y] = 1
    #             print(x, y)
    #
    #
    # file_name = 'map_5.pkl'
    # if not os.path.exists(file_name):
    #     open(file_name, 'w').close()
    # with open(file_name, 'wb') as file:
    #     pickle.dump(map, file)
    # print('保存成功')


    file_name = 'map_5.pkl'
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            map = pickle.load(file)
            draw_grid_map(map)