import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond

class Chatting(Cond):


    def __init__(self):
        super().__init__()


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        if self.scene.state['chat_list'] == []:
            return ptree.common.Status.FAILURE

        name,sentence = self.scene.state['chat_list'][0]
        if name == "Goal":
            return ptree.common.Status.SUCCESS


        if "customer" in self.scene.state["attention"]:
            attention_customer = self.scene.state["attention"]["customer"]
            if name == attention_customer:
                return ptree.common.Status.SUCCESS
            else:
                # self.scene.chat_bubble("请稍等一下")  # 机器人输出对话
                # self.scene.wait_history.add(sentence)

                return ptree.common.Status.FAILURE
        else:
            self.scene.state["attention"]["customer"] = name
            return ptree.common.Status.SUCCESS
