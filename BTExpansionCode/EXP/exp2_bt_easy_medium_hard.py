
from EXP.exp_tools import collect_action_nodes,get_start,BTTest,goal_transfer_str,collect_cond_nodes,BTTest_easy_medium_hard
import copy
import random
import re
from dataset.data_process_check import format_check,word_correct,goal_transfer_ls_set
import time

seed = 1
random.seed(seed)

multiple_num= 0
action_list = collect_action_nodes(random,multiple_num)
# for act in action_list:
#     print(act.name,act.cost)

start_robowaiter = get_start()

# 计算state总数
state_num, vaild_state_num= collect_cond_nodes()
print("meta states num: ",state_num)
print("states num: ",vaild_state_num)
print("act num: ",len(action_list))

goal_states = []

easy_data_set_file = "../dataset/easy_instr_goal.txt"
medium_data_set_file = "../dataset/medium_instr_goal.txt"
hard_data_set_file = "../dataset/hard_instr_goal.txt"
with open(easy_data_set_file, 'r', encoding="utf-8") as f:
    easy_data_set = f.read().strip()
with open(medium_data_set_file, 'r', encoding="utf-8") as f:
    medium_data_set = f.read().strip()
with open(hard_data_set_file, 'r', encoding="utf-8") as f:
    hard_data_set = f.read().strip()


all_result=[]

dataset_ls = [easy_data_set,medium_data_set,hard_data_set]
parm_difficule_ls = ['Easy','Medium','Hard']

# dataset_ls = [easy_data_set]
# parm_difficule_ls = ['Easy']

for index,dataset in enumerate(dataset_ls):

    sections = re.split(r'\n\s*\n', dataset)
    outputs_list = [[] for _ in range(len(sections))]

    goal_set_ls=[]
    for i,s in enumerate(sections):
        x,y = s.strip().splitlines()
        x = x.strip()
        y = y.strip().replace("Goal: ","")
        # goal_set_ls.append(goal_transfer_ls_set(y))
        goal_set_ls.append(y)


    goal_states = goal_set_ls
    # goal_states={"On_Milk_WindowTable6"}
    # goal_states={"On_Chips_WindowTable6 & (On_Milk_WindowTable6 | On_Yogurt_WindowTable6 )"}
    # goal_states={"(~On_Coffee_Table1 | ~On_Dessert_Table2) & ~RobotNear_Bar2"}
    # goal_states={"(~On_Milk_Bar | ~On_Yogurt_Bar) & ~RobotNear_Bar"}

    obt_result = BTTest_easy_medium_hard(bt_algo_opt=True, goal_states=goal_states,action_list=action_list,start_robowaiter=start_robowaiter)
    # print("\n")
    # 对比
    baseline_result = BTTest_easy_medium_hard(bt_algo_opt=False, goal_states=goal_states,action_list=action_list,start_robowaiter=start_robowaiter)

    param_ls=[parm_difficule_ls[index]]

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
                    'difficult',
                    'btalgorithm',
                    'tree_size_avg', 'tree_size_std',
                     'ticks_avg', 'ticks_std',
                    'cost_avg', 'cost_std',
                    'plan_time_avg', 'plan_time_std', 'plan_time_total'])

time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()).replace("-","").replace(":","")
csv_file_path = 'cage_bt_result_='+time_str+'.csv'
df.to_csv(csv_file_path, index=True)
print("CSV文件已生成:", csv_file_path)