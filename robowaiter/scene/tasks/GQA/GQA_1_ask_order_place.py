"""
具身多轮对话 GQA
点餐（order）的对话，咖啡厅服务员可以为客人（NPC）完成点餐基本对话
场景对话（GQA）结合场景：询问卫生间、附近娱乐场所（数据来源自主定义）
开始条件：顾客NPC发出点餐指令
结束条件：顾客NPC发出指令，表示不再需要服务
"""

# todo: 使用大模型进行对话，获得指令信息，适时结束对话
# order = {...}

from robowaiter.scene.scene import Scene

class SceneGQA(Scene):
    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件， (事件发生的时间，事件函数)
        self.new_event_list = [
            (3, self.customer_say, ("System","哪里有蛋糕"))
        ]

    def _reset(self):
        self.gen_obj()
        self.add_walkers([ [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
        self.control_walker(1, True, 100, 60, 720, 0)
        self.control_walker(4, True, 100, 60, -120, 0)
        self.add_walkers([[16,60, 520], [47,-40, 520]])
        pass



    def _run(self):
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneGQA(robot)
    task.reset()
    task.run()
