"""
环境主动探索和记忆
要求输出探索结果（语义地图）对环境重点信息记忆。生成环境的语义拓扑地图，和不少于10个环境物品的识别和位置记忆，可以是图片或者文字或者格式化数据。
"""
import math
import matplotlib as mpl
import pickle

import numpy as np
from matplotlib import pyplot as plt

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

        map_ratio = 5
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
            goal = self.explore(map, 120)  # cur_pos 指的是当前机器人的位置，场景中应该也有接口可以获取
            if goal is None:
                break
            cur_objs, objs_name_set, cur_obstacle_world_points= self.navigation_move(cur_objs, objs_name_set, cur_obstacle_world_points, [[goal[0], goal[1]]], map_ratio, 0, 11)

            for point in cur_obstacle_world_points:
                if point[0] < -350 or point[0] > 600 or point[1] < -400 or point[1] > 1450:
                    continue
                map_map[math.floor((point[0] + 350) / map_ratio), math.floor((point[1] + 400) / map_ratio)] = 1
                visited_obstacle.add((math.floor((point[0] + 350) / map_ratio), math.floor((point[1] + 400) / map_ratio)))
            # plt.imshow(map_map, cmap='binary', alpha=0.5, origin='lower',
            #            extent=(-400 / map_ratio, 1450 / map_ratio,
            #                    -350 / map_ratio, 600 / map_ratio))

            # 使用imshow函数绘制图像，其中cmap参数设置颜色映射
            plt.imshow(map_map, cmap='binary', alpha=0.5, origin='lower',
                       extent=(-400 / map_ratio, 1450 / map_ratio,
                               -350 / map_ratio, 600 / map_ratio))
            # plt.imshow(map_map, cmap='binary', alpha=0.5, origin='lower')
            # plt.axis('off')
            plt.show()
        print("------------物品信息--------------")
        print(cur_objs)
        # for i in range(-350, 600):
        #     for j in range(-400, 1450):
        #         i = (math.floor((i + 350) / map_ratio))
        #         j = (math.floor((j + 400) / map_ratio))
        #         if (i, j) not in visited_obstacle:
        #             map_map[i][j] = 1
        plt.imshow(map_map, cmap='binary', alpha=0.5, origin='lower',
                   extent=(-400 / map_ratio, 1450 / map_ratio,
                           -350 / map_ratio, 600 / map_ratio))
        # plt.axis('off')
        plt.show()
        print("已绘制完成地图！！！")


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneAEM(robot)
    task.reset()
    task.run()
