"""
UI场景
"""
import sys


from robowaiter.scene.scene import Scene
from robowaiter.utils.bt.draw import render_dot_tree
class SceneUI(Scene):
    scene_queue = None
    ui_queue = None
    # camera_interval = 4
    def __init__(self, robot,scene_queue,ui_queue):
        self.scene_queue = scene_queue
        self.ui_queue = ui_queue

        super().__init__(robot)
        # 在这里加入场景中发生的事件
        self.take_picture = True

        # while True:
        #     if not self.scene_queue.empty():
        #         param = self.scene_queue.get()
        #         # 处理参数...

        # self.ui_queue.put(('say',"test"))
        self.stoped = False

    def run(self):
        # 基类run
        self._run()
        # 运行并由robot打印每步信息
        while not self.stoped:
            self.step()

    def run_AEM(self):
        pass

    def run_VLN(self):
        self.gen_obj()
        self.add_walkers([
            [29, 60, 520],  # 顾客 0
            [23, 0, 220],  # 秃头老头子  1
            [0, -55, 150],  # 小男孩d走来走去 2
            [10, -55, 750],  # 3
            [19, 70, -200],  # 后门站着不动的 4
            [21, 65, 1000, -90],  # 大胖男占了一号桌 5
            [5, 230, 1200],  # 小女孩 6
            [26, -28, -10, 90],
            # [26, 60, 0, 90],
            # [26, -28, 0, 90] , #在设置一个在后门随机游走的 7
            # 设置为 26, 60, 0, 90]
            [31, 280, 1200, -45]  # 8
        ])
        self.control_walker(2, True, 200, -55, 155, 90)  # 飞速奔跑的小男孩
        # self.control_walker(7, True, 80, -25, -150, 90)
        self.control_walker(5, True, 65, 995, 520, 90)
        self.control_walker(4, True, 65, 70, -200, 90)

        self.new_event_list = [
            (5, self.customer_say, (0, "请问哪里有空位啊？")),
            (13, self.customer_say, (0, "我想坐高凳子。")),
            (3, self.customer_say, (0, "你带我去吧。")),
            (45, self.control_walker, (0, False, 100, -250, 480, -90)),
            (-1, self.customer_say, (0, "谢谢你！这儿还不错！")),
        ]

    def run_VLM(self):
        pass

    def run_GQA(self):
        pass

    def run_OT(self):
        pass

    def run_AT(self):
        pass

    def run_reset(self):
        pass

    def init_robot(self):
        # init robot

        if self.robot:
            self.robot.set_scene(self)
            self.robot.load_BT()
            self.draw_current_bt()

    def draw_current_bt(self):
        render_dot_tree(self.robot.bt.root,target_directory=self.output_path,name="current_bt")
        self.ui_queue.put(('draw_from_file',"img_label_bt", f"{self.output_path}/current_bt.png"))

    def ui_func(self,args):
        # _,_,output_path = args
        # plt.savefig(output_path)

        self.ui_queue.put(args)

    def _reset(self):
        pass

    def _step(self):
        # print("已运行")
        self.handle_queue_messages()
        # if len(self.sub_task_seq.children) == 0:
        #     question = input("请输入指令：")
        #     if question[-1] == ")":
        #         print(f"设置目标:{question}")
        #         self.new_set_goal(question)
        #     else:
        #         self.customer_say("System",question)


    def handle_queue_messages(self):
        while not self.scene_queue.empty():
            message = self.scene_queue.get()
            function_name = message[0]
            function = getattr(self, function_name, None)

            args = []
            if len(message)>1:
                args = message[1:]

            result = function(*args)

    def stop(self):
        self.stoped = True

if __name__ == '__main__':
    from robowaiter.robot.robot import Robot

    robot = Robot()
    ui = UI( Robot)

    # create task
    # task = SceneUI(robot,ui)

