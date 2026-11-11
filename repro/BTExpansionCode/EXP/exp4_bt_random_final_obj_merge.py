import random
import numpy as np
import copy
import time
from OptimalBTExpansionAlgorithm import Action,generate_random_state,state_transition
from Examples import *
import os
output_path = os.path.join(os.path.dirname(__file__), "outputs")
from tools import print_action_data_table,BTTest_act_start_goal


def modify_set(s, obj):
    return {f"{num}_{obj}" for num in s}

def get_act_start_goal(seed=1, max_copy_times=5,cond_pred=10, depth=10, act_pred=10, total_count=1000,obj_num=0):
    max_copy_times=max_copy_times

    literals_num_set = {i for i in range(cond_pred)}
    all_obj_set = {i for i in range(obj_num)}

    act_list = []
    start_list = []
    goal_list = []

    total_literals_count=[]
    total_states_num=[]
    total_action_num = []
    total_act_pred_num=[]

    start_time_0=time.time()
    for count in range(total_count):

        actions_ls = []
        literals_obj_set=set()
        state_num = 0
        action_num = 1

        # 生成一个规划问题，包括随机的状态和行动，以及目标状态
        states = []
        actions = []
        start = generate_random_state(cond_pred)
        state = copy.deepcopy(start)
        states.append(state)
        obj_index = random.randint(0, obj_num-1)  # 确定一个物体

        aa_main = [] # 主路径上的动作谓词

        for i in range(0, depth):
            a = Action()
            a.generate_from_state_local(state, literals_num_set,all_obj_set,obj_num,obj_index)
            a.cost = random.randint(0, 100)

            if not a in actions:
                a.name = "a" + str(action_num)
                action_num += 1
                actions.append(a)
                aa_main.append(a)

            state = state_transition(state, a)
            # 存入一个状态
            if state in states:
                pass
            else:
                states.append(state)
                state_num+= a.vaild_num


        goal = states[-1]
        # state = copy.deepcopy(start)
        for i in range (0,act_pred):
            a = Action()
            state = generate_random_state(cond_pred) # 随机选择一个状态
            a.generate_from_state_local(state, literals_num_set, all_obj_set, obj_num)
            a.cost = random.randint(0, 100)
            if not a in actions:
                a.name = "a"+str(action_num)
                action_num+=1
                actions.append(a)

            # 存入一个状态
            if state in states:
                pass
            else:
                states.append(state)
                state_num += a.vaild_num
            state = state_transition(state,a)
            # 存入一个状态
            if state in states:
                pass
            else:
                states.append(state)
                state_num += a.vaild_num

        for act in actions:
            # if act.vild_args==set():
            #     print(a.name,a.pre,a.add,a.cost,a.vaild_num)
            for obj in act.vild_args:
                a = Action(
                    name=act.name + "_" + str(obj),
                    pre=modify_set(act.pre, obj),
                    add=modify_set(act.add, obj),
                    del_set=modify_set(act.del_set, obj),
                    cost=act.cost,
                )
                if a.pre != set():
                    literals_obj_set |= a.pre
                if a.add != set():
                    literals_obj_set |= a.add
                if a.del_set != set():
                    literals_obj_set |= a.del_set
                actions_ls.append(a)

        # actions_ls = [
        #     copy.deepcopy(act).update(
        #         name=act.name + "_" + str(obj),
        #         pre=modify_set(act.pre, obj),
        #         del_set=modify_set(act.del_set, obj),
        #         add=modify_set(act.add, obj)
        #     )
        #     for act in actions
        #     for obj in act.vild_args
        # ]

        if max_copy_times != 0:
            for a in aa_main:
                # if a.vild_args == set():
                #     print(a.name, a.pre, a.add, a.cost, a.vaild_num)
                copy_times = random.randint(0, max_copy_times)
                for ck in range(copy_times):
                    ca=copy.deepcopy(a)
                    ca.cost = random.randint(1, 100)
                    ca = ca.update(
                        name=ca.name + "_" + str(obj_index),
                        pre=modify_set(ca.pre, obj_index),
                        del_set=modify_set(ca.del_set, obj_index),
                        add=modify_set(ca.add, obj_index)
                    )
                    if ca.pre != set():
                        literals_obj_set |= ca.pre
                    if ca.add != set():
                        literals_obj_set |= ca.add
                    if ca.del_set != set():
                        literals_obj_set |= ca.del_set
                    actions_ls.append(ca)

        # 计算所有 文字



        start = modify_set(start, obj_index)
        goal = modify_set(goal,obj_index)


        act_list.append(actions_ls)
        start_list.append(start)
        goal_list.append(goal)
        # print(literals_obj_set)
        # print(len(literals_obj_set))
        total_literals_count.append(len(literals_obj_set))
        total_action_num.append(len(actions_ls))
        total_act_pred_num.append(len(actions))
        total_states_num.append(state_num)

    end_time_0=time.time()

    print("Total Time:", end_time_0-start_time_0)
    # print("Total Time (start_to_goal):", total_time_dic["start_to_goal"])
    # print("Total Time (random_act):",total_time_dic["random_act"])
    print("Average Number of literals_obj", round(np.mean(total_literals_count), 3))  # 1000次问题的平均行动数
    print("Average Number of States", round(np.mean(total_states_num), 3))  # 1000次问题的平均行动数
    print("Average Number of Actions", round(np.mean(total_action_num),3)) # 1000次问题的平均行动数
    print("Average Number of Act Pred", round(np.mean(total_act_pred_num), 3))  # 1000次问题的平均行动数
    # print_action_data_table(goal, start, list(actions))
    return act_list, start_list, goal_list, \
        round(np.mean(total_literals_count), 3),\
        round(np.mean(total_states_num),3),round(np.mean(total_action_num),3),round(np.mean(total_act_pred_num),3)



