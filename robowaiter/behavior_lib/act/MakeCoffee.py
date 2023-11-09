import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class MakeCoffee(Act):

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def cond_sets(self):
        pre = {"At(Robot,Bar)"}
        add = {"At(Coffee,Bar)"}
        de = {}
        return pre,add,de

    def _update(self) -> ptree.common.Status:
        op_type = 1
        self.scene.move_task_area(op_type)
        self.scene.op_task_execute(op_type)
        self.scene.state["condition_set"].add("At(Coffee,Bar)")
        return Status.RUNNING