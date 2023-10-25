import os
import py_trees as ptree

from robowaiter.behavior_tree import load_bt_from_ptml

class Robot(object):
    scene = None
    def __init__(self,ptml_path,behavior_lib_path):
        self.ptml_path = ptml_path
        self.behavior_lib_path = behavior_lib_path

    def set_scene(self,scene):
        self.scene = scene

    def load_BT(self):
        self.bt = load_bt_from_ptml(self.scene, self.ptml_path,self.behavior_lib_path)


if __name__ == '__main__':
    pass