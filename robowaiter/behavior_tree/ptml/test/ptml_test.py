import os
import py_trees as ptree

from robowaiter.scene.scene import Scene
from robowaiter.behavior_tree.ptml.ptmlCompiler import load

import os
from robowaiter import Robot, task_map


if __name__ == '__main__':
    TASK_NAME = 'OT'

    # create robot
    project_path = "../../../"
    ptml_path = os.path.join(project_path, 'behavior_tree/ptml/test/Test.ptml')
    behavior_lib_path = os.path.join(project_path, 'behavior_lib')

    robot = Robot(ptml_path, behavior_lib_path)

    # create task
    task = task_map[TASK_NAME](robot)

    ptree.display.render_dot_tree(robot.bt.root,name="test")
    # build and tick
    # scene.BT = ptree.trees.BehaviourTree(scene.BT)
    # todo: tick this bt
    print(robot.bt)