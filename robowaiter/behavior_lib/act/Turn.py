import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class Clean(Act):
    can_be_expanded = True
    num_args = 1
    valid_args = [('AC','ACTemperature','TubeLight','HallLight','Curtain'),
            ('Off','On','Up','Down','Clean','Dirty')]

    def __init__(self, *args):
        super().__init__(*args)
        self.target_obj = self.args[0]
        self.op = self.args[1]
        self.op_type = 13

        if self.target_obj=="AC":
            self.op_type = 13
        elif self.target_obj=="ACTemperature":
            if self.op == 'Up':
                self.op_type = 14
            elif self.op == 'Down':
                self.op_type = 15
        elif self.target_obj=="TubeLight":
            if self.op == 'On':
                self.op_type = 6
            elif self.op == 'Off':
                self.op_type = 8
        elif self.target_obj=="HallLight":
            if self.op == 'On':
                self.op_type = 9
            elif self.op == 'Off':
                self.op_type = 10
        elif self.target_obj=="Curtain":
            if self.op == 'On':
                self.op_type = 11
            elif self.op == 'Off':
                self.op_type = 12

    @classmethod
    def get_info(cls,arg):
        info = {}
        # 明天写
        # info["pre"]= {f'Holding(Nothing)'}
        # if arg == "Table1":
        #     info["add"]= {f'Is(Table1,Clean)'}
        #     info["del"] = {f'Is(Table1,Dirty)'}
        # elif arg == "Floor":
        #     info["add"] = {f'Is(Floor,Clean)'}
        #     info["del"] = {f'Is(Floor,Dirty)'}
        # elif arg == "Chairs":
        #     info["add"] = {f'Is(Chairs,Clean)'}
        #     info["del"] = {f'Is(Chairs,Dirty)'}
        return info

    def _update(self) -> ptree.common.Status:

        self.scene.move_task_area(self.op_type)
        self.scene.op_task_execute(self.op_type)

        self.scene.state["condition_set"].union(self.info["add"])
        self.scene.state["condition_set"] -= self.info["del"]
        return Status.RUNNING