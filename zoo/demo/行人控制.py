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

def add_walker(scene_id=0):
    """pose:表示行人的初始位置姿态"""
    print('------------------add walker----------------------')
    s = sim_client.Observe(GrabSim_pb2.SceneID(value=0))

    walker_loc = [[0, 880], [250, 1200], [-55, 750], [70, -200]]
    walker_list = []
    for i in range(len(walker_loc)):
        loc = walker_loc[i] + [0, 600, 100]
        action = GrabSim_pb2.Action(scene=scene_id, action=GrabSim_pb2.Action.ActionType.WalkTo, values=loc)
        scene = sim_client.Do(action)
        print(scene.info)
        # 只有可达的位置才能成功初始化行人，显示unreachable的地方不能初始化行人
        walker_list.append(GrabSim_pb2.WalkerList.Walker(id=i, pose=GrabSim_pb2.Pose(X=loc[0], Y=loc[1], Yaw=90)))

    scene = sim_client.AddWalker(GrabSim_pb2.WalkerList(walkers=walker_list, scene=scene_id))
    return scene

def control_walkers(scene_id=0):
    """pose:表示行人的终止位置姿态"""
    s = sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id))

    walker_loc = [[-55, 750], [70, -200], [250, 1200], [0, 880]]
    controls = []
    for i in range(len(s.walkers)):
        loc = walker_loc[i]
        is_autowalk = False
        pose = GrabSim_pb2.Pose(X=loc[0], Y=loc[1], Yaw=180)
        controls.append(GrabSim_pb2.WalkerControls.WControl(id=i, autowalk=is_autowalk, speed=200, pose=pose))
    scene = sim_client.ControlWalkers(GrabSim_pb2.WalkerControls(controls=controls, scene=scene_id))
    time.sleep(10)
    return scene

def remove_walkers(scene_id=0):
    s = sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id))
    scene = sim_client.RemoveWalkers(GrabSim_pb2.RemoveList(IDs=[1, 3], scene=scene_id))
    time.sleep(2)
    return

def clean_walkers(scene_id=0):
    scene = sim_client.CleanWalkers(GrabSim_pb2.SceneID(value=scene_id))
    return scene

def walker_test(scene_id=0):
    add_walker(scene_id)
    control_walkers(scene_id)
    print(sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id)).walkers)
    remove_walkers(scene_id)
    print(sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id)).walkers)
    clean_walkers(scene_id)
    return

if __name__ == '__main__':
    map_id = 3                      # 地图编号: 3: 咖啡厅
    scene_num = 1                   # 场景数量
    map_test(map_id, scene_num)     # 场景加载测试
    time.sleep(5)

    for i in range(scene_num):
        print("------------------", i, "----------------------")
        walker_test(i)              # 行人控制测试