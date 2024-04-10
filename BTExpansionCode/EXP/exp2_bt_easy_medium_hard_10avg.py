
from EXP.exp_tools import collect_action_nodes,get_start,BTTest,goal_transfer_str,collect_cond_nodes,BTTest_easy_medium_hard,collect_action_nodes_multiple_num
import copy
import random
import re
from dataset.data_process_check import format_check,word_correct,goal_transfer_ls_set
import time
import numpy as np
seed = 1
random.seed(seed)

multiple_num= 5
iters_times= 10
# iter_action_ls=[]
iter_action_ls = collect_action_nodes(random,multiple_num,iters_times)


# for act in action_list:
#     print(act.name,act.cost)
start_robowaiter = get_start()
# 计算state总数
state_num, vaild_state_num= collect_cond_nodes()

easy_data_set_file = "../dataset/easy_instr_goal.txt"
medium_data_set_file = "../dataset/medium_instr_goal.txt"
hard_data_set_file = "../dataset/hard_instr_goal.txt"
with open(easy_data_set_file, 'r', encoding="utf-8") as f:
    easy_data_set = f.read().strip()
with open(medium_data_set_file, 'r', encoding="utf-8") as f:
    medium_data_set = f.read().strip()
with open(hard_data_set_file, 'r', encoding="utf-8") as f:
    hard_data_set = f.read().strip()
dataset_ls = [easy_data_set,medium_data_set,hard_data_set]
parm_difficule_ls = ['Easy','Medium','Hard']


# dataset_ls = [hard_data_set]
# parm_difficule_ls = ['Hard']


all_result=[]

for index, dataset in enumerate(dataset_ls):

    print(f"\n----------- {parm_difficule_ls[index]} ----------\n")

    sections = re.split(r'\n\s*\n', dataset)
    outputs_list = [[] for _ in range(len(sections))]
    goal_set_ls = []
    for i, s in enumerate(sections):
        x, y = s.strip().splitlines()
        x = x.strip()
        y = y.strip().replace("Goal: ", "")
        goal_set_ls.append(y)
    goal_states = goal_set_ls


    b_condticks_ls=[]
    obtea_condticks_ls=[]
    b_cost_ls=[]
    obtea_cost_ls=[]

    for iter in range(iters_times):
        action_list = iter_action_ls[iter]

        print("meta states num: ",state_num)
        print("states num: ",vaild_state_num)
        print("act num: ",len(action_list))


        obt_result = BTTest_easy_medium_hard(bt_algo_opt=True, goal_states=goal_states,action_list=action_list,start_robowaiter=start_robowaiter)
        # print("\n")
        # 对比
        baseline_result = BTTest_easy_medium_hard(bt_algo_opt=False, goal_states=goal_states,action_list=action_list,start_robowaiter=start_robowaiter)

        obtea_condticks_ls.append(obt_result[4])
        b_condticks_ls.append(baseline_result[4])

        obtea_cost_ls.append(obt_result[5])
        b_cost_ls.append(baseline_result[5])



    param_ls=[parm_difficule_ls[index]]
    a_result=[]
    a_result.extend(param_ls)
    a_result.extend([round(np.mean(b_condticks_ls), 1),round(np.mean(obtea_condticks_ls), 1),round(np.mean(b_cost_ls), 1),round(np.mean(obtea_cost_ls), 1)])
    all_result.append(a_result)


print(all_result)

# import pandas as pd
# df = pd.DataFrame(all_result, columns=[
#                     'difficult',
#                     'btalgorithm',
#                     'tree_size_avg', 'tree_size_std',
#                      'ticks_avg', 'ticks_std',
#                     'cost_avg', 'cost_std',
#                     'plan_time_avg', 'plan_time_std', 'plan_time_total'])
#
# time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()).replace("-","").replace(":","")
# csv_file_path = 'cage_bt_result_='+time_str+'.csv'
# df.to_csv(csv_file_path, index=True)
# print("CSV文件已生成:", csv_file_path)