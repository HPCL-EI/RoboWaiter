import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act

class ExploreEnv(Act):
    # can_be_expanded = True
    can_be_expanded = False
    num_args=0
    valid_args=()

    def __init__(self, *args):
        super().__init__(*args)

    @classmethod
    def get_info(cls):
        info = {}
        info["pre"] = set()
        info["add"] = {"EnvExplored()"}
        info["del_set"] = set()
        return info

    def _update(self) -> ptree.common.Status:
        # explore algorithm
        self.scene.state["condition_set"]|= self.info["add"]

        return ptree.common.Status.RUNNING
