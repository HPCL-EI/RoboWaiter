import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class Clean(Act):
    can_be_expanded = True
    num_args = 1
    valid_args = (
        'Table1','Floor','Chairs'
    )

    def __init__(self, *args):
        super().__init__(*args)
        self.target_obj = self.args[0]
        self.op_type = 5
        if self.target_obj=="Table1":
            self.op_type = 5
        elif self.target_obj=="Floor":
            self.op_type = 4
        elif self.target_obj=="Chairs":
            self.op_type = 7


    @classmethod
    def get_info(cls,arg):
        info = {}
        info["pre"]= {f'Holding(Nothing)'}
        if arg == "Table1":
            info["add"]= {f'Is(Table1,Clean)'}
            info["del"] = {f'Is(Table1,Dirty)'}
        elif arg == "Floor":
            info["add"] = {f'Is(Floor,Clean)'}
            info["del"] = {f'Is(Floor,Dirty)'}
        elif arg == "Chairs":
            info["add"] = {f'Is(Chairs,Clean)'}
            info["del"] = {f'Is(Chairs,Dirty)'}
        return info

    def _update(self) -> ptree.common.Status:

        self.scene.move_task_area(self.op_type)
        self.scene.op_task_execute(self.op_type)

        self.scene.state["condition_set"].union(self.info["add"])
        self.scene.state["condition_set"] -= self.info["del"]
        return Status.RUNNING