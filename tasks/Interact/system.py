"""
交互式场景，输入

"""

# todo: 接收点单信息，大模型生成任务规划

from robowaiter.scene.scene import Scene

class SubScene(Scene):

    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件

    def _reset(self):
        pass


    def _step(self):
        if len(self.sub_task_seq.children) == 0:
            question = input("请输入指令：")
            if question[-1] == ")":
                print(f"设置目标:{question}")
                self.new_set_goal(question)
            else:
                self.customer_say("System",question)



if __name__ == '__main__':
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SubScene(robot)
    task.reset()
    task.run()
