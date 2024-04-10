import random
import numpy as np
import copy
import time
from OptimalBTExpansionAlgorithm_cond2act import Action,generate_random_state,state_transition
from Examples import *
import os
output_path = os.path.join(os.path.dirname(__file__), "outputs")
from tools import print_action_data_table,BTTest_act_start_goal

def copy_act(a,actions,action_num,state,states,copy_time):

    ca_num=0

    for ct in range(copy_time):
        ca = copy.deepcopy(a)

        # pre\del 都为原来的子集
        # pre_num = random.randint(0, len(ca.pre))
        # ca.pre = set(random.sample(ca.pre, pre_num))
        #
        # del_set_num = random.randint(0, len(ca.del_set))
        # ca.del_set = set(random.sample(ca.del_set, del_set_num))

        ca.cost = random.randint(1, 100)
        if not ca in actions:
            ca_num+=1
            ca.name = "a" + str(action_num)
            action_num += 1
            actions.append(ca)
            s = state_transition(state, a)
            if s in states:
                pass
            else:
                states.append(s)
    return ca_num

def get_act_start_goal(seed=1, literals_num=10, depth=10, iters=10, total_count=1000,max_copy_times=5):



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
        state = copy.deepcopy(start)
        states.append(state)


        for i in range(0, depth):
            a = Action()
            a.generate_from_state_local(state, literals_num_set)
            a.cost = random.randint(1, 10)
            if not a in actions:
                a.name = "a" + str(action_num)
                action_num += 1
                actions.append(a)

            # if max_copy_times!=0:
            #     copy_times = random.randint(1, max_copy_times)
            #     ca_num = copy_act(a,actions,action_num,state,states,copy_times)
            #     action_num += ca_num

            state = state_transition(state, a)
            if state in states:
                pass
            else:
                states.append(state)


        goal = states[-1]
        # state = copy.deepcopy(start)
        for i in range (0,iters):
            a = Action()
            state = generate_random_state(literals_num)
            a.generate_from_state_local(state, literals_num_set)

            a.cost = random.randint(50, 100)
            if not a in actions:
                a.name = "a"+str(action_num)
                action_num+=1
                actions.append(a)

            # if max_copy_times!=0:
            #     copy_times = random.randint(1, max_copy_times)
            #     ca_num = copy_act(a,actions,action_num,state,states,copy_times)
            #     action_num += ca_num

            state = state_transition(state,a)
            if state in states:
                pass
            else:
                states.append(state)
            # state = random.sample(states,1)[0]



        act_list.append(actions)
        start_list.append(start)
        goal_list.append(goal)

        total_action_num.append(len(actions))
        total_state_num.append(len(states))

    end_time_0=time.time()

    print("Total Time:", end_time_0-start_time_0)
    print("Total Time (start_to_goal):", total_time_dic["start_to_goal"])
    print("Total Time (random_act):",total_time_dic["random_act"])
    print("Average Number of States:", round(np.mean(total_state_num),3))  # 1000次问题的平均状态数
    print("Average Number of Actions", round(np.mean(total_action_num),3)) # 1000次问题的平均行动数
    # print_action_data_table(goal, start, list(actions))
    return act_list, start_list, goal_list,round(np.mean(total_state_num),3),round(np.mean(total_action_num),3)



# # 设置生成规划问题集的超参数：文字数、解深度、迭代次数
seed = 1
random.seed(1)
np.random.seed(1)
literals_num = 2
depth = 2
iters = 2

# literals_num_ls=[10,10,10,100,100,10,10,10,100,100]
# depth_ls=[10,10,10,10,10,50,50,50,50,50]
# iters_ls=[10,100,1000,10,1000,10,100,1000,10,1000]
# literals_num_ls=[10,10,10,10,  100,100,100,100]
# depth_ls=[10,10,10,10,  10,10,10,10]
# iters_ls=[5,10,100,500,  5,10,100,500]

# literals_num_ls=[10,10,10,10,100,100,100,100]  #+[100,100]
# depth_ls=[10,10,10,10,10,10,10,10]  #+[10,10]
# iters_ls=[5,10,100,500,5,10,100,500]  #+[int(500/2),int(500/4)]
# max_copy_times_ls=8*[5]  #+[10,20]

# literals_num_ls=[10,10,10,10,100,100,100,100] + [100,100]  #+[100,100]
# depth_ls=15 * [10]
# iters_ls=[5,10,100,300,5,10,100,300,175,105]  #+[int(500/2),int(500/4)]
# max_copy_times_ls=8*[5] + [10,20]  #+[10,20]

literals_num_ls=[10]  #+[100,100]
depth_ls=15 * [10]
iters_ls=[10]  #+[int(500/2),int(500/4)]
max_copy_times_ls=6*[5]+[10,20]  #+[10,20]


all_result=[]

for literals_num,depth,iters,max_copy_times in zip(literals_num_ls, depth_ls, iters_ls,max_copy_times_ls):
    print(f"\n------literals_num: {literals_num},depth:{depth},iters:{iters},max_copy_times:{max_copy_times}-----------")
    # 为 act建立 add映射

    act_list, start_list, goal_list,state_avg,act_avg = get_act_start_goal(seed=seed, literals_num=literals_num, depth=depth, iters=iters,
                                                         total_count=2,max_copy_times=max_copy_times)

    param_ls = [max_copy_times,literals_num,depth,iters,state_avg,act_avg]

    baseline_result = BTTest_act_start_goal(bt_algo_opt=False, act_list=act_list, start_list=start_list,
                                            goal_list=goal_list,literals_num=literals_num)

    obt_result = BTTest_act_start_goal(bt_algo_opt=True, act_list=act_list, start_list=start_list, goal_list=goal_list,literals_num=literals_num)

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
                    'max_actcopy',
                    'literals_num','depth','iters','state','act',
                    'btalgorithm',
                    'tree_size_avg', 'tree_size_std',
                     'ticks_avg', 'ticks_std',
                    'cost_avg', 'cost_std',
                    'step_avg','step_std',
                    'state_num_avg','state_num_std',
                    'expand_num_avg','expand_num_std',
                    'plan_time_avg', 'plan_time_std', 'plan_time_total'])

time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()).replace("-","").replace(":","")
csv_file_path = 'bt_result_copyact=1-5_pre_del_time='+time_str+'.csv'
df.to_csv(csv_file_path, index=True)
print("CSV文件已生成:", csv_file_path)