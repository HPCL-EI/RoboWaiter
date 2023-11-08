import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Behavior import Bahavior, Status

class Cond(Bahavior):
    def __init__(self):
        super().__init__()


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        if self.scene.state['chat_list'] == []:
            return Status.FAILURE
        else:
            return Status.SUCCESS
