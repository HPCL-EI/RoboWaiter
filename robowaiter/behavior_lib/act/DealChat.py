import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.llm_client.ask_llm import ask_llm


class DealChat(Act):
    def __init__(self):
        super().__init__()
        self.chat_history = ""

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        chat = self.scene.state['chat_list'].pop()
        if isinstance(chat,set):
            self.create_sub_task(chat)
            return ptree.common.Status.RUNNING


        self.chat_history += chat + '\n'

        res_dict = ask_llm(chat)
        answer = res_dict["Answer"]
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
