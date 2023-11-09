#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import math
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable


from robowaiter.algos.navigate.DstarLite.dstar_lite import DStarLite

class Navigator:
    '''
        导航类
    '''

    def __init__(self, scene, area_range, map, scale_ratio=5):
        self.scene = scene
        self.area_range = area_range                          # 地图实际坐标范围 xmin, xmax, ymin, ymax
        self.map = map                                        # 缩放并离散化的地图 array(X,Y)
        self.scale_ratio = scale_ratio                        # 地图缩放率
        self.step_length = 50                                 # 步长(单次移动)
        self.step_num = self.step_length // self.scale_ratio  # 单次移动地图格数
        self.v = 200                                          # 速度
        self.step_time = self.step_length/self.v + 0.1        # 单步移动时长


        self.planner = DStarLite(area_range=area_range, map=map, scale_ratio=scale_ratio)


    @staticmethod
    def is_reached(pos: np.array((float, float)), goal: np.array((float, float)), dis_limit=25):
        '''
            判断是否到达目标
        '''
        dis = np.linalg.norm(pos - goal)
        return dis < dis_limit

    def reset_goal(self, goal:(float, float)):
        # TODO: 使目标可达
        # 目标在障碍物上：从目标开始方形向外扩展，直到找到可行点
        # 目标在地图外面：起点和目标连线最靠近目标的可行点
        pass

    def navigate(self, goal: (float, float), animation=True):
        '''
            单次导航，直到到达目标
        '''

        pos = np.array((self.scene.status.location.X, self.scene.status.location.Y))  # 机器人当前: 位置 和 朝向
        yaw = self.scene.status.rotation.Yaw
        print('------------------navigation_start----------------------')
        while not self.is_reached(pos, goal):
            dyna_obs = [(walker.pose.X, walker.pose.Y) for walker in self.scene.status.walkers]  # 动态障碍物(顾客)位置列表
            path = self.planner.planning(pos, goal, dyna_obs, step_num=self.step_num)
            if path:
                next_step = min(self.step_num, len(path))
                (next_x, next_y) = path[next_step-1]
                print('plan pos:', (next_x, next_y), end=' ')
                scene_info = self.scene.walk_to(next_x, next_y, yaw, velocity=self.v)
                yaw = scene_info.rotation.Yaw

                if animation:
                    self.planner.draw_graph(self.step_num)  # 画出搜索路径
                # time.sleep(self.step_time)
            pos = np.array((self.scene.status.location.X, self.scene.status.location.Y))
            print('reach pos:', pos)

        self.planner.reset()  # 完成一轮导航，重置变量

        if self.is_reached(pos, goal):
            print('The robot has achieved goal !!')