# # 设置生成规划问题集的超参数：文字数、解深度、迭代次数
seed = 1
random.seed(1)
np.random.seed(1)



# obj_num_ls =  [100,500] +4*[100] +[300,500] #9* [100,300,500]
# cond_pred_ls= [10,50,10,50] + 4*[50]
# act_pred_ls=  [0,40,0,0,20,40,40,40]
# max_copy_times_ls= [0,0] + 6*[5]


# obj_num_ls =  [100,500] +4*[100] +[300,500] #9* [100,300,500]
# cond_pred_ls= [10,50,10,50] + 4*[50]
# act_pred_ls=  [0,40,0,0,20,40,40,40]
# max_copy_times_ls= [0,0] + 3*[5]

obj_num_ls =  [500]  #9* [100,300,500]
cond_pred_ls= [50]
act_pred_ls=  [40]
max_copy_times_ls= [5,5]


# obj_num_ls =  9*[100,300,500] #9* [100,300,500]
# # Iterations  Action Predicates
# act_pred_ls= 3*[0] + 3*[20] + 3*[40]
# act_pred_ls = 3*act_pred_ls
# #Condition Predicates
# cond_pred_ls= 9* [10] + 9* [30] + 9*[50]

# obj_num_ls = [5]
# # Iterations  Action Predicates
# act_pred_ls= [0]
# #Condition Predicates
# cond_pred_ls= [2]
#
# max_copy_times_ls= 27*[5]
# depth_ls=[10]*27



depth_ls=[10]*27




all_result=[]

new_all_result=[]

for cond_pred,depth,act_pred,max_copy_times,obj_num in zip(cond_pred_ls, depth_ls, act_pred_ls,max_copy_times_ls,obj_num_ls):
    print(
        f"\n------depth:{depth},obj: {obj_num},cond_pred:{cond_pred},act_pred:{act_pred},max_copy_times:{max_copy_times}-----------")
    # print(f"\n------literals_num: {literals_num},depth:{depth},iters:{iters},obj_num:{obj_num},max_copy_times:{max_copy_times}-----------")
    # 为 act建立 add映射

    act_list, start_list, goal_list,literals_obj_count,state_avg,act_avg,act_pred_num = get_act_start_goal(seed=seed, max_copy_times=max_copy_times,\
                                                        cond_pred=cond_pred, depth=depth, act_pred=act_pred,\
                                                         total_count=1000,obj_num=obj_num)

    # param_ls = [max_copy_times,depth, obj_num,iters,act_pred_num,literals_num,act_avg]
    param_ls = [depth,obj_num, cond_pred, act_pred_num, max_copy_times, literals_obj_count, state_avg,act_avg]

    literals_num = cond_pred
    obt_result = BTTest_act_start_goal(bt_algo_opt=True, act_list=act_list, start_list=start_list, goal_list=goal_list,literals_num=literals_num)


    baseline_result = BTTest_act_start_goal(bt_algo_opt=False, act_list=act_list, start_list=start_list,
                                            goal_list=goal_list,literals_num=literals_num)

    m_result=[]
    m_result.extend(param_ls[1:])
    m_result.extend([baseline_result[3],obt_result[2],obt_result[3],baseline_result[4],obt_result[4]])
    new_all_result.append(m_result)


    a_result=[]
    a_result.extend(param_ls)
    a_result.append("OBTEA")
    a_result.extend(obt_result)
    all_result.append(a_result)

    a_result=[]
    a_result.extend(param_ls)
    a_result.append("Baseline")
    a_result.extend(baseline_result)
    all_result.append(a_result)


import pandas as pd
df = pd.DataFrame(all_result, columns=[
                    'depth','obj_num', 'cond_pred', 'act_pred', 'max_copy_times', 'literals_obj_count', 'state_avg','act_avg',
                    'btalgorithm',
                    'tree_size_avg',
                     'ticks_avg',
                    'wm_cond_ticks',
                    'cond_tick_avg',
                    'cost_avg',
                    'step_avg',
                    'expand_num_avg',
                    'plan_time_avg', 'plan_time_total'
])

time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()).replace("-","").replace(":","")
csv_file_path = 'bt_result_1logic='+time_str+'.csv'
df.to_csv(csv_file_path, index=True)
print("CSV文件已生成:", csv_file_path)


df = pd.DataFrame(new_all_result, columns=[
                    'obj_num', 'cond_pred', 'act_pred', 'max_copy_times', 'literals_obj_count', 'state_avg','act_avg',
                    'Cond_B',
                    'Cond_WM',
                    'Cond_OUR',
                    'Cost_B',
                    'Cost_OUR',
])

time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()).replace("-","").replace(":","")
csv_file_path = 'bt_result_random_wm='+time_str+'.csv'
df.to_csv(csv_file_path, index=True)
print("New CSV文件已生成:", csv_file_path)
