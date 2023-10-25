"""
在特定环境下，机器人发现目标，可自主完成任务
1. 打扫地面：地面有垃圾，机器人主动扫地、清理地面垃圾
2. 收拾桌子：桌子上的污渍，机器人主动擦桌子
3. 摆椅子：椅子不正，机器人主动摆正椅子
4. 开灯：室内光线暗，机器人主动打开房屋的灯
"""

# todo: 通过行为树控制自动任务

from robowaiter.scene.scene import Scene


class SceneAT(Scene):
    def __init__(self, robot):
        super().__init__(robot)

    def reset(self):
        self.reset_sim()

        self.add_walker(1085, 2630, 220)
        self.control_walker([self.walker_control_generator(0, False, 100, 755, 1900, 180)])

    def run(self):
        self.chat_bubble("顾客说：请给我一杯咖啡")

