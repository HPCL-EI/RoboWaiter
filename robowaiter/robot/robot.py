import os
import py_trees as ptree

from robowaiter.behavior_tree.utils import load_bt_from_ptml,find_node_by_name,print_tree_from_root

class Robot(object):
    scene = None
    response_frequency = 1

    def __init__(self,ptml_path,behavior_lib_path):
        self.ptml_path = ptml_path
        self.behavior_lib_path = behavior_lib_path

        self.next_response_time = self.response_frequency
        self.step_num = 0

    def set_scene(self,scene):
        self.scene = scene

    def load_BT(self):
        self.bt = load_bt_from_ptml(self.scene, self.ptml_path,self.behavior_lib_path)
        sub_task_seq = find_node_by_name(self.bt.root,"SubTaskPlaceHolder").parent
        sub_task_seq.children.pop()
        print(sub_task_seq.children)

    def step(self):
        if self.scene.time > self.next_response_time:
            self.next_response_time += self.response_frequency
            self.step_num += 1

            print(f"==== step: {self.step_num}, time:{self.scene.time:f}s ======")

            self.bt.tick()

            print("\n")

if __name__ == '__main__':
    pass