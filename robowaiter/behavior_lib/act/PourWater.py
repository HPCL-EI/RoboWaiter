import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class PourWater(Act):

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def cond_sets(self):
        self.pre = {"At(Robot,WaterTable)","NotHolding"}
        self.add = {"On(Water,WaterTable)"}
        self.de = {}
        return self.pre,self.add,self.de

    def _update(self) -> ptree.common.Status:
        op_type = 2
        self.scene.move_task_area(op_type)
        self.scene.op_task_execute(op_type)
        self.scene.state["condition_set"].update(self.add)
        return Status.RUNNING