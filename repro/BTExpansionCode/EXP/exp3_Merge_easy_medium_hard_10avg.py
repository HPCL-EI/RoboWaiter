import numpy as np

from EXP.exp_tools import state_transition,collect_action_nodes,get_start,BTTest,goal_transfer_str,collect_cond_nodes,BTTest_Merge,BTTest_Merge_easy_medium_hard
import copy
import random
import re
from OptimalBTExpansionAlgorithm import Action,OptBTExpAlgorithm
seed = 1
random.seed(seed)
multiple_num=5
iters_times= 10
iter_action_ls = collect_action_nodes(random,multiple_num,iters_times)


start_robowaiter = get_start()

# 计算state总数
state_num, vaild_state_num= collect_cond_nodes()
# print("meta states num: ",state_num)
# print("states num: ",vaild_state_num)
# print("act num: ",len(action_list))

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
max_merge_times=20
dataset_ls = [easy_data_set,medium_data_set,hard_data_set]
parm_difficule_ls = ['Easy','Medium','Hard']

# dataset_ls = [hard_data_set]
# parm_difficule_ls = ['Hard']

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

    import time

    # 针对一个difficult 跑10次
    condticks_avg_ls=[]

    merge_cond_tick_total = [[] for merge_time in range(max_merge_times)]

    for iter in range(iters_times):

        action_list = iter_action_ls[iter]

        planning_time_ls=[]
        planning_time_total=0
        for count, goal_str in enumerate(goal_states):
            goal = copy.deepcopy(goal_transfer_str(goal_str))
            algo = OptBTExpAlgorithm(verbose=False)
            algo.clear()
            algo.bt_merge=False
            start_time = time.time()
            algo_right = algo.run_algorithm(start_robowaiter, goal, action_list)
            end_time = time.time()
            planning_time_ls.append(end_time - start_time)
            planning_time_total += (end_time - start_time)

            for merge_time in range(max_merge_times):
                # 根据子树个数进行合并
                bt = algo.merge_subtree(merge_time)
                # 计算合并后的 cond tick
                # 开始从初始状态运行行为树，测试
                state = copy.deepcopy(start_robowaiter)
                steps = 0
                current_cond_tick_time = 0
                val, obj, cost, tick_time, cond_times = bt.cost_tick_cond(state, 0, 0, 0)  # tick行为树，obj为所运行的行动
                current_cond_tick_time += cond_times
                while val != 'success' and val != 'failure':  # 运行直到行为树成功或失败
                    state = state_transition(state, obj)
                    val, obj, cost, tick_time, cond_times = bt.cost_tick_cond(state, 0, 0, 0)
                    current_cond_tick_time += cond_times
                    if (val == 'failure'):
                        print("bt fails at step", steps)
                        error = True
                        break
                    steps += 1
                    if (steps >= 500):  # 至多运行500步
                        break
                # 检查执行后状态满不满足，只有 goal 里有一个满足就行
                error = True
                for gg in goal:
                    if gg <= state:
                        error = False
                        break
                if error:
                    print("error")
                    break
                # 结束从初始状态运行行为树，测试
                merge_cond_tick_total[merge_time].append(current_cond_tick_time)
        print("iter:", iter,"cond:",merge_cond_tick_total)
    merge_cond_tick_total_np = np.array(merge_cond_tick_total)
    merge_cond_tick_averages = np.mean(merge_cond_tick_total_np, axis=1)
    print(merge_cond_tick_averages)

    all_result.append(merge_cond_tick_averages)


import pandas as pd
df = pd.DataFrame(all_result)
import time
time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()).replace("-","").replace(":","")
csv_file_path = 'merged_result_easy_medium_hard_'+time_str+'.csv'
df.to_csv(csv_file_path, index=True)
print("CSV文件已生成:", csv_file_path)