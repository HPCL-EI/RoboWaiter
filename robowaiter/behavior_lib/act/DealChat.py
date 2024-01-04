import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act

# from robowaiter.llm_client.multi_rounds_retri import ask_llm, new_history
from robowaiter.llm_client.multi_rounds import ask_llm, new_history
import random
from collections import deque

from translate import Translator
from sympy import to_dnf


translator = Translator(to_lang="zh")
translator.from_lang = 'en'
translator.to_lang = 'zh-cn'

import spacy
# nlp = spacy.load('en_core_web_lg')
nlp_zh = spacy.load('zh_core_web_lg')


class History(deque):
    def __init__(self,scene,customer_name):
        super().__init__(maxlen=7)
        self.scene = scene
        self.customer_name = customer_name

    def append(self, __x) -> None:
        super().append(__x)
        self.scene.ui_func(("new_history",self.customer_name, __x))


class DealChat(Act):
    def __init__(self):
        super().__init__()
        self.chat_history = ""
        self.function_success = False
        self.func_map = {
            "create_sub_task": self.create_sub_task,
            "stop_serve": self.stop_serve,
            "get_object_info": self.get_object_info,
            # "find_location": self.find_location,
            "get_number_of_objects": self.get_number_of_objects,
        }

    def _update(self) -> ptree.common.Status:
        # if self.scene.status?
        name, sentence = self.scene.state['chat_list'].pop(0)

        if name == "Goal":
            self.create_sub_task(goal=sentence)
            self.scene.ui_func(("new_history", "System", {
                "role": "user",
                "content": "set goal: " + sentence
            }))

            return ptree.common.Status.RUNNING

        if name not in self.scene.state["chat_history"]:
            self.scene.state["chat_history"][name] = History(self.scene,name)

        history = self.scene.state["chat_history"][name]
        self.scene.state["attention"]["customer"] = name
        self.scene.state["serve_state"][name] = {
            "last_chat_time": self.scene.time,
            "served": False
        }

        function_call, response = ask_llm(sentence,history,func_map=self.func_map)


        self.scene.chat_bubble(response) # 机器人输出对话

        return ptree.common.Status.RUNNING


    def obj_name_en2zh(self,obj):
        obj = obj.replace("_", " ")
        obj = translator.translate(obj) #转成中文
        print("====obj:=======",obj)
        return obj

    def create_sub_task(self, **args):
        try:
            goal = args['goal']
            #
            # w = goal.split(")")
            # goal_set = set()
            # goal_set.add(w[0] + ")")
            # if len(w) > 1:
            #     for x in w[1:]:
            #         if x != "":
            #             goal_set.add(x[1:] + ")")
            # self.function_success = True

            # 解析谓词公式
            # 如果不正确，

            # 如果正确，传入两个set
            # goal = "On_Coffee_Bar | On_Yogur_Bar & At_Robot_Bar"
            goal_dnf = str(to_dnf(goal, simplify=True))
            # print(goal_dnf)
            goal_set = []
            if '|' in goal or '&' in goal or 'Not' in goal or '_' in goal:
                goal_ls = goal_dnf.split("|")
                for g in goal_ls:
                    g_set = set()
                    g = g.replace(" ", "").replace("(", "").replace(")", "")
                    g = g.split("&")
                    for literal in g:
                        if '_' in literal:
                            first_part, rest = literal.split('_', 1)
                            literal = first_part + '(' + rest
                            # 添加 ')' 到末尾
                            literal += ')'
                            # 替换剩余的 '_' 为 ','
                            literal = literal.replace('_', ',')
                        g_set.add(literal)
                    goal_set.append(g_set)
            else:
                g_set = set()
                w = goal.split(")")
                g_set.add(w[0] + ")")
                if len(w) > 1:
                    for x in w[1:]:
                        if x != "":
                            g_set.add(x[1:] + ")")
                goal_set.append(g_set)

            print("goal_set:",goal_set)
            # goal_set = [set(["On(Coffee,Bar)", "At(Robot,Bar)"]), set(["On(Yogurt,Bar)", "At(Robot,Bar)"])]
            self.function_success = True

        except:
            print("参数解析错误")

        # 添加相似性比较

        self.scene.robot.expand_sub_task_tree(goal_set)


    def get_object_info(self,**args):
        try:
            obj = args['obj']
            self.function_success = True
        except:
            obj = None
            print("参数解析错误")


        near_object = None
        d = {"保温杯": "二号桌子","洗手间":"前门","卫生间":"前门"}


        # 先把 obj 转成中文

        # 写死的内容
        if obj in d.keys():
            near_object = d[obj]
            near_object = f"{obj}在{near_object}附近"
            obj_id = 0
        else: # 根据相似性查找物品位置
            obj = self.obj_name_en2zh(obj)

            max_similarity = 0.02
            similar_word = None

            # 场景中现有物品
            cur_things = set()
            for item in self.scene.status.objects:
                cur_things.add(self.scene.objname_en2zh_dic[item.name])
            # obj与现有物品进行相似度匹配 中文的匹配
            # print("==========obj==========:",obj)
            query_token = nlp_zh(obj)
            for w in cur_things:
                word_token = nlp_zh(w)
                similarity = query_token.similarity(word_token)
                # print("similarity:", similarity, w)
                if similarity > max_similarity:
                    max_similarity = similarity
                    similar_word = w
            if similar_word:
                print("max_similarity:",max_similarity,"similar_word:",similar_word)

            if similar_word:   # 存在同义词说明场景中存在该物品
                # near_object = random.choices(list(cur_things), k=5)   # 返回场景中的5个物品
                # 找到距离最近的物品
                similar_word_en = self.scene.objname_zh2en_dic[similar_word]
                obj_dict = self.scene.status.objects
                if len(obj_dict)!=0:

                    for id, obji in enumerate(obj_dict):
                        if obji.name == similar_word_en:
                            obj_info = obj_dict[id]
                            objx,objy,objz = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
                            break

                    # 获取离它最近的物品
                    # min_dis = float('inf')
                    # obj_id = -1
                    # near_object = None
                    # for id,obji in enumerate(obj_dict):
                    #     if obji.name != similar_word_en:
                    #         obj_info = obj_dict[id]
                    #         dis = self.scene.getDistanc3D((obj_info.location.X, obj_info.location.Y, obj_info.location.Z),(objx,objy,objz))
                    #         if dis<min_dis:
                    #             min_dis = dis
                    #             obj_id = id
                    #             near_object = obji.name
                    #
                    #     near_object = f"{obj}在{self.scene.objname_en2zh_dic[near_object]}附近"

                    # 直接输出在哪个桌子上
                    min_dis = float('inf')
                    table_name = -1
                    near_object = None
                    for key,values in self.place_have_obj_xyz_dic.items():
                        dis = self.scene.getDistanc3D(values,(objx, objy, objz))
                        if dis<min_dis:
                            min_dis = dis
                            table_name = key
                    # near_object = f"{obj}在{self.place_en2zh_name[table_name]}附近"
                    # near_object = self.place_en2zh_name[table_name]
                    near_object =  obj + "在" + self.place_en2zh_name[table_name] +"附近"
                    # near_object = self.place_en2zh_name[table_name]
                    # near_object = "在" + self.place_en2zh_name[table_name] + "附近"
        return near_object




    # def find_location(self, **args):
    #     try:
    #         location = args['obj']
    #         self.function_success = True
    #     except:
    #         obj = None
    #         print("参数解析错误")
    #
    #     d = {"保温杯": "二号桌子"}
    #     if location in d.keys():
    #         result = d[obj]
    #     else:
    #         result = "None"
    #     return result
    #     # 用户咨询的地点
    #     query_token = nlp(location)
    #     max_similarity = 0
    #     similar_word = None
    #     # 到自己维护的地点列表中找同义词
    #     for w in self.scene.all_loc_en:
    #         word_token = nlp(w)
    #         similarity = query_token.similarity(word_token)
    #         if similarity > max_similarity:
    #             max_similarity = similarity
    #             similar_word = w
    #     print("similarity:", max_similarity, "similar_word:", similar_word)
    #     # 存在同义词说明客户咨询的地点有效
    #     if similar_word:
    #         mp = list(self.scene.loc_map_en[similar_word])
    #         near_location = random.choice(mp)
    #     return near_location

    def get_number_of_objects(self,**args):
        try:
            obj = args['obj']
            self.function_success = True
            obj = self.obj_name_en2zh(obj)
        except:
            obj = None
            print("参数解析错误")

        # 找到最近的中文
        max_similarity = 0.02
        similar_word = None

        # obj 是中文
        # obj = translator.translate(obj) #转成中文
        # print("obj:",obj)
        query_token = nlp_zh(obj)
        for real_obj_name in self.scene.objname_zh2en_dic.keys(): # 在中文名字里面找
            word_token = nlp_zh(real_obj_name)
            similarity = query_token.similarity(word_token)
            # print("similarity:",similarity,real_obj_name)
            if similarity > max_similarity:
                max_similarity = similarity
                similar_word = real_obj_name
        if similar_word:
            print("max_similarity:",max_similarity,"similar_word:",similar_word)

        count = 0
        similar_word_en = self.scene.objname_zh2en_dic[similar_word]
        if similar_word_en != "Customer":
            for item in self.scene.status.objects:
                if item.name == similar_word_en:
                    count+=1
        else:
            count = len(self.scene.status.walkers)

        # obj 是英文
        # query_token = nlp(obj)
        # for real_obj_name in self.scene.objname_en2zh_dic.keys(): # 在中文名字里面找
        #     word_token = nlp(real_obj_name)
        #     similarity = query_token.similarity(word_token)
        #     print("similarity:",similarity,real_obj_name)
        #     if similarity > max_similarity:
        #         max_similarity = similarity
        #         similar_word = real_obj_name
        # if similar_word:
        #     print("max_similarity:",max_similarity,"similar_word:",similar_word)
        return "有"+str(count)+"个"+obj



    def stop_serve(self,**args):
        customer = self.scene.state["attention"]["customer"]
        serve_state = self.scene.state["serve_state"][customer]

        serve_state['served'] = True

        return "好的"


