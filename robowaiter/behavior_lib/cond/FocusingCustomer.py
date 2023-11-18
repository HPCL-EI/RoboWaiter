import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond

class FocusingCustomer(Cond):

    def __init__(self):
        super().__init__()


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        if "customer" in self.scene.state['attention']:
            return ptree.common.Status.SUCCESS
        else:
            return ptree.common.Status.FAILURE
