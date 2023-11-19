"""
环境主动探索和记忆
要求输出探索结果（语义地图）对环境重点信息记忆。生成环境的语义拓扑地图，和不少于10个环境物品的识别和位置记忆，可以是图片或者文字或者格式化数据。
"""
import json
import math
import time

import matplotlib as mpl
import pickle

import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
from sklearn.cluster import DBSCAN

from robowaiter.scene.scene import Scene
class SceneAEM(Scene):
    def __init__(self, robot):
        super().__init__(robot)

    def _reset(self):
        pass
    def _run(self):
        # 创建一个从白色（1）到灰色（0）的 colormap
        cur_objs = []
        cur_obstacle_world_points = []
        objs_name_set = set()
        visited_obstacle = set()
        obj_json_data = []
        db = DBSCAN(eps=4, min_samples=2)

        map_ratio = 3
        # # 创建一个颜色映射，其中0表示黑色，1表示白色
        # cmap = plt.cm.get_cmap('gray')
        # cmap.set_under('black')
        # cmap.set_over('white')



        file_name = '../../proto/map_1.pkl'
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                map = pickle.load(file)
        print('------------ 自主探索 ------------')
        # cur_objs = self.semantic_map.navigation_move(cur_objs, 0, 11)
        # print("物品列表如下：")
        # print(cur_objs)
        # cur_pos = [int(scene.location.X), int(scene.location.Y)]
        # print(reachable([237,490]))
        # navigation_move([[237,490]], i, map_id)
        # navigation_test(i,map_id)
        map_map = np.zeros((math.ceil(950 / map_ratio), math.ceil(1850 / map_ratio)))


        while True:
            fig = plt.figure()
            goal = self.explore(map, 120)  # cur_pos 指的是当前机器人的位置，场景中应该也有接口可以获取
            if goal is None:
                break
            cur_objs, objs_name_set, cur_obstacle_world_points= self.navigation_move(plt, cur_objs, objs_name_set, cur_obstacle_world_points, [[goal[0], goal[1]]], map_ratio, db,0, 11)

            for point in cur_obstacle_world_points:
                if point[0] < -350 or point[0] > 600 or point[1] < -400 or point[1] > 1450:
                    continue
                map_map[math.floor((point[0] + 350) / map_ratio), math.floor((point[1] + 400) / map_ratio)] = 1
                visited_obstacle.add((math.floor((point[0] + 350) / map_ratio), math.floor((point[1] + 400) / map_ratio)))
            # plt.imshow(map_map, cmap='binary', alpha=0.5, origin='lower',
            #            extent=(-400 / map_ratio, 1450 / map_ratio,
            #                    -350 / map_ratio, 600 / map_ratio))

            # 使用imshow函数绘制图像，其中cmap参数设置颜色映射

            plt.subplot(2, 1, 2)  # 这里的2,1表示总共2行，1列，2表示这个位置是第2个子图
            plt.imshow(map_map, cmap='binary', alpha=0.5, origin='lower',
                       extent=(-400 / map_ratio, 1450 / map_ratio,
                               -350 / map_ratio, 600 / map_ratio))
            # plt.imshow(map_map, cmap='binary', alpha=0.5, origin='lower')
            # plt.axis('off')
            plt.title("地图构建过程")
            plt.show()
            print("------------当前检测到的物品信息--------------")
            print(cur_objs)
            time.sleep(1)


        for i in range(len(cur_objs)):
            if cur_objs[i].name == "Desk" or cur_objs[i].name == "Chair":
                obj_json_data.append({"id":f"{i}", "name":f"{cur_objs[i].name}", "location":f"{cur_objs[i].location}", "height":f"{cur_objs[i].location.Z * 2}"})

            else:
                obj_json_data.append(
                    {"id": f"{i}", "name": f"{cur_objs[i].name}", "location": f"{cur_objs[i].location}",
                     "height": f"{cur_objs[i].location.Z}"})

        with open('../../proto/objs.json', 'w') as file:
            json.dump(obj_json_data, file)

        # for i in range(-350, 600):
        #     for j in range(-400, 1450):
        #         i = (math.floor((i + 350) / map_ratio))
        #         j = (math.floor((j + 400) / map_ratio))
        #         if (i, j) not in visited_obstacle:
        #             map_map[i][j] = 1
        # plt.imshow(map_map, cmap='binary', alpha=0.5, origin='lower',
        #            extent=(-400 / map_ratio, 1450 / map_ratio,
        #                    -350 / map_ratio, 600 / map_ratio))
        # plt.axis('off')
        # plt.show()
        print("已绘制完成地图！！！")
        print("------------检测到的所有物品信息--------------")
        print(obj_json_data)


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneAEM(robot)
    task.reset()
    task.run()
