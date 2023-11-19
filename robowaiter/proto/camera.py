#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# enconding = utf8
import json
import string
import sys
import time
import grpc
from sklearn.cluster import DBSCAN

sys.path.append('./')
sys.path.append('../')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
obstacle_objs_id = [114, 115, 122, 96, 102, 83, 121, 105, 108, 89, 100, 90,
                    111, 103, 95, 92, 76, 113, 101, 29, 112, 87, 109, 98,
                    106, 120, 97, 86, 104, 78, 85, 81, 82, 84, 91, 93, 94,
                    99, 107, 116, 117, 118, 119, 255]
not_key_objs_id = {255,254,253,107,81}

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
    print(
        f"location:{[scene.location]}, rotation:{scene.rotation}\n",
        f"joints number:{len(scene.joints)}, fingers number:{len(scene.fingers)}\n",
        f"objects number: {len(scene.objects)}, walkers number: {len(scene.walkers)}\n"
        f"timestep:{scene.timestep}, timestamp:{scene.timestamp}\n"
        f"collision:{scene.collision}, info:{scene.info}")
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

def transform_co(img_data, pixel_x_, pixel_y_,depth_, scene ,id = 0,label = 0):
    im = img_data.images[0]

    # 相机外参矩阵
    out_matrix = np.array(im.parameters.matrix).reshape((4, 4))

    d = np.frombuffer(im.data, dtype=im.dtype).reshape((im.height, im.width, im.channels))
    depth = depth_

    # 将像素坐标转换为归一化设备坐标
    normalized_x = (pixel_x_ - im.parameters.cx) / im.parameters.fx
    normalized_y = (pixel_y_ - im.parameters.cy) / im.parameters.fy

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

    # if world_coordinates[0] < 200 and world_coordinates[1] <= 1050:
    #     world_coordinates[0] += 400
    #     world_coordinates[1] += 400
    # elif world_coordinates[0] >= 200 and world_coordinates[1] <= 1050:
    #     world_coordinates[0] -= 550
    #     world_coordinates[1] += 400
    # elif world_coordinates[0] >= 200 and world_coordinates[1] > 1050:
    #     world_coordinates[0] -= 550
    #     world_coordinates[1] -= 1450
    # elif world_coordinates[0] < 200 and world_coordinates[1] > 1050:
    #     world_coordinates[0] += 400
    #     world_coordinates[1] -= 1450
    # print("物体的世界坐标：", world_coordinates)

    # 世界偏移后的坐标
    world_offest_coordinates = [world_coordinates[0] + 700, world_coordinates[1] + 1400, world_coordinates[2]]
    # print("物体世界偏移的坐标: ", world_offest_coordinates)
    return world_coordinates

    # 世界偏移后的坐标
    # world_offest_coordinates = [world_coordinates[0] + 700, world_coordinates[1] + 1400, world_coordinates[2]]
    # print("物体世界偏移的坐标: ", world_offest_coordinates)


    # dict_f = {'id':id,'label':label,'world_coordinates':world_coordinates,'world_offest_coordinates':world_offest_coordinates}
    # with open('./semantic.txt', 'a') as file:
    #     file.write(str(dict_f) + '\n')


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

def get_id_object_pixels(id, scene):
    pixels = []
    world_points = []
    img_data_segment = get_camera([GrabSim_pb2.CameraName.Head_Segment])
    im_segment = img_data_segment.images[0]

    img_data_depth = get_camera([GrabSim_pb2.CameraName.Head_Depth])
    im_depth = img_data_depth.images[0]


    d_segment = np.frombuffer(im_segment.data, dtype=im_segment.dtype).reshape(
        (im_segment.height, im_segment.width, im_segment.channels))
    d_depth = np.frombuffer(im_depth.data, dtype=im_depth.dtype).reshape(
        (im_depth.height, im_depth.width, im_depth.channels))

    d_segment = np.transpose(d_segment, (1, 0, 2))
    d_depth = np.transpose(d_depth, (1, 0, 2))

    for i in range(0, d_segment.shape[0],5):
        for j in range(0, d_segment.shape[1], 5):
            if d_segment[i][j][0] == id:
                pixels.append([i, j])
    for pixel in pixels:
        world_points.append(transform_co(img_data_depth, pixel[0], pixel[1], d_depth[pixel[0]][pixel[1]][0], scene))
    return world_points




