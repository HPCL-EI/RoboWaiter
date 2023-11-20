import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond

class FocusingCustomer(Cond):

    def __init__(self):
        super().__init__()


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        if "customer" in self.scene.state['attention']:
            if self.scene.take_picture:
                self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio)
            return ptree.common.Status.SUCCESS
        else:
            goal = Cond.place_xy_yaw_dic['Bar']
            self.scene.walk_to(goal[0] - 5, goal[1], 180, 180, 0)
            return ptree.common.Status.FAILURE
