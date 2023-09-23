#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import sys
import time
import grpc

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

from proto import GrabSim_pb2
from proto import GrabSim_pb2_grpc

channel = grpc.insecure_channel('localhost:30001',options=[
            ('grpc.max_send_message_length', 1024*1024*1024),
            ('grpc.max_receive_message_length', 1024*1024*1024)
        ])

sim_client = GrabSim_pb2_grpc.GrabSimStub(channel)

def map_test(map_id=0, scene_num=1):
    initworld = sim_client.Init(GrabSim_pb2.NUL())
    print(sim_client.AcquireAvailableMaps(GrabSim_pb2.NUL()))
    initworld = sim_client.SetWorld(GrabSim_pb2.BatchMap(count=scene_num, mapID=map_id))

def walk_test(scene_id=0, map_id=0):
    """
    移动底盘
    GrabSim_pb2.Action(sceneID=0, action=GrabSim_pb2.Action.ActionType.WalkTo, values=[x, y, yaw, velocity, dis])
    yaw: 机器人朝向; velocity:速度, -1代表瞬移; dis:最终达到的位置距离目标点最远距离, 如果超过此距离则目标位置不可达
    """
    scene = sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id))

    walk_value = [scene.location.X, scene.location.Y, scene.rotation.Yaw]
    print('------------------walk_test----------------------')
    print("position:", walk_value)

    if map_id == 3:  # coffee
        v_list = [[scene.location.X + 20, scene.location.Y - 500], [scene.location.X - 200, scene.location.Y - 300],
                  [scene.location.X - 200, scene.location.Y + 20], [0, 880], [250, 1200], [-55, 750], [70, -200]]
    else:
        v_list = [[scene.location.X - 10, scene.location.Y - 20]]

    for walk_v in v_list:
        walk_v = walk_v + [scene.rotation.Yaw - 90, 600, 100]
        print("walk_v", walk_v)
        action = GrabSim_pb2.Action(scene=scene_id, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
        scene = sim_client.Do(action)
        print(scene.info)  # print navigation info
        time.sleep(2)

if __name__ == '__main__':
    map_id = 3                      # 地图编号: 3: 咖啡厅
    scene_num = 1                   # 场景数量
    map_test(map_id, scene_num)     # 场景加载测试
    time.sleep(5)

    for i in range(scene_num):
        print("------------------", i, "----------------------")
        walk_test(i, map_id)        # 导航寻路测试