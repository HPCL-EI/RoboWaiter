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
        self.event_list = [
            (5, self.create_chat_event("给我一杯咖啡")),
            (20, self.create_chat_event("我要拿铁")),
            (40, self.create_chat_event("再来一杯")),
        ]

    def _reset(self):
        self.add_walker(1085, 2630, 220)
        self.control_walker([self.walker_control_generator(0, False, 100, 755, 1900, 180)])


    def _run(self):
        pass
