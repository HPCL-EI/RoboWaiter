import random
import numpy as np
import copy
import time
from OptimalBTExpansionAlgorithm_cond2act import Action,generate_random_state,state_transition
from Examples import *
import os
output_path = os.path.join(os.path.dirname(__file__), "outputs")

from tools import print_action_data_table,BTTest_act_start_goal
# from tools import print_action_data_table,BTTest,BTTest_act_start_goal,get_act_start_goal


def get_act_start_goal(seed=1, literals_num=10, depth=10, iters=10, total_count=1000,pre_max=10000):

    literals_num_set = {i for i in range(literals_num)}

    act_list = []
    start_list = []
    goal_list = []
    total_action_num=[]
    total_state_num=[]

    total_time_dic = {"start_to_goal": 0,
                      "random_act":0}
    start_time_0=time.time()
    for count in range(total_count):
        # 生成一个规划问题，包括随机的状态和行动，以及目标状态
        action_num = 1
        states = []
        actions = []
        start = generate_random_state(literals_num)
        state_set = {i for i in range(literals_num)}
        state = copy.deepcopy(start)
        states.append(state)
        # print (state)

        for i in range(0, depth):
            a = Action()
            # a.generate_from_state_local(state, literals_num_set,pre_max)
            a.generate_from_state_local(state, literals_num_set)
            a.cost = random.randint(1, 100)
            if not a in actions:
                a.name = "a" + str(action_num)
                action_num += 1
                actions.append(a)
            state = state_transition(state, a)
            if state in states:
                pass
            else:
                states.append(state)
                # print(state)
        goal = states[-1]

        k_act_total = int(iters* (2 / 3)/depth)

        if k_act_total<1:
            k_act_total = random.randint(1, 2)

        # for k in range(int(iters/depth)):
        for k in range(k_act_total):
            depth_random = random.randint(depth, depth+10)
            for i in range(0, depth - 1):
                a = Action()

                start_time = time.time()
                # a.generate_from_state_local(state, literals_num_set,pre_max)
                a.generate_from_state_local(state, literals_num_set)
                end_time = time.time()
                total_time_dic["start_to_goal"] += end_time - start_time

                a.cost = random.randint(1, 100)
                if not a in actions:
                    a.name = "a" + str(action_num)
                    action_num += 1
                    actions.append(a)
                state = state_transition(state, a)
                if state in states:
                    pass
                else:
                    states.append(state)

            if not goal <= states[-1]:
                a = Action()

                # if len(states[-1])==0:
                #     a.pre=set()
                # else:
                pre_num = random.randint(0, min(pre_max,len(states[-1])))
                # a.pre = set(np.random.choice(list(states[-1]), pre_num, replace=False))
                a.pre = set(random.sample(states[-1], pre_num))

                a.add = goal - states[-1]
                def_set = state_set - goal

                # if len(def_set)==0:
                #     a.del_set=set()
                # else:
                def_num = random.randint(0, len(def_set))
                # a.del_set = set(np.random.choice(list(def_set), def_num, replace=False))
                a.del_set = set(random.sample(def_set, def_num))

                a.cost = random.randint(1, 100)
                a.name = "a" + str(action_num)
                action_num += 1
                actions.append(a)




        state = copy.deepcopy(start)
        for i in range(0, int(iters* (2 / 3))):
            a = Action()

            start_time = time.time()
            # a.generate_from_state_local(state, literals_num_set,pre_max)
            a.generate_from_state_local(state, literals_num_set)
            end_time = time.time()
            total_time_dic["random_act"] += end_time - start_time

            if not a in actions:
                a.name = "a" + str(action_num)
                action_num += 1
                actions.append(a)
            state = state_transition(state, a)
            if state in states:
                pass
            else:
                states.append(state)
            state = random.sample(states, 1)[0]


        act_list.append(actions)
        start_list.append(start)
        goal_list.append(goal)

        total_action_num.append(len(actions))
        total_state_num.append(len(states))

    end_time_0=time.time()

    print("Total Time:", end_time_0-start_time_0)
    print("Total Time (start_to_goal):", total_time_dic["start_to_goal"])
    print("Total Time (random_act):",total_time_dic["random_act"])
    print("Average Number of States:", np.mean(total_state_num))  # 1000次问题的平均状态数
    print("Average Number of Actions", np.mean(total_action_num))  # 1000次问题的平均行动数
    # print_action_data_table(goal, start, list(actions))
    return act_list, start_list, goal_list



# # 设置生成规划问题集的超参数：文字数、解深度、迭代次数
seed = 1
random.seed(1)
np.random.seed(1)
literals_num = 3
depth = 3
iters = 3

# total_count = 5
act_list, start_list, goal_list = get_act_start_goal(seed=seed, literals_num=literals_num, depth=depth, iters=iters,
                                                     total_count=1000,pre_max=10000)
BTTest_act_start_goal(bt_algo_opt=True, act_list=act_list, start_list=start_list, goal_list=goal_list)
# BTTest_act_start_goal(bt_algo_opt=False, act_list=act_list, start_list=start_list, goal_list=goal_list)
