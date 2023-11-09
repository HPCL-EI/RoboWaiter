"""

Path planning Sample Code with RRT with path smoothing

@author: AtsushiSakai(@Atsushi_twi)

"""

import math
import random
import matplotlib.pyplot as plt
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent))



def get_path_length(path):
    '''
        计算路径长度
    '''
    le = 0
    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        d = math.hypot(dx, dy)
        le += d

    return le


def get_target_point(path, targetL):
    le = 0
    ti = 0
    lastPairLen = 0
    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        d = math.hypot(dx, dy)
        le += d
        if le >= targetL:
            ti = i - 1
            lastPairLen = d
            break

    partRatio = (le - targetL) / lastPairLen

    x = path[ti][0] + (path[ti + 1][0] - path[ti][0]) * partRatio
    y = path[ti][1] + (path[ti + 1][1] - path[ti][1]) * partRatio

    return [x, y, ti]


# def line_collision_check(first, second, map, path_resolution=25.0, robot_radius=5, scale_ratio=5):
#     '''
#         检查first-second的直线是否穿过障碍物
#         Args:
#             path_resolution: 采样点分辨率
#     '''
#     x1 = first[0]
#     y1 = first[1]
#     x2 = second[0]
#     y2 = second[1]
#     path_x = [x1]
#     path_y = [y1]
#     # 计算距离和夹角
#     dx = x2 - x1
#     dy = y2 - y1
#     d = math.hypot(dx, dy)      # 欧式距离
#     theta = math.atan2(dy, dx)  # 夹角
#
#     n_expand = math.floor(d / path_resolution)  # first 和 second 之间的采样点数
#     for _ in range(n_expand):
#         x1 += path_resolution * math.cos(theta)
#         y1 += path_resolution * math.sin(theta)
#         path_x.append(x1)
#         path_y.append(y1)
#     if d <= path_resolution:
#         path_x.append(x2)
#         path_y.append(y2)
#
#     for (x, y) in zip(path_x, path_y):
#         (scale_x, scale_y) = (math.floor(x / scale_ratio), math.floor(y / scale_ratio))  # 向下取整
#         if robot_radius > scale_ratio:  # TODO: 根据robot_radius和scale_ratio选择不同的判断方式
#             if map[scale_x, scale_y] or map[scale_x + 1, scale_y] or \
#                     map[scale_x, scale_y + 1] or map[scale_x + 1, scale_y + 1]:  # 如果node周围的四个缩放坐标有障碍物
#                 return False
#     return True
#
#
# def path_smoothing(path, map, max_iter=1000):
#     '''
#         输入原路径，输出平滑后的路径
#         Args:
#             path: [(x,y),...]
#     '''
#     le = get_path_length(path)
#
#     for i in range(max_iter):
#         # Sample two points
#         pickPoints = [random.uniform(0, le), random.uniform(0, le)]  # 总路径长度中采样2个点
#         pickPoints.sort()
#         first = get_target_point(path, pickPoints[0])
#         second = get_target_point(path, pickPoints[1])
#
#         if first[2] <= 0 or second[2] <= 0:
#             continue
#
#         if (second[2] + 1) > len(path):
#             continue
#
#         if second[2] == first[2]:
#             continue
#
#         # collision check
#         if not line_collision_check(first, second, map):
#             continue
#
#         # Create New path
#         newPath = []
#         newPath.extend(path[:first[2] + 1])
#         newPath.append([first[0], first[1]])
#         newPath.append([second[0], second[1]])
#         newPath.extend(path[second[2] + 1:])
#         path = newPath
#         le = get_path_length(path)
#
#     return path




