import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond

class HasSubTask(Cond):
    def __init__(self):
        super().__init__()

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        if not self.scene.sub_task_seq or not self.scene.sub_task_seq.children:
            return ptree.common.Status.FAILURE
        else:
            return ptree.common.Status.SUCCESS
