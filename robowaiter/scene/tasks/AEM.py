"""
环境主动探索和记忆
要求输出探索结果（语义地图）对环境重点信息记忆。生成环境的语义拓扑地图，和不少于10个环境物品的识别和位置记忆，可以是图片或者文字或者格式化数据。
"""
import pickle

from robowaiter.scene.scene import Scene
class SceneAEM(Scene):
    def __init__(self, robot):
        super().__init__(robot)

    def _reset(self):
        pass
    def _run(self):
        cur_objs = []
        objs_name_set = set()
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
        while True:
            goal = self.explore(map, 120)  # cur_pos 指的是当前机器人的位置，场景中应该也有接口可以获取
            if goal is None:
                break
            cur_objs, objs_name_set = self.navigation_move(cur_objs, objs_name_set, [[goal[0], goal[1]]], 0, 11)
        print("------------物品信息--------------")
        print(cur_objs)

        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneAEM(robot)
    task.reset()
    task.run()
