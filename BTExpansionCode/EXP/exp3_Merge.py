
from EXP.exp_tools import collect_action_nodes,get_start,BTTest,goal_transfer_str,collect_cond_nodes,BTTest_Merge
import copy
import random
seed = 1
random.seed(seed)
multiple_num=6
action_list = collect_action_nodes(random,multiple_num)
# for act in action_list:
#     print(act.name,act.cost)

start_robowaiter = get_start()

# 计算state总数
state_num = collect_cond_nodes()
print("states num: ",state_num)
print("act num: ",len(action_list))

goal_states = []
with open('easy.txt', 'r') as file:
    for line in file:
        clean_line = line.strip()
        goal_states.append(clean_line)
print(goal_states)


merge_result=[]


max_merge_times=21

for merge_time in range(max_merge_times):
    tree_size,plan_time,ticks,cost = \
        BTTest_Merge(bt_algo_opt=True, goal_states=goal_states,action_list=action_list,\
                     start_robowaiter=start_robowaiter,merge_time=merge_time)
    tmp=[]
    tmp.extend(tree_size)
    tmp.extend(plan_time)
    tmp.extend(ticks)
    tmp.extend(cost)
    merge_result.append(tmp)

    if merge_time%5==0:
        print("merge_time=",merge_time,"cost=",cost[0]," ",cost[1])

import pandas as pd
df = pd.DataFrame(merge_result, columns=['tree_size_avg', 'tree_size_std',
                                             'plan_time_avg', 'plan_time_std',
                                             'ticks_avg', 'ticks_std',
                                             'cost_avg', 'cost_std'])
csv_file_path = 'merged_result_stats_'+str(max_merge_times)+"_states="+str(state_num)+"_acts="+str(len(action_list))+'.csv'
df.to_csv(csv_file_path, index=True)
print("CSV文件已生成:", csv_file_path)