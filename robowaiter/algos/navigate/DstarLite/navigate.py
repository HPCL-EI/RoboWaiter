#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import math
from dstar_lite import DStarLite, euclidean_distance


class Navigator:
    '''
        导航类
    '''

    def __init__(self, scene, area_range, map, scale_ratio=5, step_length=150, velocity=150, react_radius=250):
        self.scene = scene
        self.area_range = area_range  # 地图实际坐标范围 xmin, xmax, ymin, ymax
        self.map = map  # 缩放并离散化的地图 array(X,Y)
        self.scale_ratio = scale_ratio  # 地图缩放率
        self.step_length = step_length  # 步长(单次移动)
        self.step_num = self.step_length // self.scale_ratio  # 单次移动地图格数
        self.v = velocity  # 速度
        self.react_radius = react_radius  # robot反应半径

        self.planner = DStarLite(area_range=area_range, map=map, scale_ratio=scale_ratio)

    @staticmethod
    def is_reached(pos: (float, float), goal: (float, float), dis_limit=50):
        '''
            判断是否到达目标
        '''
        dis = math.hypot(pos[0]-goal[0], pos[1]-goal[1])
        # dis = np.linalg.norm(pos - goal)
        return dis < dis_limit

    @staticmethod
    def get_yaw(pos: (float, float), goal: (float, float)):
        '''
            得到移动方向
        '''
        return math.degrees(math.atan2(goal[0] - pos[0], -(goal[1] - pos[1])))

    def legalize_goal(self, goal: (float, float)):
        '''
            TODO: 处理非法目标
            目标在障碍物上：从目标开始方形向外扩展，直到找到可行点
            目标在地图外面：起点和目标连线最靠近目标的可行点
        '''
        return goal

    def navigate(self, goal: (float, float), animation=True):
        '''
            单次导航，直到到达目标
        '''
        if not self.scene.reachable_check(goal[0], goal[1], 0):
            goal = self.legalize_goal(goal)

        pos = (self.scene.status.location.X, self.scene.status.location.Y)  # 机器人当前: 位置 和 朝向
        print('------------------navigation_start----------------------')
        while not self.is_reached(pos, goal):
            dyna_obs = [(walker.pose.X, walker.pose.Y) for walker in self.scene.status.walkers]  # 动态障碍物(顾客)位置列表
            dyna_obs = [obs for obs in dyna_obs if euclidean_distance(obs, pos) < self.react_radius]  # 过滤观测范围外的dyna_obs
            # 周围有dyna_obs则步长减半
            if dyna_obs:
                step_num = self.step_num // 2
            else:
                step_num = self.step_num
            path = self.planner.planning(pos, goal, dyna_obs)
            if path:
                if animation:
                    self.planner.draw_graph(step_num)  # 画出搜索路径
                next_step = min(step_num, len(path))
                next_pos = path[next_step - 1]
                print('plan pos:', next_pos, end=' ')
                yaw = self.get_yaw(pos, next_pos)
                self.scene.walk_to(next_pos[0], next_pos[1], yaw, velocity=self.v, dis_limit=10)
                # pos = (self.scene.status.location.X, self.scene.status.location.Y)
                # if self.is_reached(pos, next_pos):
                self.planner.path = self.planner.path[next_step - 1:]  # 去除已走过的路径
            pos = (self.scene.status.location.X, self.scene.status.location.Y)
            print('reach pos:', pos)

        self.planner.reset()  # 完成一轮导航，重置变量

        if self.is_reached(pos, goal):
            print('The robot has achieved goal !!')




