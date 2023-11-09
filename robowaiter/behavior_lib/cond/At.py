import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond

class At(Cond):
    can_be_expanded = True
    num_params = 2
    valid_params = '''
        Coffee, Bar
        Robot, Bar
    '''

    def __init__(self,*args):
        super().__init__(*args)


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        arg_str = self.arg_str

        if f'At({arg_str})' in self.scene.state["condition_set"]:
            return ptree.common.Status.SUCCESS
        else:
            return ptree.common.Status.FAILURE

        # if self.scene.state['chat_list'] == []:
        #     return ptree.common.Status.FAILURE
        # else:
        #     return ptree.common.Status.SUCCESS
