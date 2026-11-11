
from EXP.exp_tools import collect_action_nodes,get_start,BTTest,goal_transfer_str,collect_cond_nodes,BTTest_Merge,BTTest_Merge_easy_medium_hard,collect_action_nodes_multiple_num
import copy
import random
import re

seed = 1
random.seed(seed)
multiple_num=1

action_list = collect_action_nodes_multiple_num(random,multiple_num)

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

# dataset_ls = [easy_data_set,medium_data_set,hard_data_set]
# parm_difficule_ls = ['Easy','Medium','Hard']

dataset_ls = [medium_data_set]
parm_difficule_ls = ['Medium']


goal_set_ls=[]
for index,dataset in enumerate(dataset_ls):

    sections = re.split(r'\n\s*\n', dataset)
    outputs_list = [[] for _ in range(len(sections))]

    # goal_set_ls = []
    for i,s in enumerate(sections):
        x,y = s.strip().splitlines()
        x = x.strip()
        y = y.strip().replace("Goal: ","")
        # goal_set_ls.append(goal_transfer_ls_set(y))
        goal_set_ls.append(y)

goal_states = goal_set_ls

merge_result=[]
max_merge_times=16

for merge_time in range(max_merge_times):
    if merge_time%5==0:
        print("========== merge_time=",merge_time,"================")

    param_ls=[parm_difficule_ls[0],merge_time]

    baseline_result = \
        BTTest_Merge_easy_medium_hard(bt_algo_opt=True, goal_states=goal_states,action_list=action_list,\
                     start_robowaiter=start_robowaiter,merge_time=merge_time)
    tmp=[]
    tmp.extend(param_ls)
    tmp.extend(baseline_result)

    merge_result.append(tmp)



import pandas as pd
df = pd.DataFrame(merge_result, columns=[
                    'difficult',
                    'merge_time',
                    'tree_size_avg', 'tree_size_std',
                     'ticks_avg', 'ticks_std',
                    'cond_ticks_avg', 'cond_ticks_std',
                    'cost_avg', 'cost_std',
                    'plan_time_avg', 'plan_time_std', 'plan_time_total'])
import time
time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()).replace("-","").replace(":","")
csv_file_path = 'merged_result_'+parm_difficule_ls[0]+'_stats_'+str(max_merge_times)+"_states="+str(state_num)+"_acts="+str(len(action_list))+"_"+time_str+'.csv'
df.to_csv(csv_file_path, index=True)
print("CSV文件已生成:", csv_file_path)