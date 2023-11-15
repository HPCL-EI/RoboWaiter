#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# enconding = utf8
import math
import os
import pickle
import sys
import time
import grpc

import camera
import semantic_map

sys.path.append('./')
sys.path.append('../')

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

import GrabSim_pb2_grpc
import GrabSim_pb2

channel = grpc.insecure_channel('localhost:30001', options=[
    ('grpc.max_send_message_length', 1024 * 1024 * 1024),
    ('grpc.max_receive_message_length', 1024 * 1024 * 1024)
])

sim_client = GrabSim_pb2_grpc.GrabSimStub(channel)

visited = set()
all_frontier_list = set()


'''
初始化，卸载已经加载的关卡，清除所有机器人
'''


def Init():
    sim_client.Init(GrabSim_pb2.NUL())


'''
获取当前可加载的地图信息(地图名字、地图尺寸)
'''


def AcquireAvailableMaps():
    AvailableMaps = sim_client.AcquireAvailableMaps(GrabSim_pb2.NUL())
    print(AvailableMaps)


'''
1、根据mapID加载指定地图
2、如果scene_num>1,则根据地图尺寸偏移后加载多个相同地图
3、这样就可以在一个关卡中训练多个地图
'''


def SetWorld(map_id=0, scene_num=1):
    print('------------------SetWorld----------------------')
    world = sim_client.SetWorld(GrabSim_pb2.BatchMap(count=scene_num, mapID=map_id))


'''
返回场景的状态信息
1、返回机器人的位置和旋转
2、返回各个关节的名字和旋转
3、返回场景中标记的物品信息(名字、类型、位置、旋转)
4、返回场景中行人的信息(名字、位置、旋转、速度)
5、返回机器人手指和双臂的碰撞信息
'''


def Observe(scene_id=0):
    print('------------------show_env_info----------------------')
    scene = sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id))
    # print(
    #     f"location:{[scene.location]}, rotation:{scene.rotation}\n",
    #     f"joints number:{len(scene.joints)}, fingers number:{len(scene.fingers)}\n",
    #     f"objects number: {len(scene.objects)}, walkers number: {len(scene.walkers)}\n"
    #     f"timestep:{scene.timestep}, timestamp:{scene.timestamp}\n"
    #     f"collision:{scene.collision}, info:{scene.info}")
    return scene


'''
重置场景
1、重置桌子的宽度和高度
2、清除生成的行人和物品
3、重置关节角度、位置旋转
4、清除碰撞信息
5、重置场景中标记的物品
'''


def Reset(scene_id=0):
    print('------------------Reset----------------------')
    scene = sim_client.Reset(GrabSim_pb2.ResetParams(scene=scene_id))
    print(scene)

    # 如果场景支持调整桌子
    # sim_client.Reset(GrabSim_pb2.ResetParams(scene = scene_id, adjust = True, height = 100.0, width = 100.0))"


"""
导航移动 
yaw:机器人朝向;
velocity:速度,>0代表移动,<0代表瞬移,=0代表只查询;
dis:最终达到的位置距离目标点最远距离,如果超过此距离则目标位置不可达

"""


# def navigation_test(scene_id=0, map_id=11):
#     print('------------------navigation_move----------------------')
#     scene = sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id))
#     walk_value = [scene.location.X, scene.location.Y, scene.rotation.Yaw]
#     print("position:", walk_value)
#
#     if map_id == 11:  # coffee
#         v_list = [[237, 495], [232, 495], [227, 490]]
#     else:
#         v_list = [[0.0, 0.0]]
#
#     for walk_v in v_list:
#         walk_v = walk_v + [scene.rotation.Yaw - 90, 60, 0]
#         print("walk_v", walk_v)
#         action = GrabSim_pb2.Action(scene=scene_id, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
#         scene = sim_client.Do(action)
#         print(scene.info)


