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

    def _reset(self):
        self.add_walker(1085, 2630, 220)
        self.control_walker([self.walker_control_generator(0, False, 100, 755, 1900, 180)])


    def _run(self):
        pass

    def _step(self):

        if int(self.time)% 5 == 0:
            print("顾客说：请问你们这里有哪些咖啡")
            self.chat_bubble('顾客说：请问你们这里有哪些咖啡')
            self.state['chat_list'].append('请问你们这里有哪些咖啡')
