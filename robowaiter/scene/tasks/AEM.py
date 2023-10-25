"""
环境主动探索和记忆
要求输出探索结果（语义地图）对环境重点信息记忆。生成环境的语义拓扑地图，和不少于10个环境物品的识别和位置记忆，可以是图片或者文字或者格式化数据。
"""

from robowaiter.scene.scene import Scene

class SceneAEM(Scene):
    def __init__(self, robot):
        super().__init__(robot)

        # control.init_world(1, 3)

    def reset(self):
        self.reset_sim()

        self.add_object(0, 570, 1600, 85.5)  # type与物品编号对应，具体参考README.md
        self.add_object(1, 570, 1630, 85.5)
        self.add_object(2, 570, 1660, 85.5)
        self.add_object(3, 580, 1680, 85.5)

        # todo: 探索并获得语义地图
        print(self.status.objects)  # 全部的物品信息，包括名称、位置等，与获得的语义地图进行对比

    def run(self):
        pass