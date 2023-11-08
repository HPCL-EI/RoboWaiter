import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act

class ExploreEnv(Act):

    def __init__(self, *args):
        super().__init__(*args)

    def _update(self) -> ptree.common.Status:
        return ptree.common.Status.SUCCESS
