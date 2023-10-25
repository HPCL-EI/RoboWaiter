import py_trees as ptree
from robowaiter.behavior_tree.ptml import ptmlCompiler


def load_bt_from_ptml(scene, ptml_path, behavior_lib_path):
    ptml_bt = ptmlCompiler.load(scene, ptml_path, behavior_lib_path)
    bt =  ptree.trees.BehaviourTree(ptml_bt)

    with open(ptml_path, 'r') as f:
        ptml = f.read()

    print(f'BT loaded: \n {ptml}')

    # print(ptree.display.unicode_tree(root=bt.root, show_status=True))
    return bt

# class BehaviorTree(ptree):
#     def __init__(self):
#         super().__init__()