import os
import py_trees as ptree

from robowaiter.behavior_tree.utils import load_bt_from_ptml,find_node_by_name,print_tree_from_root
import io
import contextlib

class Robot(object):
    scene = None
    response_frequency = 1

    def __init__(self,ptml_path,behavior_lib_path):
        self.ptml_path = ptml_path
        self.behavior_lib_path = behavior_lib_path

        self.next_response_time = self.response_frequency
        self.step_num = 0
        self.last_tick_output = ""

    def set_scene(self,scene):
        self.scene = scene

    def load_BT(self):
        self.bt = load_bt_from_ptml(self.scene, self.ptml_path,self.behavior_lib_path)
        sub_task_place_holder = find_node_by_name(self.bt.root,"SubTaskPlaceHolder")
        if sub_task_place_holder:
            sub_task_seq = sub_task_place_holder.parent
            sub_task_seq.children.pop()
            self.scene.sub_task_seq = sub_task_seq


    def step(self):
        if self.scene.time > self.next_response_time:
            self.next_response_time += self.response_frequency
            self.step_num += 1

            # 创建一个StringIO对象
            output = io.StringIO()

            # 将print输出重定向到StringIO对象
            with contextlib.redirect_stdout(output):
                self.bt.tick()

            # 获取StringIO对象中的字符串值
            contents = output.getvalue()
            output.close()

            if contents != self.last_tick_output:
                print(f"==== time:{self.scene.time:f}s ======")

                print(contents)

                print("\n")
                self.last_tick_output = contents

if __name__ == '__main__':
    pass