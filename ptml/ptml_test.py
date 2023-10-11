import os
import py_trees as ptree

from ptmlCompiler import load


if __name__ == '__main__':

    project_path = "."
    
    ptml_path = os.path.join(project_path, 'CoffeeDelivery.ptml')
    behavior_lib_path = os.path.join(project_path, 'behaviour_lib')
    # load
    bt = load(ptml_path, behavior_lib_path)
    # ptree.display.render_dot_tree(bt)
    # build and tick
    bt = ptree.trees.BehaviourTree(bt)
    # todo: tick this bt
