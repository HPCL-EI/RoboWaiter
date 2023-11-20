'''
基于两个D* lite的实现
按照原始算法的伪代码
自己写的D* lite
'''

import math
import os
import pickle
import numpy as np
import heapq

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors

from robowaiter.robot.robot import root_path  # 项目根目录路径


def diagonal_distance(start, end):  #
    return max(abs(start[0] - end[0]), abs(start[1] - end[1]))


def manhattan_distance(start, end):  # 曼哈顿距离
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def euclidean_distance(start, end):  # 欧式距离
    # return np.linalg.norm(start-end)
    # return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    return math.hypot(start[0] - end[0], start[1] - end[1])


def heuristic(start, end, name='euclidean'):
    if name == 'diagonal':
        return diagonal_distance(start, end)
    elif name == 'euclidean':
        return euclidean_distance(start, end)
    elif name == 'manhattan':
        return manhattan_distance(start, end)
    else:
        raise Exception('Error heuristic name!')


class Priority:
    '''
        优先级类
    '''

    def __init__(self, k1, k2):
        self.k1 = k1
        self.k2 = k2

    def __lt__(self, other):  # 定义对象的 < 运算
        return self.k1 < other.k1 or (self.k1 == other.k1 and self.k2 < other.k2)

    def __le__(self, other):  # 定于对象的 <= 运算
        return self.k1 < other.k1 or (self.k1 == other.k1 and self.k2 <= other.k2)


class Node:
    '''
        节点类
    '''

    def __init__(self, pos: (int, int), priority: Priority):
        self.pos = pos  # X Y
        self.priority = priority

    def __lt__(self, other):  # 定义对象的 < 运算
        return self.priority < other.priority

    def __le__(self, other):  # 定于对象的 <= 运算
        return self.priority <= other.priority


class PriorityQueue:
    def __init__(self):
        self.queue = []  # 节点队列
        self.nodes = []  # 节点位置列表

    def is_empty(self):
        # 队列判空
        return len(self.queue) == 0

    def top(self):
        return self.queue[0].pos

    def top_key(self):
        if self.is_empty():
            return Priority(float('inf'), float('inf'))
        return self.queue[0].priority

    def pop(self):
        # 取出第一个节点
        node = heapq.heappop(self.queue)
        self.nodes.remove(node.pos)
        return node

    def insert(self, pos, priority):
        # 创建并添加节点
        node = Node(pos, priority)
        heapq.heappush(self.queue, node)
        self.nodes.append(pos)

    def remove(self, pos):
        # 删除指定节点并重新排序
        self.queue = [n for n in self.queue if n.pos != pos]
        heapq.heapify(self.queue)  # 重排序
        self.nodes.remove(pos)

    def update(self, pos, priority):
        # 更新指定位置的priority值
        for n in self.queue:
            if n.pos == pos:
                n.priority = priority
                break


