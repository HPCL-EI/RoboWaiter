import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class FreeHands(Act):
    can_be_expanded = True
    num_args = 0
    valid_args = set()

    def __init__(self, *args):
        super().__init__(*args)


    @classmethod
    def get_info(cls):
        info = {}
        # info["pre"]= set()
        info["pre"] ={f'Holding(Nothing)'}
        info['add'] = {f'Holding(Nothing)'}
        info['del_set'] = {f'Holding({obj})' for obj in cls.all_object}
        info['cost'] = 0
        return info

    def _update(self) -> ptree.common.Status:


        if self.scene.show_ui:
            self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio,update_info_count=1)

        self.scene.state["condition_set"] |= (self.info["add"])
        self.scene.state["condition_set"] -= self.info["del_set"]


        return Status.RUNNING