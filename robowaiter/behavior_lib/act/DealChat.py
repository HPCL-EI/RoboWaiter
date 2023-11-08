import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.llm_client.ask_llm import ask_llm
from robowaiter.behavior_tree.utils import load_bt_from_ptml,print_tree_from_root

class DealChat(Act):
    def __init__(self):
        super().__init__()

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        chat = self.scene.state['chat_list'].pop()

        # 判断是否是测试
        if chat =="测试VLN":
            self.scene.chat_bubble(f"开始测试VLN")
            self.scene.state['sub_task_list'].append(("At(Robot, Table)",))

        answer = ask_llm(chat)
        print(f"机器人回答：{answer}")
        self.scene.chat_bubble(f"机器人回答：{answer}")

        return ptree.common.Status.RUNNING


def create_sub_task(goal):
    pass