import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act

from robowaiter.llm_client.multi_rounds import ask_llm,new_history

class DealChat(Act):
    def __init__(self):
        super().__init__()
        self.chat_history = ""
        self.function_success = False
        self.func_map = {
            "create_sub_task": self.create_sub_task,
            "get_object_info": self.get_object_info
        }

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        name,sentence = self.scene.state['chat_list'].pop(0)

        if name == "Goal":
            self.create_sub_task(goal=sentence)
            return ptree.common.Status.RUNNING

        if name not in self.scene.state["chat_history"]:
            self.scene.state["chat_history"][name] = new_history()

        history = self.scene.state["chat_history"][name]
        self.scene.state["attention"]["customer"] = name
        self.scene.state["serve_state"] = {
            "last_chat_time": self.scene.time,
        }

        function_call, response = ask_llm(sentence,history,func_map=self.func_map)


        self.scene.chat_bubble(response) # 机器人输出对话

        return ptree.common.Status.RUNNING


    def create_sub_task(self,**args):
        try:
            goal = args['goal']

            w = goal.split(")")
            goal_set = set()
            goal_set.add(w[0] + ")")
            if len(w)>1:
                for x in w[1:]:
                    if x != "":
                        goal_set.add(x[1:] + ")")
            self.function_success = True
        except:
            print("参数解析错误")

        self.scene.robot.expand_sub_task_tree(goal_set)


    def get_object_info(self,**args):
        try:
            obj = args['obj']

            self.function_success = True
        except:
            obj = None
            print("参数解析错误")

        near_object = "None"
        if obj == "洗手间":
            near_object = "大门"

        return near_object