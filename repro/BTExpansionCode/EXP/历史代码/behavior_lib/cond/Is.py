import py_trees as ptree
from typing import Any
from EXP.behavior_lib._base.Cond import Cond
import itertools

class Is(Cond):
    can_be_expanded = True
    num_params = 2
    valid_params1 = [('AC','TubeLight','HallLight','Curtain'),
                    ('On','Off')]

    # Closed(Curtain)
    # Off(TubeLight,HallLight,AC)
    # Dirty(Table1,Floor,Chairs)
    # Down(ACTemperature)

    valid_params2 = [('Table1','Floor','Chairs'),
                    ('Clean','Dirty')]
    valid_params3 = [('ACTemperature'),
                    ('Up','Down')]

    valid_args = list(itertools.product(valid_params1[0], valid_params1[1]))
    valid_args.extend(list(itertools.product(valid_params2[0], valid_params2[1])))
    valid_args.extend(list(itertools.product(valid_params3[0], valid_params3[1])))
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
