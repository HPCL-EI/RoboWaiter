"""
人提出请求，机器人完成任务
1. 做咖啡（固定动画）：接收到做咖啡指令、走到咖啡机、拿杯子、操作咖啡机、取杯子、送到客人桌子上
2. 倒水
3. 夹点心

具体描述：设计一套点单规则（如菜单包含咖啡、水、点心等），按照规则拟造随机的订单。在收到订单后，通过大模型让机器人输出合理的备餐计划，并尝试在模拟环境中按照这个规划实现任务。

"""

# todo: 接收点单信息，大模型生成任务规划

from robowaiter.scene.scene import Scene

class SceneOT(Scene):

    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件
        self.new_event_list = [
            # (9,self.add_walkers,([[0, 880]],)),
            # (10,self.walker_walk_to,(2,50,500))
            # (5, self.set_goal("On(Yogurt,Table4)"))
            # (5, self.set_goal("At(Robot,BrightTable4)"))
        ]

    def _reset(self):
        # self.add_walkers([[0, 880], [250, 1200]])

        # 展示顾客，前8个id是小孩，后面都是大人
        for i in range(20):
            self.add_walker(i,50,300 + i * 50)

        for w in self.status.walkers:
            print(w.name)
        # name1 = self.walker_index2mem(1)
        # name2 = self.walker_index2mem(3)
        #
        # self.remove_walker(0,2)
        #
        # index1 = self.state["customer_mem"][name1]
        # index2 = self.state["customer_mem"][name2]
        #
        # self.walker_bubble(name1,f"我是第{index1}个")
        # self.walker_bubble(name2,f"我是第{index2}个")

    def _run(self):
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneOT(robot)
    task.reset()
    task.run()
