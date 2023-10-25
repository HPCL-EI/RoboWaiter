import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib.Behavior import Bahavior

class Chatting(Bahavior):
    def __init__(self, name: str, scene):
        super().__init__(name, scene)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)

    def initialise(self) -> None:
        return super().initialise()

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        if self.scene.state['chat_list'] == []:
            return ptree.common.Status.FAILURE
        else:
            return ptree.common.Status.SUCCESS

    def terminate(self, new_status: ptree.common.Status) -> None:
        return super().terminate(new_status)
