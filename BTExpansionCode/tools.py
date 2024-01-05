import copy

from tabulate import tabulate
import numpy as np
import random

from OptimalBTExpansionAlgorithm import generate_random_state,state_transition
from OptimalBTExpansionAlgorithm import Action,OptBTExpAlgorithm
from BTExpansionAlgorithm import BTExpAlgorithm # 调用最优行为树扩展算法


import time
np.random.seed(1)
random.seed(1)
def print_action_data_table(goal,start,actions):
    data = []
    for a in actions:
        data.append([a.name ,a.pre ,a.add ,a.del_set ,a.cost])
    data.append(["Goal" ,goal ," " ,"Start" ,start])
    print(tabulate(data, headers=["Name", "Pre", "Add" ,"Del" ,"Cost"], tablefmt="fancy_grid"))  # grid plain simple github fancy_grid


#行为树测试代码
def BTTest_old(bt_algo_opt=True,seed=1,literals_num=10,depth=10,iters=10,total_count=1000):

    if bt_algo_opt:
        print("============= OptBT Test ==============")
    else:
        print("============= XiaoCai BT Test ==============")
    random.seed(seed)
    # 设置生成规划问题集的超参数：文字数、解深度、迭代次数
    literals_num=literals_num
    depth = depth
    iters= iters
    total_tree_size = []
    total_action_num = []
    total_state_num = []
    total_steps_num=[]
    total_cost=[]
    total_tick=[]
    #fail_count=0
    #danger_count=0
    success_count =0
    failure_count = 0
    planning_time_total = 0.0

    error = False

    # 实验1000次
    for count in range (total_count):

        action_num = 1

        # 生成一个规划问题，包括随机的状态和行动，以及目标状态
        states = []
        actions = []
        start = generate_random_state(literals_num)
        state = copy.deepcopy(start)
        states.append(state)
        #print (state)


        for i in range (0,depth):
            a = Action()
            a.generate_from_state(state,literals_num)
            a.cost = random.randint(1, 100)
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
        state = copy.deepcopy(start)
        for i in range (0,iters):
            a = Action()
            a.generate_from_state(state,literals_num)
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

        if bt_algo_opt:
            # if count==874:
            #     algo = OptBTExpAlgorithm(verbose=False)
            # else:
            algo = OptBTExpAlgorithm(verbose=False)
        else:
            algo = BTExpAlgorithm(verbose=False)
        algo.clear()

        #algo = Weakalgorithm()
        start_time = time.time()
        # if count ==  352 : #874:
        #     print_action_data_table(goal, start, list(actions))
        # print_action_data_table(goal, start, list(actions))
        if algo.run_algorithm(start, goal, actions):#运行算法，规划后行为树为algo.bt
            total_tree_size.append( algo.bt.count_size()-1)
            # if count==352:
            #     algo.print_solution()
            # algo.print_solution()  # 打印行为树
        else:
            print ("error")
        end_time = time.time()
        planning_time_total += (end_time-start_time)

        #开始从初始状态运行行为树，测试
        state=start
        steps=0
        current_cost = 0
        current_tick_time=0
        val, obj, cost, tick_time = algo.bt.cost_tick(state,0,0)#tick行为树，obj为所运行的行动

        current_tick_time+=tick_time
        current_cost += cost
        while val !='success' and val !='failure':#运行直到行为树成功或失败
            state = state_transition(state,obj)
            val, obj,cost, tick_time = algo.bt.cost_tick(state,0,0)
            current_cost += cost
            current_tick_time += tick_time
            if(val == 'failure'):
                print("bt fails at step",steps)
                error = True
                break
            steps+=1
            if(steps>=500):#至多运行500步
                break
        if not goal <= state:#错误解，目标条件不在执行后状态满足
            #print ("wrong solution",steps)
            failure_count+=1
            error = True
        else:#正确解，满足目标条件
            #print ("right solution",steps)
            success_count+=1
            total_steps_num.append(steps)
        if error:
            print_action_data_table(goal, start, list(actions))
            algo.print_solution()
            break


        algo.clear()
        total_action_num.append(len(actions))
        total_state_num.append(len(states))
        total_cost.append(current_cost)
        total_tick.append(current_tick_time)

    print("success:",success_count,"failure:",failure_count)#算法成功和失败次数
    print("Total Tree Size: mean=",np.mean(total_tree_size), "std=",np.std(total_tree_size, ddof=1))#1000次测试树大小
    print("Total Steps Num: mean=",np.mean(total_steps_num),"std=",np.std(total_steps_num,ddof=1))
    print("Average Number of States:",np.mean(total_state_num))#1000次问题的平均状态数
    print("Average Number of Actions",np.mean(total_action_num))#1000次问题的平均行动数
    print("Planning Time Total:",planning_time_total,planning_time_total/1000.0)
    print("Average Number of Ticks", np.mean(total_tick),"std=",np.std(total_tick,ddof=1))
    print("Average Cost of Execution:", np.mean(total_cost),"std=",np.std(total_cost,ddof=1))
    # print(total_steps_num) 第21个
    if bt_algo_opt:
        print("============= End OptBT Test ==============")
    else:
        print("============= End XiaoCai BT Test ==============")

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



