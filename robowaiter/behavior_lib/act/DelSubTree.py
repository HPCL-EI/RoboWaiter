import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class DelSubTree(Act):

    def __init__(self, *args):
        super().__init__(*args)

    def _update(self) -> ptree.common.Status:
        # self.scene.state["attention"] = {}
        if "customer" in self.scene.state["attention"]:
            customer = self.scene.state["attention"]["customer"]
            serve_state = self.scene.state["serve_state"][customer]

            serve_state['last_chat_time'] = self.scene.time


        sub_task_tree = self.parent
        self.scene.sub_task_seq.children.remove(sub_task_tree)
        return Status.RUNNING