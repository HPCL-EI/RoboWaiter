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

def reset(scene_id=0):
    scene = sim_client.Reset(GrabSim_pb2.ResetParams(scene=scene_id))

def show_env_info(scene_id=0):
    scene = sim_client.Observe(GrabSim_pb2.SceneID(value=scene_id))
    print('------------------show_env_info----------------------')
    print(
        f"location:{[scene.location.X, scene.location.Y]}, rotation:{scene.rotation.Yaw}\n",
        f"joints number:{len(scene.joints)}, fingers number:{len(scene.fingers)}\n", f"objects number: {len(scene.objects)}\n"
        f"rotation:{scene.rotation}, timestep:{scene.timestep}\n"
        f"timestamp:{scene.timestamp}, collision:{scene.collision}, info:{scene.info}")

if __name__ == '__main__':
    map_id = 3                      # 地图编号: 3: 咖啡厅
    scene_num = 1                   # 场景数量
    map_test(map_id, scene_num)     # 场景加载测试
    time.sleep(5)

    for i in range(scene_num):
        print("------------------", i, "----------------------")
        reset(i)                    # 场景重置测试
        show_env_info(i)            # 场景信息测试