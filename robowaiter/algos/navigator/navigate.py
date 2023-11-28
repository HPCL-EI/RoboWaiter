#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import math
import os
import pickle


import matplotlib.pyplot as plt
import numpy as np
from robowaiter.scene import scene

from robowaiter.algos.navigator.dstar_lite import DStarLite, euclidean_distance



class Navigator:
    '''
        导航类
    '''

    def __init__(self,
                 scene,
                 area_range,
                 map,
                 scale_ratio=5,
                 step_length=120,
                 velocity=300,
                 react_radius=300,
                 dyna_obs_radius=40,
                 vision_radius=math.pi*3/7,
                 max_iteration=100):
        self.scene = scene
        self.area_range = area_range        # 地图实际坐标范围 xmin, xmax, ymin, ymax
        self.map = map                      # 缩放并离散化的地图 array(X,Y)
        self.scale_ratio = scale_ratio      # 地图缩放率s
        self.step_length = step_length      # 步长(单次移动)
        self.step_num = self.step_length // self.scale_ratio  # 单次移动地图格数
        self.cur_step_num = self.step_num
        self.v = velocity  # 速度
        self.react_radius = react_radius    # robot反应半径
        self.dyna_obs_radius = dyna_obs_radius
        self.vision_radius = vision_radius
        self.max_iteration = max_iteration  # 最大规划迭代次数

        self.planner = DStarLite(area_range=area_range, map=map, scale_ratio=scale_ratio, react_radius=react_radius, vision_radius=vision_radius, dyna_obs_radius=dyna_obs_radius)
        self.yaw = None

    def validate_goal(self, goal):
        '''
            目标合法化
        '''
        return self.planner.map2real(self.planner.real2map(goal))

    def get_dyna_obs(self, pos, yaw):
        '''
            获获dyna_obs位置列表 (反应半径内 + 视野范围内)
            Args:
                pos:            robot位置
                yaw:            robot朝向 (弧度)
                vision_radius:  视野半径 (弧度)
        '''
        # obs列表
        dyna_obs = [np.array((walker.pose.X, walker.pose.Y)) for walker in self.scene.status.walkers]
        # 反应半径内的dyna_obs
        dyna_obs = [obs for obs in dyna_obs if euclidean_distance(obs, pos) < self.react_radius]
        # 视野范围内的dyna_obs
        if yaw is not None:
            vec_dir = np.array((math.cos(yaw), math.sin(yaw)))  # robot单位方向向量
            # 视野范围120°
            dyna_obs = [obs for obs in dyna_obs if
                        np.dot(vec_dir, (obs-pos)/np.linalg.norm(obs-pos)) >= math.cos(self.vision_radius)]
        return dyna_obs

    @staticmethod
    def is_reached(pos: (float, float), goal: (float, float), dis_limit=75):
        '''
            判断是否到达目标
        '''
        dis = math.hypot(pos[0]-goal[0], pos[1]-goal[1])
        # dis = np.linalg.norm(pos - goal)
        return dis < dis_limit

    @staticmethod
    def get_yaw(pos: (float, float), goal: (float, float)):
        '''
            得到移动方向 (弧度)
        '''
        return math.atan2((goal[1] - pos[1]), (goal[0] - pos[0]))

    def navigate(self, goal: (float, float), animation=True):
        '''
            单次导航，直到到达目标
        '''
        goal = np.array(self.validate_goal(goal))  # 目标合法化
        pos = np.array((self.scene.status.location.X, self.scene.status.location.Y))  # 机器人当前: 位置 和 朝向
        self.yaw = None
        print('------------------navigation_start----------------------')
        for i in range(self.max_iteration):
            dyna_obs = self.get_dyna_obs(pos, self.yaw)
            # dyna_obs = [np.array((walker.pose.X, walker.pose.Y)) for walker in self.scene.status.walkers]
            # 周围有dyna_obs则步长根据离dyna_obs的最短距离相应减小
            if dyna_obs:
                min_dist = min([euclidean_distance(obs, pos) for obs in dyna_obs])
                self.cur_step_num = math.floor(self.step_num / (2 + self.dyna_obs_radius/min_dist))
                # step_num = self.step_num // 2
            else:
                self.cur_step_num = self.step_num
            path = self.planner.planning(pos, goal, dyna_obs)
            if path:
                if animation:
                    self.planner.draw_graph(self.cur_step_num, self.yaw)  # 画出搜索路径
                next_step = min(self.cur_step_num, len(path))
                next_pos = path[next_step - 1]
                print('plan pos:', next_pos, end=' ')
                self.yaw = self.get_yaw(pos, next_pos)
                self.scene.walk_to(next_pos[0], next_pos[1], math.degrees(self.yaw), velocity=self.v, dis_limit=10)

                # 拍照片
                if self.scene.show_ui:
                    self.scene.get_obstacle_point(self.scene.db, self.scene.status, map_ratio=self.scene.map_ratio, is_nav=True)

                self.planner.path = self.planner.path[next_step - 1:]  # 去除已走过的路径
            pos = np.array((self.scene.status.location.X, self.scene.status.location.Y))
            print('reach pos:', pos)
            if self.is_reached(pos, goal):
                break

        self.planner.reset()  # 完成一轮导航，重置变量

        if self.is_reached(pos, goal):
            print('The robot has achieved goal !!')
        else:
            print("Navigation failed !!")






if __name__ == '__main__':

    # 根据map计算并保存cost_map

    file_name = 'map_4.pkl'
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            map = pickle.load(file)

    scene.init_world(1, 11)
    scene = scene.Scene(sceneID=0)

    navigator = Navigator(scene=scene, area_range=[-350, 600, -400, 1450], map=map, scale_ratio=4)

    navigator.planner.compute_cost_map()

    file_name = 'costMap_4.pkl'
    if not os.path.exists(file_name):
        open(file_name, 'w').close()
    with open(file_name, 'wb') as file:
        pickle.dump(navigator.planner.cost_map, file)
    print('保存成功')