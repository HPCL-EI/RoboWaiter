#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# enconding = utf8
import sys
import time
import grpc

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

from proto import GrabSim_pb2
from proto import GrabSim_pb2_grpc

channel = grpc.insecure_channel('localhost:30001', options=[
    ('grpc.max_send_message_length', 1024 * 1024 * 1024),
    ('grpc.max_receive_message_length', 1024 * 1024 * 1024)
])

sim_client = GrabSim_pb2_grpc.GrabSimStub(channel)


def map_test(map_id=0, scene_num=1):
    initworld = sim_client.Init(GrabSim_pb2.NUL())
    print(sim_client.AcquireAvailableMaps(GrabSim_pb2.NUL()))
    initworld = sim_client.SetWorld(GrabSim_pb2.BatchMap(count=scene_num, mapID=map_id))


def control_robot_action(scene_id=0, type=0, action=0, message="你好"):
    scene = sim_client.ControlRobot(GrabSim_pb2.ControlInfo(scene=scene_id, type=type, action=action, content=message))
    if (scene.info == "action success"):
        return True
    else:
        return False


if __name__ == '__main__':
    map_id = 3  # 地图编号: 0：空房间 1：室内 2:咖啡厅1.0 3: 咖啡厅2.0 4:餐厅 5:养老院 6：会议室
    scene_num = 1  # 场景数量
    map_test(map_id, scene_num)  # 场景加载测试
    time.sleep(5)

    # 制作咖啡
    control_robot_action(0, 0, 1, "开始制作咖啡")
    result = control_robot_action(0, 1, 1)
    if (result):
        control_robot_action(0, 1, 2)
        control_robot_action(0, 1, 3)
        control_robot_action(0, 1, 4)
    else:
        control_robot_action(0, 0, 1, "制作咖啡失败")

    # 倒水
    control_robot_action(0, 0, 1, "开始倒水")
    result = control_robot_action(0, 2, 1)
    if (result):
        control_robot_action(0, 2, 2)
        control_robot_action(0, 2, 3)
        control_robot_action(0, 2, 4)
        control_robot_action(0, 2, 5)
    else:
        control_robot_action(0, 0, 1, "倒水失败")

    # 夹点心
    control_robot_action(0, 0, 1, "开始夹点心")
    result = control_robot_action(0, 3, 1)
    if (result):
        control_robot_action(0, 3, 2)
        control_robot_action(0, 3, 3)
        control_robot_action(0, 3, 4)
        control_robot_action(0, 3, 5)
        control_robot_action(0, 3, 6)
        control_robot_action(0, 3, 7)
    else:
        control_robot_action(0, 0, 1, "夹点心失败")

        # 拖地
    control_robot_action(0, 0, 1, "开始拖地")
    result = control_robot_action(0, 4, 1)
    if (result):
        control_robot_action(0, 4, 2)
        control_robot_action(0, 4, 3)
        control_robot_action(0, 4, 4)
    else:
        control_robot_action(0, 0, 1, "拖地失败")

        # 擦桌子
    control_robot_action(0, 0, 1, "开始擦桌子")
    result = control_robot_action(0, 5, 1)
    if (result):
        control_robot_action(0, 5, 2)
        control_robot_action(0, 5, 3)
    else:
        control_robot_action(0, 0, 1, "擦桌子失败")