class DStarLite:
    def __init__(self,
                 map: np.array([int, int]),
                 area_range,  # [x_min, x_max, y_min, y_max] 实际坐标范围
                 scale_ratio=5,  # 地图缩放率
                 react_radius=200,  # 反应半径
                 vision_radius=math.pi/3,  # 视角半径
                 dyna_obs_radius=36,  # dyna_obs实际身位半径
                 max_path_length=2000  # 最大路径步数
                 ):

        self.map = map
        self.background = map.copy()
        self.X = map.shape[0]
        self.Y = map.shape[1]
        (self.x_min, self.x_max, self.y_min, self.y_max) = area_range
        self.scale_ratio = scale_ratio
        self.react_radius = math.floor(react_radius / scale_ratio)
        self.vision_radius = vision_radius
        self.dyna_obs_radius = math.floor(dyna_obs_radius / scale_ratio)  # dyna_obs缩放后身位半径
        self.max_path_length = max_path_length

        self.dyna_obs_list = []  # dyna_obs位置列表 [(x, y)]
        self.dyna_obs_occupy = []  # dyna_obs占用位置列表

        # free:0, obs:1, dyna_obs:2
        self.idx_to_object = {
            0: "free",
            1: "obstacle",
            2: "dynamic obstacle"
        }
        self.object_to_idx = dict(zip(self.idx_to_object.values(), self.idx_to_object.keys()))
        self.object_to_cost = {
            "free": 0,
            "obstacle": float('inf'),
            "dynamic obstacle": float('inf')
        }

        # 读取 cost_map 文件
        file_cost_map = os.path.join(root_path, 'robowaiter/algos/navigator/costMap_' + str(self.scale_ratio) + '.pkl')
        if os.path.exists(file_cost_map):
            with open(file_cost_map, 'rb') as file:
                cost_map = pickle.load(file)
        self.cost_map = cost_map
        self.cost_background = self.cost_map.copy()

        self.s_start = None  # (int,int) 必须是元组(元组可以直接当作矩阵索引)
        self.s_goal = None  # (int,int)
        self.s_last = None  # (int,int)
        self.U = PriorityQueue()
        self.k_m = 0
        self.rhs = np.ones((self.X, self.Y)) * np.inf
        # self.rhs = np.ones_like(self.map) * 1000
        # self.rhs[self.map==self.object_to_idx['obstacle']] = np.inf
        self.g = self.rhs.copy()
        self.path = []

    # def set_map(self, map_):
    #     '''
    #         设置map 和 cost_map
    #     '''
    #     self.map = map_
    #     self.background = map_.copy()
    #     self.X = map_.shape[0]
    #     self.Y = map_.shape[1]
    #     self.compute_cost_map()
    #     self.cost_background = self.cost_map.copy()

    def reset(self):
        '''
            (完成一次导航后)
            重置 1.环境变量
                2.dstar_lite变量
        '''
        # env reset
        self.map = self.background.copy()
        self.cost_map = self.cost_background.copy()
        self.dyna_obs_list.clear()
        self.dyna_obs_occupy.clear()
        self.path.clear()
        # dstar_lite reset
        self.s_start = None
        self.s_goal = None
        self.s_last = None
        self.U = PriorityQueue()
        self.k_m = 0
        self.rhs = np.ones((self.X, self.Y)) * np.inf
        self.g = self.rhs.copy()

    def calculate_key(self, s: (int, int)):
        '''
            计算 位置s 的 key1, key2
            :returns：
                Priority(k1, k2): 可比较的对象
        '''
        k1 = min(self.g[s], self.rhs[s]) + heuristic(self.s_start, s) + self.k_m
        k2 = min(self.g[s], self.rhs[s])
        return Priority(k1, k2)

    def c(self, u: (int, int), v: (int, int), c_old=None) -> float:
        '''
        计算节点间的 路径代价 和 目标位置代价 (目标位置代价为0时采用路径代价)
        (因为是终点->起点的扩展方向，因此v是node，u是v扩展的neighbor)
        Args:
            u:     from pos
            v:     to pos
            c_old: 节点v的旧cost
        '''
        if u == v:
            return 0.0
        if c_old is not None:
            obj_cost = c_old
        else:
            obj_cost = self.cost_map[v]
        if obj_cost > 0:
            return obj_cost
        return heuristic(u, v)

    def contain(self, u: (int, int)):
        '''
            判断 节点u 是否在队列中
        '''
        return u in self.U.nodes

    def update_vertex(self, u: (int, int)):
        '''
            判定节点状态, 更新队列
                不一致且在队列   -->  更新key
                不一致且不在队列 -->  计算key并加入队列
                一致且在队列    -->  移出队列
        '''
        if self.g[u] != self.rhs[u] and self.contain(u):
            self.U.update(u, self.calculate_key(u))
        elif self.g[u] != self.rhs[u] and not self.contain(u):
            self.U.insert(u, self.calculate_key(u))
        elif self.g[u] == self.rhs[u] and self.contain(u):
            self.U.remove(u)

    def compute_shortest_path(self):
        '''
            计算最短路径
        '''

        c_map = self.map.copy()

        while self.U.top_key() < self.calculate_key(self.s_start) or self.rhs[self.s_start] > self.g[self.s_start]:
            u = self.U.top()
            c_map[u] = 10
            k_old = self.U.top_key()
            k_new = self.calculate_key(u)
            if k_old < k_new:
                self.U.update(u, k_new)
            elif self.g[u] > self.rhs[u]:  # 过一致
                self.g[u] = self.rhs[u]
                self.U.remove(u)
                pred = self.get_neighbors(u)
                for s in pred:
                    if s != self.s_goal:
                        self.rhs[s] = min(self.rhs[s], self.c(s, u) + self.g[u])
                    self.update_vertex(s)
            else:  # 欠一致
                g_old = self.g[u]
                self.g[u] = float('inf')
                pred = self.get_neighbors(u)
                for s in pred + [u]:
                    if self.rhs[s] == self.c(s, u) + g_old:
                        if s != self.s_goal:
                            succ = self.get_neighbors(s)
                            self.rhs[s] = min([self.c(s, s_) + self.g[s_] for s_ in succ])
                    self.update_vertex(s)
        # self.draw_rhs(self.rhs)




    def _planning(self, s_start, s_goal, dyna_obs, debug=False):
        '''
            规划路径(实际实现)
            Args:
                dyna_obs: 动态障碍物位置列表
                step_num: 单次移动步数
        '''
        # 确保目标合法
        if not self.in_bounds_without_obstacle(s_goal):
            return []
        # 第一次规划需要初始化rhs并将goal加入队列，计算最短路径
        if self.s_goal is None:
            self.s_start = tuple(s_start)
            self.s_goal = tuple(s_goal)
            self.s_last = tuple(s_start)
            self.rhs[tuple(s_goal)] = 0
            self.U.insert(tuple(s_goal), Priority(k1=heuristic(tuple(s_start), tuple(s_goal)), k2=0))
            changed_pos = self.update_map(dyna_obs=dyna_obs)
            if changed_pos:
                self.update_cost_map(changed_pos)
            self.compute_shortest_path()  # 计算最短路径
            self.path = self.get_path()
            return self.path
        # 后续规划只更新起点，直接使用原路径(去掉已走过部分)
        else:
            self.s_start = tuple(s_start)
            # 根据obs更新map, cost_map, edge_cost
            changed_pos = self.update_map(dyna_obs=dyna_obs)
            if changed_pos:
                self.update_cost_map(changed_pos)
                self.update_edge_costs(changed_pos)
                # 若地图改变，重新计算最短路径
                self.compute_shortest_path()
                self.path = self.get_path()
            return self.path

    def planning(self, s_start, s_goal, dyna_obs, debug=False):
        '''
            路径规划(供外部调用，处理实际坐标和地图坐标的转换)
        '''
        # 实际坐标 -> 地图坐标
        s_start = self.real2map(s_start)
        if self.s_goal is None:
            s_goal = self.real2map(s_goal)
        else:
            s_goal = self.s_goal
        dyna_obs = [self.real2map(obs, reachable_assurance=False) for obs in dyna_obs]

        self._planning(s_start, s_goal, dyna_obs, debug)

        # 地图坐标->实际坐标
        path = [self.map2real(node) for node in self.path]
        return path

    def get_path(self):
        '''
            得到路径
            Args:
                step_num: 路径步数
            return:
                path: [(x, y), ...]
        '''
        if self.s_start is None or self.s_goal == self.s_start:
            return []
        path = []
        cur = self.s_start
        for i in range(self.max_path_length):
            succ = [s_ for s_ in self.get_neighbors(cur)]
            cur = succ[np.argmin([self.c(cur, s_) + self.g[s_] + 20*(s_ in path) for s_ in succ])]  # 避免抖动 (走重复的点会有惩罚)
            # print(cur)
            path.append(cur)
            if cur == self.s_goal:
                while cur in self.dyna_obs_occupy:  # 确保目标未在dyna_obs范围中
                    cur = path.pop()
                break
        return path

    def in_bounds_without_obstacle(self, pos):
        '''
            判断位置在地图范围内 且 不是静态障碍物
        '''
        (x, y) = pos
        return 0 <= x < self.X and 0 <= y < self.Y and self.map[x, y] != self.object_to_idx["obstacle"]

    def get_neighbors(self, pos, mode=8):
        '''
            获取邻居节点, 地图范围内
        '''
        (x_, y_) = pos
        neighbors = [(x_ + 1, y_), (x_ - 1, y_), (x_, y_ + 1), (x_, y_ - 1), (x_ + 1, y_ + 1), (x_ - 1, y_ + 1),
                     (x_ + 1, y_ - 1), (x_ - 1, y_ - 1)]
        neighbors = filter(self.in_bounds_without_obstacle, neighbors)  # 确保位置在地图范围内 且 不是静态障碍物
        return list(neighbors)

    def compute_cost_map(self):
        # 计算当前地图的cost_map
        self.cost_map = np.zeros_like(self.map)
        for idx, obj in self.idx_to_object.items():
            self.cost_map[self.map == idx] = self.object_to_cost[obj]

        # 扩张静态障碍物影响范围
        obs_pos = np.where(self.map == self.object_to_idx['obstacle'])  # 静态障碍物位置列表
        for (x, y) in zip(obs_pos[0], obs_pos[1]):
            start_x, end_x = max(x - 1, 0), min(x + 1, self.X - 1)
            start_y, end_y = max(y - 1, 0), min(y + 1, self.Y - 1)
            for cost in range(9, 0, -3):
                for x_ in range(start_x, end_x + 1):
                    self.cost_map[x_, start_y] = max(self.cost_map[x_, start_y], cost)
                for y_ in range(start_y + 1, end_y + 1):
                    self.cost_map[end_x, y_] = max(self.cost_map[end_x, y_], cost)
                for x_ in range(end_x - 1, start_x - 1, -1):
                    self.cost_map[x_, end_y] = max(self.cost_map[x_, end_y], cost)
                for y_ in range(end_y - 1, start_y, -1):
                    self.cost_map[start_x, y_] = max(self.cost_map[start_x, y_], cost)
                start_x, end_x = max(start_x - 1, 0), min(end_x + 1, self.X - 1)
                start_y, end_y = max(start_y - 1, 0), min(end_y + 1, self.Y - 1)

        self.cost_background = self.cost_map.copy()

    def update_map(self, dyna_obs):
        '''
            更新地图 和 动态障碍物列表
            Args:
                dyna_obs: 当前动态障碍物位置列表 [(x,y), ...]
            return:
                update_obj: 改变的位置列表 [(x, y, obj_idx, cost_old), ...]
        '''
        # dyna_obs没有变化 (集合set可以忽略元素在列表中的位置) 且 robot未在dyna_obs占用位置中
        if set(dyna_obs) == set(self.dyna_obs_list) and self.s_start not in self.dyna_obs_occupy:
            return []

        # 当前dyna_obs占用位置列表
        dyna_obs_occupy = []
        for pos in dyna_obs:
            dyna_obs_occupy.extend(self.get_occupy_pos(pos))
        dyna_obs_occupy = [pos for i, pos in enumerate(dyna_obs_occupy) if pos not in dyna_obs_occupy[:i]]  # 去除重复位置
        # 转变为free 和 转变为dyna_obs的位置列表
        changed_free = [pos for pos in self.dyna_obs_occupy if pos not in dyna_obs_occupy]
        changed_obs = [pos for pos in dyna_obs_occupy if pos not in self.dyna_obs_occupy]

        # 更新地图，计算changed_pos
        changed_pos = []
        for (x, y) in changed_free:
            self.map[x, y] = self.object_to_idx['free']
            changed_pos.append((x, y, self.object_to_idx["free"], self.cost_map[x, y]))
            # changed_pos.append((x, y, self.object_to_idx["free"], self.object_to_idx["dynamic obstacle"]))
        for (x, y) in changed_obs:
            self.map[x, y] = self.object_to_idx['dynamic obstacle']
            changed_pos.append((x, y, self.object_to_idx["dynamic obstacle"], self.cost_map[x, y]))
            # changed_pos.append((x, y, self.object_to_idx["dynamic obstacle"], self.object_to_idx["free"]))

        # 更新dyna_obs 位置列表 和 占用位置列表
        self.dyna_obs_list = dyna_obs
        self.dyna_obs_occupy = dyna_obs_occupy

        return changed_pos

    def get_occupy_pos(self, obs_pos):
        '''
            根据dyna_obs中心位置，计算其占用的所有网格位置
        '''
        (x, y) = obs_pos
        occupy_radius = min(self.dyna_obs_radius,
                            int(euclidean_distance(obs_pos, self.s_start) - 1))  # 避免robot被dyna_obs的占用区域包裹住
        # 圆形区域
        occupy_pos = [(i, j) for i in range(x - occupy_radius, x + occupy_radius + 1)
                      for j in range(y - occupy_radius, y + occupy_radius + 1)
                      if euclidean_distance((i, j), obs_pos) < occupy_radius]
        # # 等边三角形区域 TODO: 效果不及预期(三角形棱角容易导致robot卡住)
        # triangle_occupy = self.triangle_occupy(obs=obs_pos, occupy_radius=occupy_radius)
        # occupy_pos = [(i, j) for i in range(x - occupy_radius, x + occupy_radius + 1)
        #               for j in range(y - occupy_radius, y + occupy_radius + 1)
        #               if triangle_occupy.contains_point((i, j))]
        occupy_pos = filter(self.in_bounds_without_obstacle, occupy_pos)  # 确保位置在地图范围内 且 不是静态障碍物
        return list(occupy_pos)

    def update_cost_map(self, changed_pos):
        '''
            更新cost_map
            Args:
                changed_pos: 改变的位置列表 [x, y, idx]
        '''
        for (x, y, idx, _) in changed_pos:
            if self.idx_to_object[idx] == 'free':  # 空位的cost取决于离障碍物的距离
                self.cost_map[x, y] = self.cost_background[x, y]
            else:
                self.cost_map[x, y] = self.object_to_cost[self.idx_to_object[idx]]

    def update_edge_costs(self, changed_pos):
        '''
            重新计算edge_cost，更新受影响节点的rhs
            Args:
                changed_pos: 改变的位置列表 [(x, y, obj_idx_new, obj_idx_old)]
        '''
        if not changed_pos: return
        self.k_m += heuristic(self.s_last, self.s_start, name='euclidean')  # 使用欧式距离 更新km
        self.s_last = self.s_start
        for pos in changed_pos:
            v = (pos[0], pos[1])  # to pos
            c_old = pos[3]  # 位置v的旧cost
            pred_v = self.get_neighbors(v)
            for u in pred_v:
                c_old = self.c(u, v, c_old=c_old)
                c_new = self.c(u, v)
                if c_old > c_new and u != self.s_goal:
                    self.rhs[u] = min(self.rhs[u], c_new + self.g[v])
                elif self.rhs[u] == c_old + self.g[v] and u != self.s_goal:
                    succ_u = self.get_neighbors(u)
                    self.rhs[u] = min([self.c(u, s_) + self.g[s_] for s_ in succ_u])
                self.update_vertex(u)

    def map2real(self, pos):
        '''
            地图坐标->实际坐标
        '''
        x = pos[0] * self.scale_ratio + self.x_min
        y = pos[1] * self.scale_ratio + self.y_min
        return tuple((x, y))

    def real2map(self, pos, reachable_assurance=True):
        '''
            实际坐标->地图坐标
        '''
        x = round((pos[0] - self.x_min) / self.scale_ratio)
        y = round((pos[1] - self.y_min) / self.scale_ratio)
        # 确保点不在静态障碍物上，否则就不断向外圈扩展直到找到非静态障碍物位置
        if reachable_assurance:
            return self.validate_pos((x, y))
        else:
            return tuple((x, y))

    def validate_pos(self, pos):
        '''
            对于不合法的pos，找到周围距离最近的合法坐标
        '''
        (x, y) = pos
        x = max(0, min(x, self.X - 1))
        y = max(0, min(y, self.Y - 1))
        if self.idx_to_object[self.map[x, y]] == 'obstacle':
            start_x, end_x = max(x - 1, 0), min(x + 1, self.X - 1)
            start_y, end_y = max(y - 1, 0), min(y + 1, self.Y - 1)
            while True:
                for x_ in range(start_x, end_x + 1):
                    if self.idx_to_object[self.map[x_, start_y]] != 'obstacle':
                        return tuple((x_, start_y))
                for y_ in range(start_y + 1, end_y + 1):
                    if self.idx_to_object[self.map[end_x, y_]] != 'obstacle':
                        return tuple((end_x, y_))
                for x_ in range(end_x - 1, start_x - 1, -1):
                    if self.idx_to_object[self.map[x_, end_y]] != 'obstacle':
                        return tuple((x_, end_y))
                for y_ in range(end_y - 1, start_y, -1):
                    if self.idx_to_object[self.map[start_x, y_]] != 'obstacle':
                        return tuple((start_x, y_))
                start_x, end_x = max(start_x - 1, 0), min(end_x + 1, self.X - 1)
                start_y, end_y = max(start_y - 1, 0), min(end_y + 1, self.Y - 1)
            # raise Exception('invalid pos!')
        return tuple((x, y))

    def draw_graph(self, step_num, yaw):
        '''
        Args:
            step_num: 移动步数
            yaw:      robot朝向 (弧度)
        '''
        # 清空当前figure内容，保留figure对象
        plt.clf()
        # for stopping simulation with the esc key. 按esc结束
        plt.gcf().canvas.mpl_connect(
            'key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])

        # 缩放坐标偏移量
        offset = (self.x_min / self.scale_ratio, self.x_max / self.scale_ratio,
                  self.y_min / self.scale_ratio, self.y_max / self.scale_ratio)
        start = (self.s_start[0] + offset[0], self.s_start[1] + offset[2])
        goal = (self.s_goal[0] + offset[0], self.s_goal[1] + offset[2])

        # 画地图: X行Y列，第一行在下面
        # 范围: 横向Y[-80,290] 纵向X[-70,120]
        plt.imshow(self.map, cmap='binary', alpha=0.5, origin='lower',
                   extent=(offset[2], offset[3],
                           offset[0], offset[1]))
        # 画起点和目标
        plt.plot(start[1], start[0], 'x', color='r')
        plt.plot(goal[1], goal[0], 'x', color='darkorange')

        # 画搜索路径
        plt.plot([y + offset[2] for (x, y) in self.path],
                 [x + offset[0] for (x, y) in self.path], "-g")

        # 画移动路径
        next_step = min(step_num, len(self.path))
        plt.plot([start[1], self.path[next_step - 1][1] + offset[2]],
                 [start[0], self.path[next_step - 1][0] + offset[0]], "-r")
        # plt.plot([y + offset[2] for (x, y) in self.path[:next_step]],
        #          [x + offset[0] for (x, y) in self.path[:next_step]], "-r")

        # 画感应半径和观测范围
        self.plot_circle(start[1], start[0], self.react_radius, 'lightgrey')
        if yaw is not None:
            plt.plot([start[1], start[1] + self.react_radius * (math.sin(yaw + self.vision_radius))],
                     [start[0], start[0] + self.react_radius * (math.cos(yaw + self.vision_radius))], "aqua", linewidth=1)
            plt.plot([start[1], start[1] + self.react_radius * (math.sin(yaw - self.vision_radius))],
                     [start[0], start[0] + self.react_radius * (math.cos(yaw - self.vision_radius))], "aqua", linewidth=1)

        plt.xlabel('y', loc='right')
        plt.ylabel('x', loc='top')
        plt.grid(color='black', linestyle='-', linewidth=0.5)
        plt.show()

    def draw_rhs(self, rhs):
        # 画地图: X行Y列，第一行在下面

        # 缩放坐标偏移量
        offset = (self.x_min / self.scale_ratio, self.x_max / self.scale_ratio,
                  self.y_min / self.scale_ratio, self.y_max / self.scale_ratio)

        # 将无穷大位置的值替换为指定的颜色
        # rhs[np.isinf(rhs)] = np.nan

        # 将无穷大位置的值替换为 np.nan
        rhs = np.ma.masked_invalid(rhs)

        # 设置颜色映射范围
        vmin = np.nanmin(rhs)
        vmax = np.nanmax(rhs)


        # 创建一个图形对象
        fig, ax = plt.subplots()

        # cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', ['#0000FF', '#FFFFFF'])

        # 绘制热力图
        heatmap = ax.imshow(rhs, cmap='jet',  vmin=vmin, vmax=vmax, origin='lower',
                            extent=(offset[2], offset[3],
                                    offset[0], offset[1]))
        # 添加颜色条
        plt.colorbar(heatmap)

        start = (self.s_start[0] + offset[0], self.s_start[1] + offset[2])
        goal = (self.s_goal[0] + offset[0], self.s_goal[1] + offset[2])

        # 画起点和目标
        plt.plot(start[1], start[0], 'x', color='black')
        plt.plot(goal[1], goal[0], 'x', color='darkorange')


        # 设置图形标题和轴标签
        ax.set_title('Heatmap(G)')
        ax.set_xlabel('y', loc='right')
        ax.set_ylabel('x', loc='top')
        ax.grid(color='black', linestyle='-', linewidth=0.5)
        # 显示图形
        plt.show()




    @staticmethod
    def plot_circle(y, x, size, color="lightgrey"):  # pragma: no cover
        '''
            以(x,y)为圆心，size为半径 画圆
        '''
        deg = list(range(0, 360, 5))
        deg.append(0)
        yl = [y + size * math.cos(np.deg2rad(d)) for d in deg]
        xl = [x + size * math.sin(np.deg2rad(d)) for d in deg]
        plt.plot(yl, xl, color)

    def triangle_occupy(self, obs, occupy_radius):
        '''
            计算等边三角形的三个顶点并返回三角形对象
            TODO: 效果不及预期
        Args:
            obs:           三角形底边中点
            occupy_radius: 三角形的高
        '''
        dist = euclidean_distance(self.s_start, obs)
        # obs(底边中点)的坐标
        x1, y1 = obs
        # 顶点A的坐标
        x2 = x1 + occupy_radius * ((self.s_start[0] - x1) / dist)
        y2 = y1 + occupy_radius * ((self.s_start[1] - y1) / dist)

        # 计算向量AP的坐标
        AP_x = x1 - x2
        AP_y = y1 - y2
        # 计算向量AB的坐标
        AB_x = AP_x * math.cos(math.pi / 6) - AP_y * math.sin(math.pi / 6)
        AB_y = AP_x * math.sin(math.pi / 6) + AP_y * math.cos(math.pi / 6)
        # 计算向量AC的坐标
        AC_x = AP_x * math.cos(math.pi / 6) + AP_y * math.sin(math.pi / 6)
        AC_y = -AP_x * math.sin(math.pi / 6) + AP_y * math.cos(math.pi / 6)

        # 计算顶点B的坐标
        x3 = x2 + AB_x
        y3 = y2 + AB_y
        # 计算顶点C的坐标
        x4 = x2 + AC_x
        y4 = y2 + AC_y

        ver1 = (x2, y2)
        ver2 = (x3, y3)
        ver3 = (x4, y4)

        return Polygon([ver1, ver2, ver3], closed=True, fill=True)
