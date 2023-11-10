import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.llm_client.ask_llm import ask_llm


class DealChat(Act):
    def __init__(self):
        super().__init__()

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        chat = self.scene.state['chat_list'].pop()

        # 判断是否是测试
        # if chat in fixed_answers.keys():
        #     sentence,goal = fixed_answers[chat].split("---")
        #     sentence = sentence.strip()
        #     goal = goal.strip()
        #     print(f'机器人回答：{sentence}')
        #     goal = eval(goal)
        #     print(f'goal：{goal}')
        #
        #     self.create_sub_task(goal)
        # else:
        answer = ask_llm(chat)
        answer_split = answer.split("---")
        sentence = answer_split[0].strip()
        goal = None
        if len(answer_split) > 1:
            goal = answer_split[1].strip()

        print(f'{sentence}')
        if goal:
            goal = eval(goal)
            print(f'goal：{goal}')

            self.create_sub_task(goal)

        if self.scene.show_bubble:
            self.scene.chat_bubble(f"{answer}")

        return ptree.common.Status.RUNNING


    def create_sub_task(self,goal):
        self.scene.robot.expand_sub_task_tree(goal)