def navigation_move(cur_objs, objs_name_set, v_list, scene_id=0, map_id=11):
    print('------------------navigation_move----------------------')
    scene = sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id))
    walk_value = [scene.location.X, scene.location.Y, scene.rotation.Yaw]
    print("position:", walk_value)


    # if map_id == 11:  # coffee
    #     v_list = [[0, 880], [250, 1200], [-55, 750], [70, -200]]
    # else:
    #     v_list = [[0.0, 0.0]]

    for walk_v in v_list:
        walk_v = walk_v + [scene.rotation.Yaw - 90, 250, 60]
        print("walk_v", walk_v)
        action = GrabSim_pb2.Action(scene=scene_id, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
        scene = sim_client.Do(action)
        cur_objs, objs_name_set = camera.get_semantic_map(GrabSim_pb2.CameraName.Head_Segment, cur_objs, objs_name_set)
        # if scene.info == "Unreachable":
        print(scene.info)
    return cur_objs, objs_name_set


def isOutMap(pos, min_x=-350, max_x=600, min_y=-400, max_y=1450):
    if pos[0] <= min_x or pos[0] >= max_x or pos[1] <= min_y or pos[1] >= \
            max_y:
        return True
    return False


def real2map(x, y):
    '''
        实际坐标->地图坐标 (向下取整)
    '''
    # x = round((x - self.min_x) / self.scale_ratio)
    # y = round((y - self.min_y) / self.scale_ratio)
    x = math.floor((x + 350) / 5)
    y = math.floor((y + 400) / 5)
    return x, y


def explore(map, cur_pos, explore_range):
    for i in range(cur_pos[0] - explore_range, cur_pos[0] + explore_range + 1):
        for j in range(cur_pos[1] - explore_range, cur_pos[1] + explore_range + 1):
            if isOutMap((i, j)):
                continue
            x, y = real2map(i, j)
            if map[x, y] == 0:
                visited.add((i, j))
    for i in range(cur_pos[0] - explore_range, cur_pos[0] + explore_range + 1):
        for j in range(cur_pos[1] - explore_range, cur_pos[1] + explore_range + 1):
            if isOutMap((i, j)):
                continue
            x, y = real2map(i, j)
            if map[x, y] == 0:
                if isNewFrontier((i, j), map):
                    all_frontier_list.add((i, j))
    if len(all_frontier_list) <= 400:
        free_list = list(visited)
        free_array = np.array(free_list)
        print(f"探索完成！以下是场景中可以到达的点：{free_array}；其余点均是障碍物不可达")
        return None
    return getNearestFrontier(cur_pos, all_frontier_list)


def isNewFrontier(pos, map):
    around_nodes = [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]

    for node in around_nodes:
        x, y = real2map(node[0], node[1])
        if node not in visited and map[x, y] == 0:
            return True
    if (pos[0], pos[1]) in all_frontier_list:
        all_frontier_list.remove((pos[0], pos[1]))
    return False


# def reachable(pos, map):
#     # scene = sim_client.Observe(GrabSim_pb2.SceneID(value=0))
#     # # x, y = real2map(self.area_range[0], self.area_range[2], self.scale_ratio, pos[0], pos[1])
#     # # if self.map[x, y] == 1:
#     # #     return True
#     # # else:
#     # #     return False
#     # loc = pos + [0, 0, 5]
#     # action = GrabSim_pb2.Action(scene=0, action=GrabSim_pb2.Action.ActionType.WalkTo, values=loc)
#     # scene = sim_client.Do(action)
#     # # print(scene.info)
#     # if (str(scene.info).find('Unreachable') > -1):
#     #     return False
#     # else:
#     #     return True
#     if map[pos[0], pos[1]] == 0:
#         return True
#     else:
#         return False
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


if __name__ == '__main__':
    map_id = 11  # 地图编号
    scene_num = 1  # 场景数量
    node_list = []  # 探索点
    explore_range = 240  # 机器人感知范围（以机器人为中心，边长为2 * _explore_range的正方形）
    cur_objs = []
    objs_name_set = set()

    file_name = 'map_5.pkl'
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            map = pickle.load(file)

    print('------------ 初始化加载场景 ------------')
    Init()
    AcquireAvailableMaps()
    SetWorld(map_id, scene_num)
    time.sleep(5.0)

    for i in range(scene_num):
        print('------------ 场景操作 ------------')
        scene = Observe(i)
        Reset(i)

        print('------------ 自主探索 ------------')
        cur_objs = semantic_map.navigation_move(cur_objs,i, map_id)
        print("物品列表如下：")
        print(cur_objs)



        # cur_pos = [int(scene.location.X), int(scene.location.Y)]
        # # print(reachable([237,490]))
        # # navigation_move([[237,490]], i, map_id)
        # # navigation_test(i,map_id)
        # while True:
        #     goal = explore(map, cur_pos, explore_range)  # cur_pos 指的是当前机器人的位置，场景中应该也有接口可以获取
        #     if goal is None:
        #         break
        #     node_list.append(goal)
        #     # print(goal)
        #     cur_objs, objs_name_set= navigation_move(cur_objs, objs_name_set, [[goal[0], goal[1]]], i, map_id)
        #     print(cur_objs)
        #     cur_pos = goal

        # TODO：node_list就是机器人拍照的点，目前没有设置拍照角度，需要机器人到达一个拍照点后，前后左右各拍一张照片然后获取语义信息
