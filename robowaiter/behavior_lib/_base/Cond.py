import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Behavior import Bahavior, Status

class Cond(Bahavior):
    print_name_prefix = "cond "
    type = 'Cond'

    def __init__(self,*args):
        super().__init__(*args)


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        if self.scene.state['chat_list'] == []:
            return Status.FAILURE
        else:
            return Status.SUCCESS
