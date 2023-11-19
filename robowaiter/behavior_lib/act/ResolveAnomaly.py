import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act

class ResolveAnomaly(Act):

    def __init__(self, *args):
        super().__init__(*args)

    def _update(self) -> ptree.common.Status:
        # explore algorithm
        self.scene.state["chat_list"].insert(0,("Goal",'Is(HallLight,On)'))

        return ptree.common.Status.RUNNING
