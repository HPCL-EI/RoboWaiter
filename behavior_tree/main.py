import py_trees
from behavior_library import *


def LoadMainTree() -> py_trees.trees.BehaviourTree:
    """
        此方法用于加载固定的顶层行为树（不包括实际执行）

        Args: None
    """

    seq_subtree_0 = py_trees.composites.Sequence(
        name='seq_subtree_0',
        memory=False,
        children=[IsChatting(), Chatting()]
    )

    seq_subtree_1 = py_trees.composites.Sequence(
        name='seq_subtree_1',
        memory=False,
        children=[IsTakingAction(), TakingAction()]
    )

    seq_subtree_2 = py_trees.composites.Sequence(
        name='seq_subtree_2',
        memory=False,
        children=[IsSomethingMore(), TakingMoreAction()]
    )

    root = py_trees.composites.Selector(
        name='selector_root',
        memory=False,
        children=[seq_subtree_0, seq_subtree_1, seq_subtree_2]
    )

    return py_trees.trees.BehaviourTree(root)


def LoadSubTree(path: str) -> py_trees.behaviour.Behaviour:
    """
        此方法用于从ptml文件中加载行为树（不包括实际执行）

        Args:
            -- path: ptml文件的路径
    """
    # TODO
    pass


if '__name__' == '__main__':
    btree = LoadMainTree()


    def print_tree(tree):
        print(py_trees.display.unicode_tree(root=tree.root, show_status=True))


    try:
        btree.tick_tock(
            period_ms=500,
            number_of_iterations=py_trees.trees.CONTINUOUS_TICK_TOCK,
            pre_tick_handler=None,
            post_tick_handler=print_tree
        )
    except KeyboardInterrupt:
        btree.interrupt()
