import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib.Behavior import Bahavior
from robowaiter.llm_client.ask_llm import ask_llm

class DealChat(Bahavior):
    def __init__(self, name: str, scene):
        super().__init__(name, scene)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)

    def initialise(self) -> None:
        return super().initialise()

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        chat = self.scene.state['chat_list'].pop()
        answer = ask_llm(chat)
        print(f"机器人回答：{answer}")
        self.scene.chat_bubble(f"机器人回答：{answer}")

        return ptree.common.Status.RUNNING

    def terminate(self, new_status: ptree.common.Status) -> None:
        return super().terminate(new_status)
