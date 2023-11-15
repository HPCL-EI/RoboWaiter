"""
环境主动探索和记忆
要求输出探索结果（语义地图）对环境重点信息记忆。生成环境的语义拓扑地图，和不少于10个环境物品的识别和位置记忆，可以是图片或者文字或者格式化数据。
"""

from robowaiter.scene.scene import Scene
from robowaiter.algos.explore.semantic_map import impo
class SceneAEM(Scene):
    def __init__(self, robot):
        super().__init__(robot)

    def _reset(self):
        pass
    def _run(self):
        cur_objs = []
        print('------------ 自主探索 ------------')
        cur_objs = self.semantic_map.navigation_move(cur_objs, 0, 11)
        print("物品列表如下：")
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