def BTTest(bt_algo_opt=True,seed=1,literals_num=10,depth=10,iters=10,total_count=1000):

    if bt_algo_opt:
        print("============= OptBT Test ==============")
    else:
        print("============= XiaoCai BT Test ==============")
    random.seed(seed)
    # 设置生成规划问题集的超参数：文字数、解深度、迭代次数
    literals_num=literals_num
    depth = depth
    iters= iters
    total_tree_size = []
    total_action_num = []
    total_state_num = []
    total_steps_num=[]
    total_cost=[]
    total_tick=[]
    #fail_count=0
    #danger_count=0
    success_count =0
    failure_count = 0
    planning_time_total = 0.0

    error = False

    # 实验1000次
    for count in range (total_count):

        action_num = 1

        # 生成一个规划问题，包括随机的状态和行动，以及目标状态
        states = []
        actions = []
        start = generate_random_state(literals_num)
        state = copy.deepcopy(start)
        states.append(state)
        #print (state)
        for k in range(10):
            for i in range (0,depth):
                a = Action()
                a.generate_from_state(state,literals_num)
                a.cost = random.randint(1, 100)
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
        state = copy.deepcopy(start)
        for i in range (0,iters):
            a = Action()
            a.generate_from_state(state,literals_num)
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

        if bt_algo_opt:
            # if count==874:
            #     algo = OptBTExpAlgorithm(verbose=False)
            # else:
            algo = OptBTExpAlgorithm(verbose=False)
        else:
            algo = BTExpAlgorithm(verbose=False)
        algo.clear()

        #algo = Weakalgorithm()
        start_time = time.time()
        if count ==  0 : #874:
            print_action_data_table(goal, start, list(actions))
        # print_action_data_table(goal, start, list(actions))
        if algo.run_algorithm_test(start, goal, actions):#运行算法，规划后行为树为algo.bt
            total_tree_size.append( algo.bt.count_size()-1)
            # if count==0:
            #     algo.print_solution()
            # algo.print_solution()  # 打印行为树
        else:
            print ("error")
        end_time = time.time()
        planning_time_total += (end_time-start_time)

        #开始从初始状态运行行为树，测试
        state=start
        steps=0
        current_cost = 0
        current_tick_time=0
        val, obj, cost, tick_time = algo.bt.cost_tick(state,0,0)#tick行为树，obj为所运行的行动

        current_tick_time+=tick_time
        current_cost += cost
        while val !='success' and val !='failure':#运行直到行为树成功或失败
            state = state_transition(state,obj)
            val, obj,cost, tick_time = algo.bt.cost_tick(state,0,0)
            current_cost += cost
            current_tick_time += tick_time
            if(val == 'failure'):
                print("bt fails at step",steps)
                error = True
                break
            steps+=1
            if(steps>=500):#至多运行500步
                break
        if not goal <= state:#错误解，目标条件不在执行后状态满足
            #print ("wrong solution",steps)
            failure_count+=1
            error = True
        else:#正确解，满足目标条件
            #print ("right solution",steps)
            success_count+=1
            total_steps_num.append(steps)
        if error:
            print_action_data_table(goal, start, list(actions))
            algo.print_solution()
            break


        algo.clear()
        total_action_num.append(len(actions))
        total_state_num.append(len(states))
        total_cost.append(current_cost)
        total_tick.append(current_tick_time)

    print("success:",success_count,"failure:",failure_count)#算法成功和失败次数
    print("Total Tree Size: mean=",np.mean(total_tree_size), "std=",np.std(total_tree_size, ddof=1))#1000次测试树大小
    print("Total Steps Num: mean=",np.mean(total_steps_num),"std=",np.std(total_steps_num,ddof=1))
    print("Average Number of States:",np.mean(total_state_num))#1000次问题的平均状态数
    print("Average Number of Actions",np.mean(total_action_num))#1000次问题的平均行动数
    print("Planning Time Total:",planning_time_total,planning_time_total/1000.0)
    print("Average Number of Ticks", np.mean(total_tick),"std=",np.std(total_tick,ddof=1))
    print("Average Cost of Execution:", np.mean(total_cost),"std=",np.std(total_cost,ddof=1))
    # print(total_steps_num) 第21个
    if bt_algo_opt:
        print("============= End OptBT Test ==============")
    else:
        print("============= End XiaoCai BT Test ==============")

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


