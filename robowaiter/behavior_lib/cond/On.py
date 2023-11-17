import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond

class On(Cond):
    can_be_expanded = True
    num_params = 2
    valid_params = [tuple(Cond.all_object),
            tuple(Cond.all_place)]


    def __init__(self,*args):
        super().__init__(*args)


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?

        # print("self.name:",self.name)
        # print("On: condition_set:",self.scene.state["condition_set"])

        if self.name in self.scene.state["condition_set"]:
            return ptree.common.Status.SUCCESS
        else:
            return ptree.common.Status.FAILURE

        # if self.scene.state['chat_list'] == []:
        #     return ptree.common.Status.FAILURE
        # else:
        #     return ptree.common.Status.SUCCESS
