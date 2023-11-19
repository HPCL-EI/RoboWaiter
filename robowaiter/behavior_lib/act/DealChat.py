import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act

from robowaiter.llm_client.multi_rounds import ask_llm, new_history
import random

# import spacy
# nlp = spacy.load('en_core_web_lg')


class DealChat(Act):
    def __init__(self):
        super().__init__()
        self.chat_history = ""
        self.function_success = False
        self.func_map = {
            "create_sub_task": self.create_sub_task,
            "get_object_info": self.get_object_info,
            "stop_serve": self.stop_serve,
            "find_location": self.find_location
        }

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        name, sentence = self.scene.state['chat_list'].pop(0)

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


    def create_sub_task(self, **args):
        try:
            goal = args['goal']

            w = goal.split(")")
            goal_set = set()
            goal_set.add(w[0] + ")")
            if len(w) > 1:
                for x in w[1:]:
                    if x != "":
                        goal_set.add(x[1:] + ")")
            self.function_success = True
        except:
            print("参数解析错误")

        self.scene.robot.expand_sub_task_tree(goal_set)

    # def get_object_info(self,**args):
    #     try:
    #         obj = args['obj']
    #
    #         self.function_success = True
    #     except:
    #         obj = None
    #         print("参数解析错误")
    #
    #     near_object = "None"
    #
    #     # 场景中现有物品
    #     cur_things = set()
    #     for item in self.status.objects:
    #         cur_things.add(item.name)
    #     # obj与现有物品进行相似度匹配
    #     query_token = nlp(obj)
    #     for w in self.all_loc_en:
    #         word_token = nlp(w)
    #         similarity = query_token.similarity(word_token)
    #         if similarity > max_similarity:
    #             max_similarity = similarity
    #             similar_word = w
    #     print("max_similarity:",max_similarity,"similar_word:",similar_word)
    #
    #     if similar_word:   # 存在同义词说明场景中存在该物品
    #         near_object = random.choices(list(cur_things), k=5)   # 返回场景中的5个物品
    #
    #     if obj == "洗手间":
    #         near_object = "大门"
    #
    #     return near_object
    #
    # def find_location(self, **args):
    #     try:
    #         location = args['obj']
    #         self.function_success = True
    #     except:
    #         obj = None
    #         print("参数解析错误")
    #
    #     near_location = None
    #     # 用户咨询的地点
    #     query_token = nlp(location)
    #     max_similarity = 0
    #     similar_word = None
    #     # 到自己维护的地点列表中找同义词
    #     for w in self.all_loc_en:
    #         word_token = nlp(w)
    #         similarity = query_token.similarity(word_token)
    #         if similarity > max_similarity:
    #             max_similarity = similarity
    #             similar_word = w
    #     print("similarity:", max_similarity, "similar_word:", similar_word)
    #     # 存在同义词说明客户咨询的地点有效
    #     if similar_word:
    #         mp = list(self.loc_map_en[similar_word])
    #         near_location = random.choice(mp)
    #     return near_location

    def stop_serve(self,**args):


        return "好的"


