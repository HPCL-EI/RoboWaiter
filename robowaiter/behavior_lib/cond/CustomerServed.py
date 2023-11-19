import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond
import itertools

class CustomerServed(Cond):
    can_be_expanded = True

    def __init__(self,*args):
        super().__init__(*args)


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?

        customer = self.scene.state["attention"]["customer"]
        serve_state = self.scene.state["serve_state"][customer]
        if serve_state['served']:
            return ptree.common.Status.SUCCESS
        else:
            return ptree.common.Status.FAILURE

        # if self.scene.state["attention"]["customer"]
        #
        # if self.name in self.scene.state["condition_set"]:
        #     return ptree.common.Status.SUCCESS
        # else:
        #     return ptree.common.Status.FAILURE

        # if self.scene.state['chat_list'] == []:
        #     return ptree.common.Status.FAILURE
        # else:
        #     return ptree.common.Status.SUCCESS
