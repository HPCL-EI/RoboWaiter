# from robowaiter.scene.scene import Scene
# from robowaiter.behavior_tree.ptml.ptmlCompiler import load

import os
from robowaiter.robot.robot import Robot
from robowaiter.utils.bt.draw import render_dot_tree
from robowaiter.utils.basic import get_root_path
from robowaiter.utils.bt.load import load_bt_from_ptml

if __name__ == '__main__':

    # create robot
    root_path = get_root_path()
    ptml_path = os.path.join(root_path, 'robowaiter/utils/draw_bt/Default.ptml')
    behavior_lib_path = os.path.join(root_path, 'robowaiter/behavior_lib')
    bt = load_bt_from_ptml(None, ptml_path, behavior_lib_path)



    render_dot_tree(bt.root,name="test")
    # build and tick
