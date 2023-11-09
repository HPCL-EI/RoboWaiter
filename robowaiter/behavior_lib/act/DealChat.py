import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.llm_client.ask_llm import ask_llm

fixed_answers = {
    "测试VLM：做一杯咖啡":
        '''
        测试VLM：做一杯咖啡
        ---
        {"At(Coffee,Bar)"}
        '''
    ,
    "测试VLN：前往桌子":
        '''
        测试VLN：前往桌子
        ---
        {"At(Robot,Table)"}
        '''
    ,
}
class DealChat(Act):
    def __init__(self):
        super().__init__()

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        chat = self.scene.state['chat_list'].pop()

        # 判断是否是测试
        if chat in fixed_answers.keys():
            sentence,goal = fixed_answers[chat].split("---")
            sentence = sentence.strip()
            goal = goal.strip()
            print(f'机器人回答：{sentence}')
            goal = eval(goal)
            print(f'goal：{goal}')

            self.create_sub_task(goal)
        else:
            answer = ask_llm(chat)
            print(f"机器人回答：{answer}")
            if self.scene.show_bubble:
                self.scene.chat_bubble(f"机器人回答：{answer}")

        return ptree.common.Status.RUNNING


    def create_sub_task(self,goal):
        self.scene.robot.expand_sub_task_tree(goal)
