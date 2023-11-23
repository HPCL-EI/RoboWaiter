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
        self.signal_event_list = [
            (5, self.customer_say, (6, "你好呀，你们这有啥好吃的？")), # 男
            (8, self.customer_say, (6, "听起来都好甜呀，我女朋友爱吃水果。")),
            (8, self.customer_say, (6, "你们这人可真多。")),
            (8, self.customer_say, (6, "我女朋友怕晒，有空余的阴凉位置嘛？")),
            (8, self.customer_say, (6, "那还不错。")),
            (8, self.customer_say, (5, "请问洗手间在哪呢？")),
            (8, self.customer_say, (5, "我们还想一起下下棋,切磋切磋。")),
            (8, self.customer_say, (6, "太棒啦，亲爱的。")),
            (8, self.customer_say, (5, "那你知道附近最近的电影院在哪吗?")),
            (8, self.customer_say, (6, "谢啦，那我们先去阴凉位置下个棋，等电影开始了就去看呢!")),

            # (6, self.customer_say, (5, "你好呀，这位可是我女朋友呢！")),
            # (5, self.customer_say, (6, "你们这有什么饮料嘛？")),
            # (6, self.customer_say, (5, "你好呀，这位可是我女朋友呢！")),
            # (5, self.customer_say, (6, "你们这有什么饮料嘛？")),
            # (6, self.customer_say, (5, "你好呀，这位可是我女朋友呢！")),
            # (5, self.customer_say, (6, "你们这有什么饮料嘛？")),
            # (1, self.control_walker_ls,([[[5, False, 100, -250, 480, 0],[6, False, 100, 60, 520, 0]]])),
            # (-1, self.customer_say, (5, "感谢，这些够啦，你去忙吧。")),
            # (10, self.customer_say, (6, "我想来份点心和酸奶。")),
            # (-1, self.customer_say, (6, "真美味啊！")),
        ]

    def _reset(self):
        self.gen_obj()
        self.add_walkers([ [16,250, 1200],[6,-55, 750],[10,70, -200],[47,-290, 400, 180],[26, 60,-320,90]])
        self.control_walker(1, True, 100, 60, 720, 0)
        self.control_walker(4, True, 100, 60, -120, 0)
        self.add_walkers([[31, 60,480,0], [15,60,550,0]])
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
