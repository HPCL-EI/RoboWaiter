import math
import sys

import numpy as np


# from rrt import RRT
# from rrt_star import RRTStar


# def real2map(min_x, min_y, scale_ratio, x, y):
#     '''
#         实际坐标->地图坐标 (向下取整)
#     '''
#     # x = round((x - self.min_x) / self.scale_ratio)
#     # y = round((y - self.min_y) / self.scale_ratio)
#     x = math.floor((x - min_x) / scale_ratio)
#     y = math.floor((y - min_y) / scale_ratio)
#     return x, y


def getDistance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def getNearestFrontier(cur_pos, frontiers):
    dis_min = sys.maxsize
    frontier_best = None
    for frontier in frontiers:
        dis = getDistance(frontier, cur_pos)
        if dis <= dis_min:
            dis_min = dis
            frontier_best = frontier
    return frontier_best


class Explore:
    def __init__(self, _explore_range):
        self.explore_range = _explore_range  # 机器人感知范围（以机器人为中心，边长为2 * _explore_range的正方形）
        self.visited = set()
        self.all_frontier_list = set()

    def explore(self, cur_pos):
        for i in range(cur_pos[0] - self.explore_range, cur_pos[0] + self.explore_range + 1):
            for j in range(cur_pos[1] - self.explore_range, cur_pos[1] + self.explore_range + 1):
                # if self.isOutMap((i, j)):
                #     continue
                # x, y = real2map(self.area_range[0], self.area_range[2], self.scale_ratio, i, j)
                # if self.map[x, y] == 0:
                if self.reachable((i, j)):
                    self.visited.add((i, j))
        for i in range(cur_pos[0] - self.explore_range, cur_pos[0] + self.explore_range + 1):
            for j in range(cur_pos[1] - self.explore_range, cur_pos[1] + self.explore_range + 1):
                # if self.isOutMap((i, j)):
                #     continue
                # x, y = real2map(self.area_range[0], self.area_range[2], self.scale_ratio, i, j)
                if self.reachable((i, j)):
                    if self.isNewFrontier((i, j)):
                        self.all_frontier_list.add((i, j))
        if len(self.all_frontier_list) == 0:
            free_list = list(self.visited)
            free_array = np.array(free_list)
            print(f"探索完成！以下是场景中可以到达的点：{free_array}；其余点均是障碍物不可达")
            return None
        return getNearestFrontier(cur_pos, self.all_frontier_list)

    def isNewFrontier(self, pos):
        around_nodes = [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]

        for node in around_nodes:
            if node not in self.visited and self.reachable(node):
                return True
        if (pos[0], pos[1]) in self.all_frontier_list:
            self.all_frontier_list.remove((pos[0], pos[1]))
        return False

    def reachable(self, pos):
        # x, y = real2map(self.area_range[0], self.area_range[2], self.scale_ratio, pos[0], pos[1])
        # if self.map[x, y] == 1:
        #     return True
        # else:
        #     return False

        # TODO: 调用reachable_check函数
        pass

    # def isOutMap(self, pos):
    #     if pos[0] <= self.area_range[0] or pos[0] >= self.area_range[1] or pos[1] <= self.area_range[2] or pos[1] >= \
    #             self.area_range[3]:
    #         return True
    #     return False
