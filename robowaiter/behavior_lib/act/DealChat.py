import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Behavior import Bahavior
from robowaiter.llm_client.ask_llm import ask_llm

class DealChat(Bahavior):
    def __init__(self):
        super().__init__()

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        chat = self.scene.state['chat_list'].pop()
        answer = ask_llm(chat)
        print(f"机器人回答：{answer}")
        self.scene.chat_bubble(f"机器人回答：{answer}")

        return ptree.common.Status.RUNNING
