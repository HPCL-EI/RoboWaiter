import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class DelSubTree(Act):

    def __init__(self, *args):
        super().__init__(*args)

    def _update(self) -> ptree.common.Status:
        sub_task_tree = self.parent
        self.scene.sub_task_seq.children.remove(sub_task_tree)
        return Status.RUNNING