import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status
import itertools

class Turn(Act):
    can_be_expanded = True
    num_args = 2
    valid_args = [('AC','TubeLight','HallLight','Curtain'),
            ('On','Off')]

    valid_args = list(itertools.product(valid_args[0], valid_args[1]))
    valid_args.extend([('ACTemperature','Up'),('ACTemperature','Down')])
    valid_args = tuple(valid_args)



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
                self.op_type = 12
            elif self.op == 'Off':
                self.op_type = 11

    @classmethod
    def get_info(cls,*arg):
        info = {}
        info["pre"] = set()
        if arg[0] == "TubeLight" or arg[0] == "HallLight" or arg[0] == 'AC':
            info["pre"] |= {f'Holding(Nothing)'}
            if arg[1] == "On":
                info["pre"] |= {f'Not Active({arg[0]})'}
                info["add"] = {f'Active({arg[0]})'}
                info["del_set"] = {f'Off({arg[0]})'}
            elif arg[1]=="Off":
                info["pre"] |= {f'Active({arg[0]})'}
                info["add"] = {f'Not Active({arg[0]})'}
                info["del_set"] = {f'Active({arg[0]})'}

        # elif arg[0] == 'AC':
        #     if arg[1] == "On":
        #         info["pre"] |= {f'Not Active({arg[0]})'}
        #         info["add"] = {f'Active({arg[0]})',f'Not Low({arg[0]})'}
        #         info["del_set"] = {f'Off({arg[0]})',f'Low({arg[0]})'}
        #     elif arg[1]=="Off":
        #         info["pre"] |= {f'Active({arg[0]})'}
        #         info["add"] = {f'Not Active({arg[0]})'}
        #         info["del_set"] = {f'Active({arg[0]})',f'Not Low({arg[0]})',f'Low({arg[0]})'}

        elif arg[0]=='ACTemperature':
            info["pre"] = {f'Holding(Nothing)',f'Active(AC)'}
            if arg[1]=="Up":
                # info["pre"] |= {f'Low({arg[0]})'}
                info["add"] = {f'Not Low({arg[0]})'}
                info["del_set"] = {f'Low({arg[0]})'}
            elif arg[1]=="Down":
                # info["pre"] |= {f'Not Low({arg[0]})'}
                info["add"] = {f'Low({arg[0]})'}
                info["del_set"] = {f'Not Low({arg[0]})'}

        elif arg[0]=='Curtain':
            if arg[1]=="On":
                info["pre"] |= {f'Closed({arg[0]})'}
                info["add"] = {f'Not Closed({arg[0]})'}
                info["del_set"] = {f'Closed({arg[0]})'}
            elif arg[1]=="Off":
                info["pre"] |= {f'Not Closed({arg[0]})'}
                info["add"] = {f'Closed({arg[0]})'}
                info["del_set"] = {f'Not Closed({arg[0]})'}
        return info

    def _update(self) -> ptree.common.Status:

        if self.scene.show_ui:
            self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio)

        self.scene.move_task_area(self.op_type)
        self.scene.op_task_execute(self.op_type)
        if self.scene.show_ui:
            self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio)
        self.scene.state["condition_set"] |= (self.info["add"])
        self.scene.state["condition_set"] -= self.info["del_set"]

        return Status.RUNNING