def get_obstacle_point(plt, db, scene, cur_obstacle_world_points, map_ratio):
    cur_obstacle_pixel_points = []
    object_pixels = {}
    colors = [
        'red',
        'pink',
        'purple',
        'blue',
        'cyan',
        'green',
        'yellow',
        'orange',
        'brown',
        'gold',
    ]

    img_data_segment = get_camera([GrabSim_pb2.CameraName.Head_Segment])
    img_data_depth = get_camera([GrabSim_pb2.CameraName.Head_Depth])
    img_data_color = get_camera([GrabSim_pb2.CameraName.Head_Color])

    im_segment = img_data_segment.images[0]
    im_depth = img_data_depth.images[0]
    im_color = img_data_color.images[0]

    d_segment = np.frombuffer(im_segment.data, dtype=im_segment.dtype).reshape((im_segment.height, im_segment.width, im_segment.channels))
    d_depth = np.frombuffer(im_depth.data, dtype=im_depth.dtype).reshape((im_depth.height, im_depth.width, im_depth.channels))
    d_color = np.frombuffer(im_color.data, dtype=im_color.dtype).reshape((im_color.height, im_color.width, im_color.channels))

    items = img_data_segment.info.split(";")
    objs_id = {}
    for item in items:
        key, value = item.split(":")
        objs_id[int(key)] = value
    # plt.imshow(d_depth, cmap="gray" if "depth" in im_depth.name.lower() else None)
    # plt.show()
    #
    # plt.imshow(d_segment, cmap="gray" if "depth" in im_segment.name.lower() else None)
    # plt.show()

    d_depth = np.transpose(d_depth, (1, 0, 2))
    d_segment = np.transpose(d_segment, (1, 0, 2))
    for i in range(0, d_segment.shape[0], map_ratio):
        for j in range(0, d_segment.shape[1], map_ratio):
            if d_depth[i][j][0] == 600:
                continue

            # if d_segment[i][j] == 96:
            #     print(f"apple的像素坐标：({i},{j})")
            #     print(f"apple的深度：{d_depth[i][j][0]}")
            #     print(f"apple的世界坐标: {transform_co(img_data_depth, i, j, d_depth[i][j][0], scene)}")
            # if d_segment[i][j] == 113:
            #     print(f"kettle的像素坐标：({i},{j})")
            #     print(f"kettle的深度：{d_depth[i][j][0]}")
            #     print(f"kettle的世界坐标: {transform_co(img_data_depth, i, j, d_depth[i][j][0], scene)}")
            if d_segment[i][j][0] in obstacle_objs_id:
                cur_obstacle_pixel_points.append([i, j])
            if d_segment[i][j][0] not in not_key_objs_id:
                # 首先检查键是否存在
                if d_segment[i][j][0] in object_pixels:
                    # 如果键存在，那么添加元组(i, j)到对应的值中
                    object_pixels[d_segment[i][j][0]].append([i, j])
                else:
                    # 如果键不存在，那么创建一个新的键值对，其中键是d_segment[i][j][0]，值是一个包含元组(i, j)的列表
                    object_pixels[d_segment[i][j][0]] = [[i, j]]
    # print(cur_obstacle_pixel_points)
    for pixel in cur_obstacle_pixel_points:
        world_point = transform_co(img_data_depth, pixel[0], pixel[1], d_depth[pixel[0]][pixel[1]][0], scene)
        cur_obstacle_world_points.append([world_point[0], world_point[1]])
        # print(f"{pixel}：{[world_point[0], world_point[1]]}")
    plt.subplot(2, 1, 1)
    plt.imshow(d_color, cmap="gray" if "depth" in im_depth.name.lower() else None)
    plt.axis('off')
    plt.title("目标检测")
    # plt.tight_layout()

    for key, value in object_pixels.items():
        if key == 0:
            continue
        if key in [91, 84, 96, 87, 102, 106, 120, 85,113, 101, 83]:
            X = np.array(value)
            db.fit(X)
            labels = db.labels_
            # 将数据按照聚类标签分组，并打印每个分组的数据
            for i in range(max(labels) + 1):  # 从0到最大聚类标签的值
                group_data = X[labels == i]  # 获取当前标签的数据
                x_max = max(p[0] for p in group_data)
                y_max = max(p[1] for p in group_data)
                x_min = min(p[0] for p in group_data)
                y_min = min(p[1] for p in group_data)
                if x_max - x_min < 10 or y_max - y_min < 10:
                    continue
                # 在指定的位置绘制方框
                # 创建矩形框
                rect = patches.Rectangle((x_min, y_min), (x_max - x_min), (y_max - y_min), linewidth=1, edgecolor=colors[key % 10],
                                         facecolor='none')
                plt.text(x_min, y_min, f'{objs_id[key]}', fontdict={'family': 'serif', 'size': 10, 'color': 'green'}, ha='center',
                         va='center')
                plt.gca().add_patch(rect)
        else:
            x_max = max(p[0] for p in value)
            y_max = max(p[1] for p in value)
            x_min = min(p[0] for p in value)
            y_min = min(p[1] for p in value)
            # 在指定的位置绘制方框
            # 创建矩形框
            rect = patches.Rectangle((x_min, y_min), (x_max - x_min), (y_max - y_min), linewidth=1, edgecolor=colors[key % 10],
                                     facecolor='none')
            plt.text(x_min, y_min, f'{objs_id[key]}', fontdict={'family': 'serif', 'size': 10, 'color': 'green'}, ha='center',
                     va='center')
            plt.gca().add_patch(rect)
        # point1 = min(value, key=lambda x: (x[0], x[1]))
        # point2 = max(value, key=lambda x: (x[0], x[1]))
        # width = point2[1] - point1[1]
        # height = point2[0] - point1[0]
        # rect = patches.Rectangle((0, 255), 15, 30, linewidth=1, edgecolor='g',
        #                          facecolor='none')


        # 将矩形框添加到图像中
        # plt.gca().add_patch(rect)

    # plt.show()
    return cur_obstacle_world_points





def get_semantic_map(camera, cur_objs, objs_name):
    scene = Observe(0)
    objs = scene.objects
    img_data = get_camera([camera])
    # show_image(img_data, scene)
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

        # for camera_name in [GrabSim_pb2.CameraName.Head_Depth]:
        #     img_data = get_camera([camera_name], i)
        #     show_image(img_data, scene)
        # for camera_name in [GrabSim_pb2.CameraName.Waist_Color, GrabSim_pb2.CameraName.Waist_Depth]:
        #     img_data = get_camera([camera_name], i)
        #     show_image(img_data, 2)
