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
        self.signal_event_list = [
            # (3, self.customer_say, ("System","来一号桌")),
            (2, self.customer_say, (0,"可以关筒灯和关窗帘吗？")),
            # (5, self.new_set_goal, ("Is(TubeLight,Off),Is(Curtain,Off)",))
        ]


    def _reset(self):
        self.add_walker(23, 60, 520,0)
        # self.control_walker([self.walker_control_generator(0, False, 100, 755, 1900, 180)])
        pass

    def _run(self):

        pass

    def _step(self):
        pass

if __name__ == '__main__':
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneAT(robot)
    task.reset()
    task.run()
