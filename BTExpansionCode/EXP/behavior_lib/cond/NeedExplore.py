import py_trees as ptree
from typing import Any
from EXP.behavior_lib._base.Cond import Cond

class NeedExplore(Cond):
    def __init__(self):
        super().__init__()

    def _update(self) -> ptree.common.Status:
        # arg_str = self.arg_str
        #
        # if f'EnvExplored()' not in self.scene.state["condition_set"]:
        #     return ptree.common.Status.SUCCESS
        # else:
        #     return ptree.common.Status.FAILURE
        return ptree.common.Status.FAILURE


        # if self.scene.status?
        # if self.scene.state['map']['2d'] == None:
        #     return ptree.common.Status.FAILURE
        # else:
        #     return ptree.common.Status.SUCCESS
