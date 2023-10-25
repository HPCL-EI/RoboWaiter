import os
import py_trees as ptree

from scene import scene
from ptmlCompiler import load


if __name__ == '__main__':

    project_path = ""

    ptml_path = os.path.join(project_path, 'CoffeeDelivery.ptml')
    behavior_lib_path = os.path.join(project_path, '../../behavior_lib')

    scene = control.Scene(sceneID=0)
    # load
    scene.load_BT(ptml_path, behavior_lib_path)
    # ptree.display.render_dot_tree(bt)
    # build and tick
    scene.BT = ptree.trees.BehaviourTree(scene.BT)
    # todo: tick this bt
    print(scene.BT)