"""
人提出请求，机器人完成任务
1. 做咖啡（固定动画）：接收到做咖啡指令、走到咖啡机、拿杯子、操作咖啡机、取杯子、送到客人桌子上
2. 倒水
3. 夹点心

具体描述：设计一套点单规则（如菜单包含咖啡、水、点心等），按照规则拟造随机的订单。在收到订单后，通过大模型让机器人输出合理的备餐计划，并尝试在模拟环境中按照这个规划实现任务。

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
                self.set_goal(question)()
            else:
                self.state['chat_list'].append(question)



if __name__ == '__main__':
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SubScene(robot)
    task.reset()
    task.run()
