# !/usr/bin/env python3
# -*- encoding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

from scipy.ndimage import binary_dilation

from scene import scene


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


def discretize_map(scene, scale_ratio):
    X = int(950 / scale_ratio)  # 采点数量
    Y = int(1850 / scale_ratio)
    map = np.zeros((X, Y))

    for x in range(X):
        for y in range(Y):
            if not scene.reachable_check(x * scale_ratio - 350, y * scale_ratio - 400, Yaw=0):
                map[x, y] = 1
                print(x, y)

    file_name = 'map_'+str(scale_ratio)+'.pkl'
    if not os.path.exists(file_name):
        open(file_name, 'w').close()
    with open(file_name, 'wb') as file:
        pickle.dump(map, file)
    print('保存成功')


def expand_obstacles(scale_ratio, expand_range=1):
    '''
        障碍物边沿扩展
        TODO: 扩展后的地图不可用！！！
    '''
    file_name = 'map_'+str(scale_ratio)+'.pkl'
    dilated_file_name = 'map_'+str(scale_ratio)+'_e'+str(expand_range)+'.pkl'

    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            map = pickle.load(file)

    dilated_map = binary_dilation(map, iterations=expand_range)

    if not os.path.exists(dilated_file_name):
        open(dilated_file_name, 'w').close()
    with open(dilated_file_name, 'wb') as file:
        pickle.dump(dilated_map, file)
    print('保存成功')


def show_map(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            map = pickle.load(file)
            draw_grid_map(map)


if __name__ == '__main__':
    # scene.init_world(scene_num=1, mapID=11)
    # scene = scene.Scene(sceneID=0)
    #
    # # 离散化地图
    # discretize_map(scene, scale_ratio=4)

    # # 扩张构型空间
    # expand_obstacles(scale_ratio=3, expand_range=1)

    # 展示离散化地图
    file_name = 'costMap_4.pkl'
    show_map(file_name)
