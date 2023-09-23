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

def get_camera(part, scene_id=0):
    action = GrabSim_pb2.CameraList(cameras=part, scene=scene_id)
    return sim_client.Capture(action)

def show_image(img_data):
    im = img_data.images[0]
    d = np.frombuffer(im.data, dtype=im.dtype).reshape((im.height, im.width, im.channels))
    plt.imshow(d, cmap="gray" if "depth" in im.name.lower() else None)
    plt.show()

def camera_test(scene_id=0):
    for camera_name in [GrabSim_pb2.CameraName.Head_Color, GrabSim_pb2.CameraName.Head_Depth, GrabSim_pb2.CameraName.Head_Segment]:
        img_data = get_camera([camera_name], scene_id)
        show_image(img_data)

if __name__ == '__main__':
    map_id = 3                      # 地图编号: 0：空房间 1：室内 2:咖啡厅1.0 3: 咖啡厅2.0 4:餐厅 5:养老院 6：会议室
    scene_num = 1                   # 场景数量
    map_test(map_id, scene_num)     # 场景加载测试
    time.sleep(5)

    for i in range(scene_num):
        print("------------------", i, "----------------------")
        camera_test(i)              # 相机操作测试