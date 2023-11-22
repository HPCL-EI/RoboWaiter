"""
交互式场景，输入
"""
import tkinter as tk
from robowaiter.utils.ui.pyqt5 import UI
import os
from matplotlib import pyplot as plt

# todo: 接收点单信息，大模型生成任务规划

from robowaiter.scene.scene import Scene
from robowaiter.utils.ui.ui import RobotInterface
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

    def init_robot(self, robot):
        # init robot
        self.robot = robot

        if robot:
            robot.set_scene(self)
            robot.load_BT()
            self.draw_current_bt()

    def draw_current_bt(self):
        render_dot_tree(self.robot.bt.root,target_directory=self.output_path,name="current_bt")
        self.ui_queue.put(('draw_from_file',"img_label_bt", f"{self.output_path}/current_bt.png"))

    def ui_func(self,args):
        _,_,output_path = args
        plt.savefig(output_path)

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


if __name__ == '__main__':
    from robowaiter.robot.robot import Robot

    robot = Robot()
    ui = UI(SceneUI, Robot)

    # create task
    # task = SceneUI(robot,ui)