def get_act_start_goal(seed=1,literals_num=10,depth=10,iters=10,total_count=1000):
        act_list=[]
        start_list=[]
        goal_list=[]

        for count in range(total_count):
            # 生成一个规划问题，包括随机的状态和行动，以及目标状态
            action_num=1
            states = []
            actions = []
            start = generate_random_state(literals_num)
            state = copy.deepcopy(start)
            states.append(state)
            # print (state)
            for k in range(int(iters/5)):
                state = copy.deepcopy(start)
                for i in range(0, depth):
                    a = Action()
                    a.generate_from_state(state, literals_num)
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
            state = copy.deepcopy(start)
            for i in range(0, int(iters/5)):
                a = Action()
                a.generate_from_state(state, literals_num)
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
            # print("action:",len(actions))
        return act_list, start_list, goal_list


def BTTest_act_start_goal(bt_algo_opt,act_list,start_list,goal_list):

    if bt_algo_opt:
        print("============= OptBT Test ==============")
    else:
        print("============= XiaoCai BT Test ==============")

    # 设置生成规划问题集的超参数：文字数、解深度、迭代次数

    total_tree_size = []
    total_action_num = []
    total_state_num = []
    total_steps_num=[]
    total_cost=[]
    total_tick=[]
    #fail_count=0
    #danger_count=0
    success_count =0
    failure_count = 0
    planning_time_total = 0.0

    error = False

    # 实验1000次
    for count, (actions, start, goal) in enumerate(zip(act_list, start_list, goal_list)):


        states=[]
        # 生成一个规划问题，包括随机的状态和行动，以及目标状态
        state = copy.deepcopy(start)
        states.append(state)

        # 选择测试本文算法btalgorithm，或对比算法weakalgorithm

        if bt_algo_opt:
            # if count==874:
            #     algo = OptBTExpAlgorithm(verbose=False)
            # else:
            algo = OptBTExpAlgorithm(verbose=False)
        else:
            algo = BTExpAlgorithm(verbose=False)
        algo.clear()

        #algo = Weakalgorithm()
        start_time = time.time()
        if count ==  0 : #874:
            print_action_data_table(goal, start, list(actions))
        # print_action_data_table(goal, start, list(actions))
        if algo.run_algorithm_test(start, goal, actions):#运行算法，规划后行为树为algo.bt
            total_tree_size.append( algo.bt.count_size()-1)
            if count==0:
                algo.print_solution()
            # algo.print_solution()  # 打印行为树
        else:
            print ("error")
        end_time = time.time()
        planning_time_total += (end_time-start_time)

        #开始从初始状态运行行为树，测试
        state=start
        steps=0
        current_cost = 0
        current_tick_time=0
        val, obj, cost, tick_time = algo.bt.cost_tick(state,0,0)#tick行为树，obj为所运行的行动

        current_tick_time+=tick_time
        current_cost += cost
        while val !='success' and val !='failure':#运行直到行为树成功或失败
            state = state_transition(state,obj)
            val, obj,cost, tick_time = algo.bt.cost_tick(state,0,0)
            current_cost += cost
            current_tick_time += tick_time
            if(val == 'failure'):
                print("bt fails at step",steps)
                error = True
                break
            steps+=1
            if(steps>=500):#至多运行500步
                break
        if not goal <= state:#错误解，目标条件不在执行后状态满足
            #print ("wrong solution",steps)
            failure_count+=1
            error = True
        else:#正确解，满足目标条件
            #print ("right solution",steps)
            success_count+=1
            total_steps_num.append(steps)
        if error:
            print_action_data_table(goal, start, list(actions))
            algo.print_solution()
            break


        algo.clear()
        total_action_num.append(len(actions))
        total_state_num.append(len(states))
        total_cost.append(current_cost)
        total_tick.append(current_tick_time)

    print("success:",success_count,"failure:",failure_count)#算法成功和失败次数
    print("Total Tree Size: mean=",np.mean(total_tree_size), "std=",np.std(total_tree_size, ddof=1))#1000次测试树大小
    print("Total Steps Num: mean=",np.mean(total_steps_num),"std=",np.std(total_steps_num,ddof=1))
    print("Average Number of States:",np.mean(total_state_num))#1000次问题的平均状态数
    print("Average Number of Actions",np.mean(total_action_num))#1000次问题的平均行动数
    print("Planning Time Total:",planning_time_total,planning_time_total/1000.0)
    print("Average Number of Ticks", np.mean(total_tick),"std=",np.std(total_tick,ddof=1))
    print("Average Cost of Execution:", np.mean(total_cost),"std=",np.std(total_cost,ddof=1))
    # print(total_steps_num) 第21个
    if bt_algo_opt:
        print("============= End OptBT Test ==============")
    else:
        print("============= End XiaoCai BT Test ==============")

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