#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scene_utils import control

from rrt import RRT
from rrt_star import RRTStar
from apf import APF


class Navigator:
    '''
        导航类
    '''

    def __init__(self, scene, area_range, map, scale_ratio=5):
        self.scene = scene
        self.area_range = area_range                # 地图实际坐标范围 xmin, xmax, ymin, ymax
        self.map = map                              # 缩放并离散化的地图 array(X,Y)
        self.scale_ratio = scale_ratio              # 地图缩放率
        self.step_length = 50                       # 步长(单次移动)
        self.v = 100                                # 速度
        self.step_time = self.step_length/self.v    # 单步移动时长

        self.planner = RRTStar(rand_area=area_range, map=map, scale_ratio=scale_ratio, max_iter=400, search_until_max_iter=True)

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

    def navigate(self, goal: (float, float), path_smoothing=True, animation=True):
        pos = np.array((self.scene.status.location.X, self.scene.status.location.Y))  # 机器人当前: 位置 和 朝向
        yaw = self.scene.status.rotation.Yaw
        print('------------------navigation_start----------------------')

        path = self.planner.planning(pos, goal, path_smoothing, animation)
        if path:
            self.planner.draw_graph(final_path=path)  # 画出探索过程
            for (x, y) in path:
                self.scene.walk_to(x, y, yaw, velocity=self.v)
                time.sleep(self.step_time)
            pos = np.array((self.scene.status.location.X, self.scene.status.location.Y))

        self.planner.reset()



        '''APF势场法暂不可用'''
        # while not self.is_reached(pos, goal):
        #     # 1. 路径规划
        #     path = self.planner.planning(pos, goal, path_smoothing, animation)
        #     self.planner.draw_graph(final_path=path)  # 画出探索过程
        #
        #     # 2. 使用APF导航到路径中的每个waypoint
        #     traj = [(pos[0], pos[1])]
        #     #self.planner.draw_graph(final_path=traj)  # 画出探索过程
        #     for i, waypoint in enumerate(path[1:]):
        #         print('waypoint [', i, ']:', waypoint)
        #         # if (not self.scene.reachable_check(waypoint[0], waypoint[1], yaw)) and self.map[self.planner.real2map(waypoint[0], waypoint[1])] == 0:
        #         #     print('error')
        #         while not self.is_reached(pos, waypoint):
        #             # 2.1 计算next_step
        #             pos = np.array((self.scene.status.location.X, self.scene.status.location.Y))
        #             Pobs = []  # 障碍物(顾客)位置数组
        #             for walker in self.scene.status.walkers:
        #                 Pobs.append((walker.pose.X, walker.pose.Y))
        #             next_step, _ = APF(Pi=pos, Pg=waypoint, Pobs=Pobs, step_length=self.step_length)
        #             traj.append((next_step[0], next_step[1]))
        #             #self.planner.draw_graph(final_path=traj)  # 画出探索过程
        #             while not self.scene.reachable_check(next_step[0], next_step[1], yaw):  # 取中点直到next_step可达
        #                 traj.pop()
        #                 next_step = (pos + next_step) / 2
        #                 traj.append((next_step[0], next_step[1]))
        #                 #self.planner.draw_graph(final_path=traj)  # 画出探索过程
        #             # 2.2 移动robot
        #             self.scene.walk_to(next_step[0], next_step[1], yaw, velocity=self.v)
        #             # print(self.scene.status.info)  # print navigation info
        #             # print(self.scene.status.collision)
        #             time.sleep(self.step_time)
        #         # print(self.scene.status.info)  # print navigation info
        #         # print(self.scene.status.collision)
        #     self.planner.reset()
        if self.is_reached(pos, goal):
            print('The robot has achieved goal !!')









# class Walker:
#     def __int__(self, scene):
#         self.scene = scene
#
#     def add_walkers(self, walker_loc, scene_id=0):
#         """
#             批量添加行人
#             Args:
#                 walker_loc: 行人的初始位置列表( 列表元素数量对应行人数量 )
#         """
#         print('------------------add walker----------------------')
#         walker_list = []
#         for i in range(len(walker_loc)):
#             # 只有可达的位置才能成功初始化行人，显示unreachable的地方不能初始化行人
#             walker_list.append(
#                 GrabSim_pb2.WalkerList.Walker(id=i, pose=GrabSim_pb2.Pose(X=walker_loc[0], Y=walker_loc[1], Yaw=90)))
#         scene = self.client.AddWalker(GrabSim_pb2.WalkerList(walkers=walker_list, scene=scene_id))  # 生成环境中行人
#         # print(self.client.Observe(GrabSim_pb2.SceneID(value=scene_id)).walkers) # 打印行人信息
#         return scene
#
#     def control_walkers(self, walker_loc, scene_id=0):
#         """
#             批量移动行人
#             Args:
#                 walker_loc: 行人的终止位置列表
#         """
#         scene = self.client.Observe(GrabSim_pb2.SceneID(value=scene_id))
#         controls = []
#         for i in range(len(scene.walkers)):
#             loc = walker_loc[i]
#             is_autowalk = False  # True: 随机移动; False: 移动到目标点
#             pose = GrabSim_pb2.Pose(X=loc[0], Y=loc[1], Yaw=180)
#             controls.append(GrabSim_pb2.WalkerControls.WControl(id=i, autowalk=is_autowalk, speed=200, pose=pose))
#         scene = self.client.ControlWalkers(
#             GrabSim_pb2.WalkerControls(controls=controls, scene=scene_id))  # 设置行人移动速度和目标点
#         # print(self.client.Observe(GrabSim_pb2.SceneID(value=scene_id)).walkers) # 打印行人信息
#         time.sleep(10)
#         return scene
#
#     def remove_walkers(self, ids, scene_id=0):
#         '''
#             按编号移除行人
#             Args:
#                 ids: 待移除的行人编号列表
#         '''
#         scene = self.client.RemoveWalkers(GrabSim_pb2.RemoveList(IDs=ids, scene=scene_id))  # 按编号移除行人
#         # print(self.client.Observe(GrabSim_pb2.SceneID(value=scene_id)).walkers) # 打印行人信息
#         time.sleep(2)
#         return scene
#
#     def clean_walkers(self, scene_id=0):
#         '''
#             删除环境中所有行人
#         '''
#         scene = self.client.CleanWalkers(GrabSim_pb2.SceneID(value=scene_id))
#         return scene
