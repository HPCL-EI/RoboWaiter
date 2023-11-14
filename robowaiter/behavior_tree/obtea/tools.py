

from tabulate import tabulate
import numpy as np
import random
from robowaiter.behavior_tree.obtea.OptimalBTExpansionAlgorithm import Action,OptBTExpAlgorithm
import time


def print_action_data_table(goal,start,actions):
    data = []
    for a in actions:
        data.append([a.name , a.pre , a.add , a.del_set , a.cost])
    data.append(["Goal" ,goal ," " ,"Start" ,start])
    print(tabulate(data, headers=["Name", "Pre", "Add" ,"Del" ,"Cost"], tablefmt="fancy_grid"))  # grid plain simple github fancy_grid


# 从状态随机生成一个行动
def generate_from_state(act,state,num):
    for i in range(0,num):
        if i in state:
            if random.random() >0.5:
                act.pre.add(i)
                if random.random() >0.5:
                    act.del_set.add(i)
                continue
        if random.random() > 0.5:
            act.add.add(i)
            continue
        if random.random() >0.5:
            act.del_set.add(i)

def print_action(act):
    print (act.pre)
    print(act.add)
    print(act.del_set)



#行为树测试代码
def BTTest(seed=1,literals_num=10,depth=10,iters=10,total_count=1000):
    print("============= BT Test ==============")
    random.seed(seed)
    # 设置生成规划问题集的超参数：文字数、解深度、迭代次数
    literals_num=literals_num
    depth = depth
    iters= iters
    total_tree_size = []
    total_action_num = []
    total_state_num = []
    total_steps_num=[]
    #fail_count=0
    #danger_count=0
    success_count =0
    failure_count = 0
    planning_time_total = 0.0
    # 实验1000次
    for count in range (total_count):

        action_num = 1

        # 生成一个规划问题，包括随机的状态和行动，以及目标状态
        states = []
        actions = []
        start = generate_random_state(literals_num)
        state = start
        states.append(state)
        #print (state)
        for i in range (0,depth):
            a = Action()
            generate_from_state(a,state,literals_num)
            if not a in actions:
                a.name = "a"+str(action_num)
                action_num+=1
                actions.append(a)
            state = state_transition(state,a)
            if state in states:
                pass
            else:
                states.append(state)
                #print(state)

        goal = states[-1]
        state = start
        for i in range (0,iters):
            a = Action()
            generate_from_state(a,state,literals_num)
            if not a in actions:
                a.name = "a"+str(action_num)
                action_num+=1
                actions.append(a)
            state = state_transition(state,a)
            if state in states:
                pass
            else:
                states.append(state)
            state = random.sample(states,1)[0]

        # 选择测试本文算法btalgorithm，或对比算法weakalgorithm
        algo = OptBTExpAlgorithm()
        #algo = Weakalgorithm()
        start_time = time.time()
        # print_action_data_table(goal, start, list(actions))
        if algo.run_algorithm(start, goal, actions):#运行算法，规划后行为树为algo.bt
            total_tree_size.append( algo.bt.count_size()-1)
            # algo.print_solution()  # 打印行为树
        else:
            print ("error")
        end_time = time.time()
        planning_time_total += (end_time-start_time)

        #开始从初始状态运行行为树，测试
        state=start
        steps=0
        val, obj = algo.bt.tick(state)#tick行为树，obj为所运行的行动
        while val !='success' and val !='failure':#运行直到行为树成功或失败
            state = state_transition(state,obj)
            val, obj = algo.bt.tick(state)
            if(val == 'failure'):
                print("bt fails at step",steps)
            steps+=1
            if(steps>=500):#至多运行500步
                break
        if not goal <= state:#错误解，目标条件不在执行后状态满足
            #print ("wrong solution",steps)
            failure_count+=1

        else:#正确解，满足目标条件
            #print ("right solution",steps)
            success_count+=1
            total_steps_num.append(steps)
        algo.clear()
        total_action_num.append(len(actions))
        total_state_num.append(len(states))

    print ("success:",success_count,"failure:",failure_count)#算法成功和失败次数
    print("Total Tree Size: mean=",np.mean(total_tree_size), "std=",np.std(total_tree_size, ddof=1))#1000次测试树大小
    print ("Total Steps Num: mean=",np.mean(total_steps_num),"std=",np.std(total_steps_num,ddof=1))
    print ("Average number of states:",np.mean(total_state_num))#1000次问题的平均状态数
    print ("Average number of actions",np.mean(total_action_num))#1000次问题的平均行动数
    print("Planning Time Total:",planning_time_total,planning_time_total/1000.0)
    print("============ End BT Test ===========")

    # xiao cai
    # success: 1000 failure: 0
    # Total Tree Size: mean= 35.303 std= 29.71336526001515
    # Total Steps Num: mean= 1.898 std= 0.970844240101644
    # Average number of states: 20.678
    # Average number of actions 20.0
    # Planning Time Total: 0.6280641555786133 0.0006280641555786133

    # our start
    # success: 1000 failure: 0
    # Total Tree Size: mean= 17.945 std= 12.841997192488865
    # Total Steps Num: mean= 1.785 std= 0.8120556843187752
    # Average number of states: 20.678
    # Average number of actions 20.0
    # Planning Time Total: 1.4748523235321045 0.0014748523235321046

    # our
    # success: 1000 failure: 0
    # Total Tree Size: mean= 48.764 std= 20.503626574406358
    # Total Steps Num: mean= 1.785 std= 0.8120556843187752
    # Average number of states: 20.678
    # Average number of actions 20.0
    # Planning Time Total: 3.3271877765655518 0.0033271877765655516

