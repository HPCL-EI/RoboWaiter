'''
基于两个D* lite的实现
按照原始算法的伪代码
自己写的D* lite
'''

import math
import queue
from functools import partial
import numpy as np
import heapq

from matplotlib import pyplot as plt


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
                 map: np.array([int, int]),  # [X, Y]
                 area_range,  # [x_min, x_max, y_min, y_max] 实际坐标范围
                 scale_ratio=5,  # 地图缩放率
                 dyna_obs_radius=30,  # dyna_obs实际身位半径
                 ):

        # self.area_bounds = area
        self.map = map
        self.background = map.copy()
        self.X = map.shape[0]
        self.Y = map.shape[1]
        (self.x_min, self.x_max, self.y_min, self.y_max) = area_range
        self.scale_ratio = scale_ratio

        self.dyna_obs_list = []  # dyna_obs位置列表 [(x, y)]
        self.dyna_obs_radius = math.floor(dyna_obs_radius / scale_ratio)  # dyna_obs缩放后身位半径
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
            "dynamic obstacle": 100
        }
        self.cost_map = np.zeros_like(self.map)
        self.cost_background = self.cost_map.copy()
        self.compute_cost_map()

        self.s_start = None  # (int,int) 必须是元组(元组可以直接当作矩阵索引)
        self.s_goal = None  # (int,int)
        self.s_last = None  # (int,int)
        self.U = PriorityQueue()
        self.k_m = 0
        self.rhs = np.ones((self.X, self.Y)) * np.inf
        self.g = self.rhs.copy()
        self.path = []

    # def set_map(self, map_):
    #     '''
    #         设置map 和 cost_map
    #     '''
    #     self.map = map_
    #     self.X = map_.shape[0]
    #     self.Y = map_.shape[1]
    #     self.compute_cost_map()

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

    def c(self, u: (int, int), v: (int, int), v_old=None) -> float:
        '''
        计算节点间的 路径代价 和 目标位置代价 (目标位置代价为0时采用路径代价)
        (因为是终点->起点的扩展方向，因此v是node，u是v扩展的neighbor)
        Args:
            u:     from pos
            v:     to pos
            v_old: 指定的v的类型
        '''
        if v_old:
            obj_cost = self.object_to_cost[v_old]
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
        while self.U.top_key() < self.calculate_key(self.s_start) or self.rhs[self.s_start] > self.g[self.s_start]:
            u = self.U.top()
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
        # TODO: 误差抖动使robot没有到达路径上的点，导致新起点的rhs=∞，可能导致get_path失败 ( 当前版本没有该问题 )
        # assert (self.rhs[self.s_start] != float('inf')), "There is no known path!"
        # # debug
        # if debug:
        #     pass

    def planning(self, s_start, s_goal, dyna_obs, debug=False):
        '''
            路径规划(供外部调用，处理实际坐标和地图坐标的转换)
        '''
        # 实际坐标 -> 地图坐标
        s_start = self.real2map(s_start)
        s_goal = self.real2map(s_goal)
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
        while cur != self.s_goal:
            succ = [s_ for s_ in self.get_neighbors(cur) if s_ not in path]  # 避免抖动 (不可走重复的点)
            cur = succ[np.argmin([self.c(cur, s_) + self.g[s_] for s_ in succ])]
            path.append(cur)
        # else:
        #     for i in range(step_num):
        #         if cur == self.s_goal:
        #             break
        #         succ = self.get_neighbors(cur)
        #         cur = succ[np.argmin([self.c(cur, s_) + self.g[s_] for s_ in succ])]
        #         path.append(cur)
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
        # results = [(x_+1,y_), (x_-1,y_), (x_, y_+1), (x_,y_-1)]
        # if mode == 8:
        neighbors = [(x_ + 1, y_), (x_ - 1, y_), (x_, y_ + 1), (x_, y_ - 1), (x_ + 1, y_ + 1), (x_ - 1, y_ + 1),
                     (x_ + 1, y_ - 1), (x_ - 1, y_ - 1)]
        neighbors = filter(self.in_bounds_without_obstacle, neighbors)  # 确保位置在地图范围内 且 不是静态障碍物
        return list(neighbors)

    def compute_cost_map(self):
        # 计算当前地图的cost_map
        for idx, obj in self.idx_to_object.items():
            self.cost_map[self.map == idx] = self.object_to_cost[obj]

        # # TODO
        # for x in range(self.X):
        #     for y in range(self.Y):
        #         if self.cost_map[x, y] > 0:
        #             neighbors = self.get_neighbors((x, y))
        #             for (x_, y_) in neighbors:
        #                 self.cost_map[x_, y_] = max(self.cost_map[x_, y_], self.cost_map[x, y] - 10)


        self.cost_background = self.cost_map.copy()

    def update_map(self, dyna_obs):
        '''
            更新地图 和 动态障碍物列表
            Args:
                dyna_obs: 当前动态障碍物位置列表 [(x,y), ...]
            return:
                update_obj: 改变的位置列表 [(x, y, obj_idx, obj_idx_old), ...]
        '''
        # dyna_obs没有变化 (集合set可以忽略元素在列表中的位置)
        if set(dyna_obs) == set(self.dyna_obs_list):
            return []

        # 当前dyna_obs占用位置列表
        dyna_obs_occupy = []
        for pos in dyna_obs:
            dyna_obs_occupy.extend(self.get_occupy_pos(pos))
        dyna_obs_occupy = [pos for i, pos in enumerate(dyna_obs_occupy) if pos not in dyna_obs_occupy[:i]]  # 去除重复位置
        # 转变为free 和 转变为obs的位置列表
        changed_free = [pos for pos in self.dyna_obs_occupy if pos not in dyna_obs_occupy]
        changed_obs = [pos for pos in dyna_obs_occupy if pos not in self.dyna_obs_occupy]

        # # 新旧dyna_obs占用位置列表
        # old_obs_occupy = []
        # new_obs_occupy = []
        # for pos in self.dyna_obs_list:
        #     old_obs_occupy.extend(self.get_occupy_pos(pos))
        # for pos in dyna_obs:
        #     new_obs_occupy.extend(self.get_occupy_pos(pos))
        # old_obs_occupy = [pos for i, pos in enumerate(old_obs_occupy) if pos not in old_obs_occupy[:i]]  # 去除重复位置
        # new_obs_occupy = [pos for i, pos in enumerate(new_obs_occupy) if pos not in new_obs_occupy[:i]]  # 去除重复位置
        #
        # # 转变为free 和 转变为obs的位置列表
        # changed_free = [pos for pos in old_obs_occupy if pos not in new_obs_occupy]
        # changed_obs = [pos for pos in new_obs_occupy if pos not in old_obs_occupy]

        # 更新地图，计算changed_pos
        changed_pos = []
        for (x, y) in changed_free:
            self.map[x, y] = self.object_to_idx['free']
            changed_pos.append((x, y, self.object_to_idx["free"], self.object_to_idx["dynamic obstacle"]))
        for (x, y) in changed_obs:
            self.map[x, y] = self.object_to_idx['dynamic obstacle']
            changed_pos.append((x, y, self.object_to_idx["dynamic obstacle"], self.object_to_idx["free"]))

        # 更新dyna_obs 位置列表 和 占用位置列表
        self.dyna_obs_list = dyna_obs
        self.dyna_obs_occupy = dyna_obs_occupy

        return changed_pos



    def get_occupy_pos(self, obs_pos):
        '''
            根据dyna_obs中心位置，计算其占用的所有网格位置
        '''
        (x, y) = obs_pos
        occupy_radius = min(self.dyna_obs_radius, int(euclidean_distance(obs_pos, self.s_start) - 1))  # 避免robot被dyna_obs的占用区域包裹住
        # for i in range(x - self.dyna_obs_radius, x + self.dyna_obs_radius + 1):  # 方形区域
        #     for j in range(y - self.dyna_obs_radius, y + self.dyna_obs_radius + 1):
        #         occupy_pos.append((i, j))
        occupy_pos = [(i, j) for i in range(x - occupy_radius, x + occupy_radius + 1)  # 圆形区域
                      for j in range(y - occupy_radius, y + occupy_radius + 1)
                      if euclidean_distance((i, j), obs_pos) < occupy_radius]

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
            v_old = self.idx_to_object[pos[3]]  # 位置v的旧类型
            pred_v = self.get_neighbors(v)
            for u in pred_v:
                c_old = self.c(u, v, v_old=v_old)
                c_new = self.c(u, v)
                if c_old > c_new and u != self.s_goal:
                    self.rhs[u] = min(self.rhs[u], self.c(u, v) + self.g[v])
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
        # 需要确保点可达
        if reachable_assurance and self.idx_to_object[self.map[x, y]] != 'free':
            print('1')
            x_ = math.floor((pos[0] - self.x_min) / self.scale_ratio)
            y_ = math.floor((pos[1] - self.y_min) / self.scale_ratio)
            candidates = [(x_, y_), (x_ + 1, y_), (x_, y_ + 1), (x_ + 1, y_ + 1)]
            for (x, y) in candidates:
                print(self.idx_to_object[self.map[x, y]])
                if self.idx_to_object[self.map[x, y]] == 'free':
                    print((x,y))
                    return tuple((x, y))
            raise Exception('error')
        else:
            return tuple((x, y))

    def draw_graph(self, step_num):
        # 清空当前figure内容，保留figure对象
        plt.clf()
        # for stopping simulation with the esc key. 按esc结束
        plt.gcf().canvas.mpl_connect(
            'key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])

        # 缩放坐标偏移量
        offset = (self.x_min / self.scale_ratio, self.x_max / self.scale_ratio,
                  self.y_min / self.scale_ratio, self.y_max / self.scale_ratio,)

        # 画地图: X行Y列，第一行在下面
        # 范围: 横向Y[-80,290] 纵向X[-70,120]
        plt.imshow(self.map, cmap='binary', alpha=0.5, origin='lower',
                   extent=(offset[2], offset[3],
                           offset[0], offset[1]))
        # 画起点和目标
        plt.plot(self.s_start[1] + offset[2], self.s_start[0] + offset[0], "xr")
        plt.plot(self.s_goal[1] + offset[2], self.s_goal[0] + offset[0], "xr")

        # 画搜索路径
        plt.plot([y + offset[2] for (x, y) in self.path],
                 [x + offset[0] for (x, y) in self.path], "-g")

        # 画移动路径
        next_step = min(step_num, len(self.path))
        # plt.plot([self.s_start[1] + offset[2], self.path[next_step-1][1] + offset[2]],
        #          [self.s_start[0] + offset[0], self.path[next_step-1][0] + offset[0]], "-r")
        plt.plot([y + offset[2] for (x, y) in self.path[:next_step]],
                 [x + offset[0] for (x, y) in self.path[:next_step]], "-r")

        plt.xlabel('y', loc='right')
        plt.ylabel('x', loc='top')
        plt.grid(color='black', linestyle='-', linewidth=0.5)
        plt.pause(0.2)
