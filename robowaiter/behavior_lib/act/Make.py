import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class Make(Act):
    can_be_expanded = True
    num_args = 1
    valid_args = (
        "Coffee","Water","Dessert"
    )

    def __init__(self, *args):
        super().__init__(*args)
        self.target_obj = self.args[0]


    @classmethod
    def get_info(cls,arg):
        info = {}
        info["pre"]= {f'Holding(Nothing)'}
        info['del'] = set()
        if arg == "Coffee":
            info["add"]= {f'On(Coffee,CoffeeTable)'}
        elif arg == "Water":
            info["add"] = {f'On(Water,WaterTable)'}
        elif arg == "Dessert":
            info["add"] = {f'On(Dessert,Bar)'}
        return info
    def _update(self) -> ptree.common.Status:
        op_type = 1
        self.scene.move_task_area(op_type)
        self.scene.op_task_execute(op_type)
        self.scene.state["condition_set"].union(self.info["add"])
        self.scene.state["condition_set"] -= self.info["del"]
        return Status.RUNNING