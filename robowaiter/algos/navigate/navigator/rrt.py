"""

Path planning Sample Code with Randomized Rapidly-Exploring Random Trees (RRT)

author: AtsushiSakai(@Atsushi_twi)

"""

import math
import random
import matplotlib.pyplot as plt
import numpy as np
from pathsmoothing import get_path_length, get_target_point

show_animation = True


class RRT:
    """
    Class for RRT planning
    """

    class Node:
        """
        RRT Node
        """

        def __init__(self, x=0.0, y=0.0):
            self.x = x
            self.y = y
            self.path_x = []  # Node 到 parent 间的路径链
            self.path_y = []
            self.parent = None

    class AreaBounds:

        def __init__(self, area):
            self.xmin = float(area[0])
            self.xmax = float(area[1])
            self.ymin = float(area[2])
            self.ymax = float(area[3])

    def __init__(self,
                 rand_area,  # 横纵坐标的采样范围 [minx,maxx,miny,maxy]
                 map,  # 离散化地图
                 scale_ratio=5,  # 地图缩放率
                 expand_dis=200,  # 最大扩展距离
                 path_resolution=10.0,  # 路径链分辨率
                 goal_sample_rate=5,  # 5%的几率采样到目标点
                 max_iter=500,
                 robot_radius=12.0,  # robot身位半径
                 ):

        self.map = map
        self.scale_ratio = scale_ratio
        self.start = self.Node(0, 0)
        self.goal = self.Node(0, 0)
        (self.min_x, self.max_x, self.min_y, self.max_y) = rand_area
        # self.play_area = self.AreaBounds(rand_area)  # 采样区域(边界框启发式)
        self.play_area = None
        self.expand_dis = expand_dis
        self.path_resolution = path_resolution
        self.goal_sample_rate = goal_sample_rate
        self.max_iter = max_iter
        self.node_list = []
        self.robot_radius = robot_radius

    def reset(self):
        '''
            重置rrt的变量和数据结构
        '''
        self.node_list.clear()
        self.start = self.Node(0, 0)
        self.goal = self.Node(0, 0)

    def update_play_area(self):
        '''
            更新采样区域
        '''
        if self.goal.x > self.start.x:
            self.play_area.xmin = self.start.x
            self.play_area.xmax = self.max_x
        else:
            self.play_area.xmin = self.min_x
            self.play_area.xmax = self.start.x
        if self.goal.y > self.start.y:
            self.play_area.ymin = self.start.y
            self.play_area.ymax = self.max_y
        else:
            self.play_area.ymin = self.min_y
            self.play_area.ymax = self.start.y

    def planning(self, start, goal, path_smoothing=True, animation=False):
        """
        rrt path planning, return a path list

        animation: flag for animation on or off
        """
        (self.start.x, self.start.y) = start
        (self.goal.x, self.goal.y) = goal
        # self.update_play_area()
        self.node_list = [self.start]  # 已经采样的节点列表
        for i in range(self.max_iter):
            rnd_node = self.get_random_node()  # 随机采样节点
            nearest_ind = self.get_nearest_node_index(self.node_list, rnd_node)
            nearest_node = self.node_list[nearest_ind]  # node_list中距离新采样点最近的节点

            new_node = self.steer(nearest_node, rnd_node, self.expand_dis)

            # 确保新采样节点在范围内且不是障碍物
            if self.check_if_outside_play_area(new_node, self.play_area) and \
                    self.check_collision(new_node):
                self.node_list.append(new_node)

            if animation and i % 5 == 0:
                self.draw_graph(rnd_node)

            if self.calc_dist_to_goal(self.node_list[-1].x,
                                      self.node_list[-1].y) <= self.expand_dis:
                final_node = self.steer(self.node_list[-1], self.goal,
                                        self.expand_dis)
                if self.check_collision(final_node):
                    path = self.generate_final_course(len(self.node_list) - 1)
                    if path_smoothing:
                        return self.path_smoothing(path)
                    else:
                        return path

            if animation and i % 5:
                self.draw_graph(rnd_node)

        return None  # cannot find path

    def steer(self, from_node, to_node, extend_length=float("inf")):
        '''
            返回from_node 到 to_node 距离限制内最远的节点，并设置其父节点为from_node
            并计算路径链
            Args:
                entend_length: 距离限制
            return:
                new_node: from_node 到 to_node 距离限制内最远的节点
                ( 如果 to_node 在距离限制内则返回 to_node )
        '''
        new_node = self.Node(from_node.x, from_node.y)
        d, theta = self.calc_distance_and_angle(new_node, to_node)  # from 和 to 之间的距离和方向角

        new_node.path_x = [new_node.x]
        new_node.path_y = [new_node.y]

        if extend_length > d:
            extend_length = d

        n_expand = math.floor(extend_length / self.path_resolution)  # from 和 to 之间的采样点数

        for _ in range(n_expand):
            new_node.x += self.path_resolution * math.cos(theta)
            new_node.y += self.path_resolution * math.sin(theta)
            new_node.path_x.append(new_node.x)
            new_node.path_y.append(new_node.y)

        d, _ = self.calc_distance_and_angle(new_node, to_node)
        if d <= self.path_resolution:
            new_node.path_x.append(to_node.x)
            new_node.path_y.append(to_node.y)
            new_node.x = to_node.x
            new_node.y = to_node.y

        new_node.parent = from_node

        return new_node

    def generate_final_course(self, goal_ind) -> [(float, float), ]:
        '''
            得到路径(起点->终点)
        '''
        path = [(self.goal.x, self.goal.y)]
        node = self.node_list[goal_ind]
        while node.parent is not None:
            path.append((node.x, node.y))
            node = node.parent
        path.append((node.x, node.y))
        path.reverse()
        return path

    def calc_dist_to_goal(self, x, y):
        '''
            计算节点到终点距离
        '''
        dx = x - self.goal.x
        dy = y - self.goal.y
        return math.hypot(dx, dy)

    def get_random_node(self):
        '''
            在规定范围内随机采样节点(一定概率采样到目标节点)
        '''
        if random.randint(0, 100) > self.goal_sample_rate:
            rnd = self.Node(
                random.uniform(self.min_x, self.max_x),
                random.uniform(self.min_y, self.max_y))
        else:  # goal point sampling
            rnd = self.Node(self.goal.x, self.goal.y)  # 返回goal
        return rnd

    def map2real(self, x, y):
        '''
            地图坐标->实际坐标
        '''
        x = x * self.scale_ratio + self.min_x
        y = y * self.scale_ratio + self.min_y
        return x, y

    def real2map(self, x, y):
        '''
            实际坐标->地图坐标 (向下取整)
        '''
        # x = round((x - self.min_x) / self.scale_ratio)
        # y = round((y - self.min_y) / self.scale_ratio)
        x = math.floor((x - self.min_x) / self.scale_ratio)
        y = math.floor((y - self.min_y) / self.scale_ratio)
        return x, y

    def check_collision(self, node):
        '''
            判断 node 到 父节点之间 是否有障碍物
        '''

        if node is None:
            return False
        for (x, y) in zip(node.path_x, node.path_y):
            map_x, map_y = self.real2map(x, y)
            # TODO: 碰撞检测考虑robot_radius和scale_ratio
            if self.map[map_x, map_y] or self.map[map_x + 1, map_y] or \
                    self.map[map_x, map_y + 1] or self.map[map_x + 1, map_y + 1]:
                return False
        return True  # safe

    def draw_graph(self, new=None, final_path=None):
        # 清空当前figure内容，保留figure对象
        plt.clf()
        # for stopping simulation with the esc key. 按esc结束
        plt.gcf().canvas.mpl_connect(
            'key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])

        # 画地图: X行Y列，第一行在下面
        # 范围: 横向Y[-70,120] 纵向X[-80,290]
        plt.imshow(self.map, cmap='binary', alpha=0.5, origin='lower',
                   extent=(self.min_y / self.scale_ratio, self.max_y / self.scale_ratio,
                           self.min_x / self.scale_ratio, self.max_x / self.scale_ratio))
        # 画新采样点
        if new is not None:
            (scale_x, scale_y) = (new.x / self.scale_ratio, new.y / self.scale_ratio)
            plt.plot(scale_y, scale_x, "^k")
            if self.robot_radius > 0.0:
                self.plot_circle(scale_y, scale_x, self.robot_radius / self.scale_ratio, '-r')
            # 画新边
            if new.parent:
                plt.plot([y / self.scale_ratio for y in new.path_y],
                         [x / self.scale_ratio for x in new.path_x], "-g")

        # 画整个搜索树
        for node in self.node_list:
            if node.parent:
                plt.plot([y / self.scale_ratio for y in node.path_y],
                         [x / self.scale_ratio for x in node.path_x], "-g")
        # 画起点和目标
        plt.plot(self.start.y / self.scale_ratio, self.start.x / self.scale_ratio, "xr")
        plt.plot(self.goal.y / self.scale_ratio, self.goal.x / self.scale_ratio, "xr")

        plt.xlabel('y', loc='right')
        plt.ylabel('x', loc='top')
        plt.grid(color='black', linestyle='-', linewidth=0.5)
        plt.pause(0.2)

        # 画最终路径
        if final_path:
            plt.plot([y / self.scale_ratio for (x, y) in final_path],
                     [x / self.scale_ratio for (x, y) in final_path], '-r')  # 画出最终路径
            plt.pause(2)

    @staticmethod
    def plot_circle(x, y, size, color="-b"):  # pragma: no cover
        '''
            以(x,y)为圆心，size为半径 画圆
        '''
        deg = list(range(0, 360, 5))
        deg.append(0)
        xl = [x + size * math.cos(np.deg2rad(d)) for d in deg]
        yl = [y + size * math.sin(np.deg2rad(d)) for d in deg]
        plt.plot(xl, yl, color)

    @staticmethod
    def get_nearest_node_index(node_list, rnd_node):
        '''
            得到距离rnd_node最近的节点编号
        '''
        dlist = [(node.x - rnd_node.x) ** 2 + (node.y - rnd_node.y) ** 2
                 for node in node_list]
        minind = dlist.index(min(dlist))

        return minind

    @staticmethod
    def check_if_outside_play_area(node, play_area):

        if play_area is None:
            return True  # no play_area was defined, every pos should be ok

        if node.x < play_area.xmin or node.x > play_area.xmax or \
                node.y < play_area.ymin or node.y > play_area.ymax:
            return False  # outside - bad
        else:
            return True  # inside - ok

    @staticmethod
    def calc_distance_and_angle(from_node, to_node):
        '''
            计算2点间的距离和角度( 以from_node为原点 )
        '''
        dx = to_node.x - from_node.x
        dy = to_node.y - from_node.y
        d = math.hypot(dx, dy)  # 欧式距离
        theta = math.atan2(dy, dx)
        return d, theta

    # **************************Path Smoothing**************************************************** #
    # **************************Path Smoothing**************************************************** #
    # **************************Path Smoothing**************************************************** #

    def line_collision_check(self, first, second):
        '''
            检查first-second的直线是否穿过障碍物
            Args:
                path_resolution: 采样点分辨率
        '''
        x1 = first[0]
        y1 = first[1]
        x2 = second[0]
        y2 = second[1]
        path_x = [x1]
        path_y = [y1]
        # 计算距离和夹角
        dx = x2 - x1
        dy = y2 - y1
        d = math.hypot(dx, dy)  # 欧式距离
        theta = math.atan2(dy, dx)  # 夹角

        n_expand = math.floor(d / self.path_resolution)  # first 和 second 之间的采样点数
        for _ in range(n_expand):
            x1 += self.path_resolution * math.cos(theta)
            y1 += self.path_resolution * math.sin(theta)
            path_x.append(x1)
            path_y.append(y1)
        if d <= self.path_resolution:
            path_x.append(x2)
            path_y.append(y2)

        for (x, y) in zip(path_x, path_y):
            map_x, map_y = self.real2map(x, y)  # 向下取整
            # TODO: 碰撞检测考虑robot_radius和scale_ratio
            if self.map[map_x, map_y] or self.map[map_x + 1, map_y] or \
                    self.map[map_x, map_y + 1] or self.map[map_x + 1, map_y + 1]:
                return False

        return True

    def path_smoothing(self, path, max_iter=1000):
        '''
            输入原路径，输出平滑后的路径
            Args:
                path: [(x,y),...]
        '''
        le = get_path_length(path)

        for i in range(max_iter):
            # Sample two points
            pickPoints = [random.uniform(0, le), random.uniform(0, le)]  # 总路径长度中采样2个点
            pickPoints.sort()
            first = get_target_point(path, pickPoints[0])
            second = get_target_point(path, pickPoints[1])

            if first[2] <= 0 or second[2] <= 0:
                continue

            if (second[2] + 1) > len(path):
                continue

            if second[2] == first[2]:
                continue

            # collision check
            if not self.line_collision_check(first, second):
                continue

            # Create New path
            newPath = []
            newPath.extend(path[:first[2] + 1])
            newPath.append([first[0], first[1]])
            newPath.append([second[0], second[1]])
            newPath.extend(path[second[2] + 1:])
            path = newPath
            le = get_path_length(path)

        return path


def main(gx=6.0, gy=10.0):
    print("start " + __file__)

    # ====Search Path with RRT====
    obstacleList = [(5, 5, 1), (3, 6, 2), (3, 8, 2), (3, 10, 2), (7, 5, 2),
                    (9, 5, 2), (8, 10, 1)]  # [x, y, radius]
    # Set Initial parameters
    rrt = RRT(
        start=[0, 0],
        goal=[gx, gy],
        rand_area=[-2, 15],
        obstacle_list=obstacleList,
        # play_area=[0, 10, 0, 14]
        robot_radius=0.8
    )
    path = rrt.planning(animation=show_animation)

    if path is None:
        print("Cannot find path")
    else:
        print("found path!!")

        # Draw final path
        if show_animation:
            rrt.draw_graph()  # 画出探索过程
            plt.plot([x for (x, y) in path], [y for (x, y) in path], '-r')  # 画出最终路径
            plt.grid(True)
            plt.pause(0.01)
            plt.show()


if __name__ == '__main__':
    main()
