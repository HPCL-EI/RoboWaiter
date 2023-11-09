import py_trees as ptree
from robowaiter.behavior_tree.ptml import ptmlCompiler


def load_bt_from_ptml(scene, ptml_path, behavior_lib_path):
    ptml_bt = ptmlCompiler.load(scene, ptml_path, behavior_lib_path)
    bt =  ptree.trees.BehaviourTree(ptml_bt)

    with open(ptml_path, 'r') as f:
        ptml = f.read()

    print(f'BT loaded:')
    print_tree_from_root(bt.root)
    # print(ptree.display.unicode_tree(root=bt.root, show_status=True))
    return bt

def load_bt_from_ptml_str(scene, ptml_path, behavior_lib_path):
    ptml_bt = ptmlCompiler.load(scene, ptml_path, behavior_lib_path)
    bt =  ptree.trees.BehaviourTree(ptml_bt)

    with open(ptml_path, 'r') as f:
        ptml = f.read()

    print(f'BT loaded:')
    print_tree_from_root(bt.root)
    # print(ptree.display.unicode_tree(root=bt.root, show_status=True))
    return bt


def print_tree_from_root(node, indent=0):
    """
    Recursively prints the tree, each child with increased indentation.

    :param node: The current tree node to print.
    :param indent: The number of '\t' to prefix the line with.
    """
    # 打印当前节点，增加缩进来表示层级
    print(f"{'    ' * indent}{node.print_name}")
    # 如果该节点有子节点，递归打印子节点
    if hasattr(node, "children"):
        for child in node.children:
            print_tree_from_root(child, indent + 1)

def find_node_by_name(tree, name):
    """
    Find a node in the behavior tree with the specified name.

    :param tree: The root of the behavior tree or subtree.
    :param name: The name of the node to find.
    :return: Node with the specified name, or None if not found.
    """
    if tree.name == name:
        return tree
    elif hasattr(tree, "children"):  # Check if the tree has children
        for child in tree.children:
            result = find_node_by_name(child, name)
            if result is not None:
                return result
    return None



# class BehaviorTree(ptree):
#     def __init__(self):
#         super().__init__()