#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# enconding = utf8
import json
import string
import sys
import time
import grpc

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
objects_dic = {}

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


'''
根据传入的部位名字，获取相机数据
'''


def get_camera(part, scene_id=0):
    print('------------------get_camera----------------------')
    action = GrabSim_pb2.CameraList(cameras=part, scene=scene_id)
    return sim_client.Capture(action)


'''
显示相机画面
'''


def show_image(img_data, scene):
    print('------------------show_image----------------------')
    im = img_data.images[0]

    # 相机内参矩阵
    in_matrix = np.array(
        [[im.parameters.fx, 0, im.parameters.cx], [0, im.parameters.fy, im.parameters.cy], [0, 0, 1]])

    # 相机外参矩阵
    out_matrix = np.array(im.parameters.matrix).reshape((4, 4))

    # # 旋转矩阵
    # rotation_matrix = out_matrix[0:3, 0:3]
    #
    # # 平移矩阵
    # translation_matrix = out_matrix[0:3, -1].reshape(3, 1)

    # 像素坐标
    # pixel_point = np.array([403, 212, 1]).reshape(3, 1)
    pixel_x = 404
    pixel_y = 212
    depth = 369

    # 将像素坐标转换为归一化设备坐标
    normalized_x = (pixel_x - im.parameters.cx) / im.parameters.fx
    normalized_y = (pixel_y - im.parameters.cy) / im.parameters.fy

    # 将归一化设备坐标和深度值转换为相机坐标
    camera_x = normalized_x * depth
    camera_y = normalized_y * depth
    camera_z = depth

    # 构建相机坐标向量
    camera_coordinates = np.array([camera_x, camera_y, camera_z, 1])
    # print("物体相对相机坐标的齐次坐标: ", camera_coordinates)

    # 将相机坐标转换为机器人底盘坐标
    robot_coordinates = np.dot(out_matrix, camera_coordinates)[:3]
    # print("物体的相对底盘坐标为:", robot_coordinates)

    # 将物体相对机器人底盘坐标转为齐次坐标
    robot_homogeneous_coordinates = np.array([robot_coordinates[0], -robot_coordinates[1], robot_coordinates[2], 1])
    # print("物体的相对底盘的齐次坐标为:", robot_homogeneous_coordinates)

    # 机器人坐标
    X = scene.location.X
    Y = scene.location.Y
    Z = 0.0

    # 机器人旋转信息
    Roll = 0.0
    Pitch = 0.0
    Yaw = scene.rotation.Yaw

    # 构建平移矩阵
    T = np.array([[1, 0, 0, X],
                  [0, 1, 0, Y],
                  [0, 0, 1, Z],
                  [0, 0, 0, 1]])

    # 构建旋转矩阵
    Rx = np.array([[1, 0, 0, 0],
                   [0, np.cos(Roll), -np.sin(Roll), 0],
                   [0, np.sin(Roll), np.cos(Roll), 0],
                   [0, 0, 0, 1]])

    Ry = np.array([[np.cos(Pitch), 0, np.sin(Pitch), 0],
                   [0, 1, 0, 0],
                   [-np.sin(Pitch), 0, np.cos(Pitch), 0],
                   [0, 0, 0, 1]])

    Rz = np.array([[np.cos(np.radians(Yaw)), -np.sin(np.radians(Yaw)), 0, 0],
                   [np.sin(np.radians(Yaw)), np.cos(np.radians(Yaw)), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    R = np.dot(Rz, np.dot(Ry, Rx))

    # 构建机器人的变换矩阵
    T_robot = np.dot(T, R)
    # print(T_robot)

    # 将物体的坐标从机器人底盘坐标系转换到世界坐标系
    world_coordinates = np.dot(T_robot, robot_homogeneous_coordinates)[:3]
    # print("物体的世界坐标：", world_coordinates)

    # 世界偏移后的坐标
    world_offest_coordinates = [world_coordinates[0] + 700, world_coordinates[1] + 1400, world_coordinates[2]]
    # print("物体世界偏移的坐标: ", world_offest_coordinates)
    # world_point = world_coordinates + np.array([])
    # print("物体的世界坐标为：", )

    # # 相对机器人的世界坐标
    # world_point = rotation_matrix.T @ (in_matrix.T * 369 @ pixel_point - translation_matrix)


    # print(world_point)

    # print(in_matrix @ out_matrix @ obj_world)
    #
    d = np.frombuffer(im.data, dtype=im.dtype).reshape((im.height, im.width, im.channels))
    plt.imshow(d, cmap="gray" if "depth" in im.name.lower() else None)
    plt.show()


def save_obj_info(img_data, objs_name):
    items = img_data.info.split(";")
    dictionary = {}
    for item in items:
        key, value = item.split(":")
        dictionary[int(key)] = value

    im = img_data.images[0]
    d = np.frombuffer(im.data, dtype=im.dtype).reshape((im.height, im.width, im.channels))
    arr_flat = d.ravel()
    for id in arr_flat:
        if id not in dictionary:
            print(id)
        else:
            objs_name.add(dictionary[id])
    return objs_name


def get_semantic_map(camera, cur_objs, objs_name):
    scene = Observe(0)
    objs = scene.objects
    img_data = get_camera([camera])
    show_image(img_data, scene)
    objs_name = save_obj_info(img_data, objs_name)
    for obj_name in list(objs_name):
        for obj in objs:
            if obj.name == obj_name and obj not in cur_objs:
                cur_objs.append(obj)
                break
    return cur_objs, objs_name


if __name__ == '__main__':
    map_id = 11  # 地图编号
    scene_num = 1  # 场景数量
    cur_objs = []

    print('------------ 初始化加载场景 ------------')
    Init()
    AcquireAvailableMaps()
    SetWorld(map_id, scene_num)
    time.sleep(5.0)

    for i in range(scene_num):
        print('------------ 场景操作 ------------')
        scene = Observe(i)

        Reset(i)

        print('------------ 相机捕获 ------------')
        Reset(i)
        time.sleep(1.0)

        # print(get_semantic_map(GrabSim_pb2.CameraName.Head_Segment,cur_objs))

        for camera_name in [GrabSim_pb2.CameraName.Head_Depth]:
            img_data = get_camera([camera_name], i)
            show_image(img_data, scene)
        # for camera_name in [GrabSim_pb2.CameraName.Waist_Color, GrabSim_pb2.CameraName.Waist_Depth]:
        #     img_data = get_camera([camera_name], i)
        #     show_image(img_data, 2)
