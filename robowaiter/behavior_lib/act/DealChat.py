import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.llm_client.ask_llm import ask_llm


class DealChat(Act):
    def __init__(self):
        super().__init__()
        self.chat_history = ""

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        name,sentence = self.scene.state['chat_list'].pop(0)

        if name == "Goal":
            self.create_sub_task(sentence)
            return ptree.common.Status.RUNNING

        self.scene.state["attention"]["customer"] = name
        self.scene.state["serve_state"] = {
            "last_chat_time": self.scene.time,
        }


        self.chat_history += sentence + '\n'

        res_dict = ask_llm(sentence)
        answer = res_dict["Answer"]
        self.scene.chat_bubble(answer) # 机器人输出对话
        self.chat_history += answer + '\n'

        goal = res_dict["Goal"]
        if goal:
            if "{" not in goal:
                goal = {str(goal)}
            else:
                goal=eval(goal)

        if goal is not None:
            print(f'goal：{goal}')

            self.create_sub_task(goal)

        if self.scene.show_bubble:
            self.scene.chat_bubble(f"{answer}")

        return ptree.common.Status.RUNNING


    def create_sub_task(self,goal):
        self.scene.robot.expand_sub_task_tree(goal)
