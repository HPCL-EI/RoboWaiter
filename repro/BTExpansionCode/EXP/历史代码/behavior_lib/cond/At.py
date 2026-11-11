import py_trees as ptree
from typing import Any
from EXP.behavior_lib._base.Cond import Cond
import itertools

class Near(Cond):
    can_be_expanded = True
    num_params = 2

    valid_args = list(itertools.product(('Robot','Customer'), tuple(Cond.all_object | Cond.tables_for_placement | Cond.tables_for_guiding | {'Customer'})))
    valid_args.remove(('Customer','Customer'))
    valid_args = tuple(valid_args)

    def __init__(self,*args):
        super().__init__(*args)


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?

        # self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio)

        if self.name in self.scene.state["condition_set"]:
            return ptree.common.Status.SUCCESS
        else:
            return ptree.common.Status.FAILURE

        # if self.scene.state['chat_list'] == []:
        #     return ptree.common.Status.FAILURE
        # else:
        #     return ptree.common.Status.SUCCESS
