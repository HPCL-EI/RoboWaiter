


from utils.bt.load import load_behavior_tree_lib
from OptimalBTExpansionAlgorithm import Action,OptBTExpAlgorithm

import copy
from tabulate import tabulate
import numpy as np
import os

from sympy import symbols, Not, Or, And, to_dnf
from OptimalBTExpansionAlgorithm import Action,OptBTExpAlgorithm
from BTExpansionAlgorithm import BTExpAlgorithm # 调用最优行为树扩展算法
import time
from utils.bt.draw import render_dot_tree
from utils.bt.load import load_bt_from_ptml
root_path = os.path.abspath(
        os.path.join(__file__, "../../..")
    )
def goal_transfer_str(goal):
    goal_dnf = str(to_dnf(goal, simplify=True))
    # print(goal_dnf)
    goal_set = []
    if ('|' in goal or '&' in goal or 'Not' in goal) or not '(' in goal:
        goal_ls = goal_dnf.split("|")
        for g in goal_ls:
            g_set = set()
            g = g.replace(" ", "").replace("(", "").replace(")", "")
            g = g.split("&")
            for literal in g:
                if '_' in literal:
                    first_part, rest = literal.split('_', 1)
                    literal = first_part + '(' + rest
                    # 添加 ')' 到末尾
                    literal += ')'
                    # 替换剩余的 '_' 为 ','
                    literal = literal.replace('_', ',')
                g_set.add(literal)
            goal_set.append(g_set)

    else:
        g_set = set()
        w = goal.split(")")
        g_set.add(w[0] + ")")
        if len(w) > 1:
            for x in w[1:]:
                if x != "":
                    g_set.add(x[1:] + ")")
        goal_set.append(g_set)
    return goal_set

def collect_action_nodes(random):
    multiple_num=2
    action_list = []
    behavior_dict = load_behavior_tree_lib()

    for cls in behavior_dict["act"].values():
        if cls.can_be_expanded:
            print(f"可扩展动作：{cls.__name__}, 存在{len(cls.valid_args)}个有效论域组合")
            if cls.num_args == 0:
                for num in range(multiple_num):
                    info = cls.get_info()
                    action_list.append(Action(name=cls.get_ins_name() + str(num), **info))
            if cls.num_args == 1:
                for num in range(multiple_num):
                    for arg in cls.valid_args:
                        info = cls.get_info(arg)
                        action_list.append(Action(name=cls.get_ins_name(arg) + str(num), **info))
            if cls.num_args > 1:
                for num in range(multiple_num):
                    for args in cls.valid_args:
                        info = cls.get_info(*args)
                        action_list.append(Action(name=cls.get_ins_name(*args) + str(num),**info))

    action_list = sorted(action_list, key=lambda x: x.name)
    for i in range(len(action_list)):
        cost = random.randint(1, 100)
        action_list[i].cost=cost
    return action_list

def collect_action_nodes_old(random):
    action_list = []
    behavior_dict = load_behavior_tree_lib()
    behavior_ls = list()
    # behavior_ls.sort()

    behavior_ls = [cls for cls in behavior_ls]
    behavior_ls =  sorted(behavior_ls, key=lambda x: x.__class__.__name__)

    for cls in behavior_ls:
        if cls.can_be_expanded:
            print(f"可扩展动作：{cls.__name__}, 存在{len(cls.valid_args)}个有效论域组合")
            if cls.num_args == 0:
                for num in range(2):
                    cost = random.randint(1, 100)
                    info = cls.get_info()
                    info.pop('cost', None)
                    action_list.append(Action(name=cls.get_ins_name()+str(num),cost=cost, **info))
            if cls.num_args == 1:
                for num in range(2):
                    for arg in cls.valid_args:
                        cost = random.randint(1, 100)
                        info = cls.get_info(arg)
                        info.pop('cost', None)
                        action_list.append(Action(name=cls.get_ins_name(arg)+str(num),cost=cost, **info))
            if cls.num_args > 1:
                for num in range(2):
                    for args in cls.valid_args:
                        cost = random.randint(1, 100)
                        info = cls.get_info(*args)
                        info.pop('cost', None)
                        action_list.append(Action(name=cls.get_ins_name(*args)+str(num),cost=cost, **info))
    return action_list


def get_start():
    start_robowaiter = {'At(Robot,Bar)', 'Is(AC,Off)',
            'Exist(Yogurt)', 'Exist(BottledDrink)', 'Exist(Softdrink)', 'Exist(ADMilk)',
            'On(Yogurt,Bar)','On(BottledDrink,Bar)','On(ADMilk,Bar)','On(Chips,Bar)',
            'Exist(Milk)', 'On(Softdrink,Table1)', 'On(Softdrink,Table3)',
            'Exist(Chips)', 'Exist(NFCJuice)', 'Exist(Bernachon)', 'Exist(ADMilk)', 'Exist(SpringWater)', 'Exist(MilkDrink)',
            'Exist(ADMilk)','On(ADMilk,Bar)','On(Bernachon,Bar)','On(SpringWater,Bar2)','On(MilkDrink,Bar)',
            'Holding(Nothing)',
            'Exist(VacuumCup)', 'On(VacuumCup,Table2)',
            'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
            'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
    return start_robowaiter


def print_action_data_table(goal,start,actions):
    data = []
    for a in actions:
        data.append([a.name ,a.pre ,a.add ,a.del_set ,a.cost])
    data.append(["Goal" ,goal ," " ,"Start" ,start])
    print(tabulate(data, headers=["Name", "Pre", "Add" ,"Del" ,"Cost"], tablefmt="fancy_grid"))  # grid plain simple github fancy_grid


def state_transition(state,action):
    if not action.pre <= state:
        print ('error: action not applicable')
        return state
    new_state=(state | action.add) - action.del_set
    return new_state


def BTTest(bt_algo_opt,goal_states,action_list,start_robowaiter):

    if bt_algo_opt:
        print("============= OptBT Test ==============")
    else:
        print("============= XiaoCai BT Test ==============")

    total_tree_size = []
    total_action_num = []
    total_state_num = []
    total_steps_num = []
    total_cost = []
    total_tick = []
    success_count = 0
    failure_count = 0
    planning_time_total = 0.0
    states=[] ####？？？
    actions = copy.deepcopy(action_list)
    start = copy.deepcopy(start_robowaiter)

    error=False

    for count, goal_str in enumerate(goal_states):

        goal = copy.deepcopy(goal_transfer_str(goal_str))
        print("count:", count, "goal:", goal)


        if bt_algo_opt:
            # if count==874:
            #     algo = OptBTExpAlgorithm(verbose=False)
            # else:
            algo = OptBTExpAlgorithm(verbose=False)
        else:
            algo = BTExpAlgorithm(verbose=False)
        algo.clear()

        # algo = Weakalgorithm()
        start_time = time.time()
        # if count ==  11 : #874:
        #     print_action_data_table(goal, start, list(actions))
        # print_action_data_table(goal, start, list(actions))
        if algo.run_algorithm(start, goal, actions):  # 运行算法，规划后行为树为algo.bt
            total_tree_size.append(algo.bt.count_size() - 1)
            # if count==10:
            #     algo.print_solution()
            # algo.print_solution()  # 打印行为树

            # 画出行为树
            # if count == 11:
            #     ptml_string = algo.get_ptml_many_act()
            #     file_name = "sub_task"
            #     file_path = f'./{file_name}.ptml'
            #     with open(file_path, 'w') as file:
            #         file.write(ptml_string)
            #     ptml_path = os.path.join(root_path, 'BTExpansionCode/EXP/sub_task.ptml')
            #     behavior_lib_path = os.path.join(root_path, 'BTExpansionCode/EXP/behavior_lib')
            #     bt = load_bt_from_ptml(None, ptml_path, behavior_lib_path)
            #     if bt_algo_opt:
            #         render_dot_tree(bt.root, target_directory="", name="expanded_bt_obt", png_only=False)
            #     else:
            #         render_dot_tree(bt.root, target_directory="", name="expanded_bt_xiaocai", png_only=False)

        else:
            print("error")
        end_time = time.time()
        planning_time_total += (end_time - start_time)

        # 开始从初始状态运行行为树，测试
        state = start
        steps = 0
        current_cost = 0
        current_tick_time = 0
        val, obj, cost, tick_time = algo.bt.cost_tick(state, 0, 0)  # tick行为树，obj为所运行的行动

        current_tick_time += tick_time
        current_cost += cost
        while val != 'success' and val != 'failure':  # 运行直到行为树成功或失败
            state = state_transition(state, obj)
            val, obj, cost, tick_time = algo.bt.cost_tick(state, 0, 0)
            current_cost += cost
            current_tick_time += tick_time
            if (val == 'failure'):
                print("bt fails at step", steps)
                error = True
                break
            steps += 1
            if (steps >= 500):  # 至多运行500步
                break
        if not goal[0] <= state:  # 错误解，目标条件不在执行后状态满足
            # print ("wrong solution",steps)
            failure_count += 1
            error = True
        else:  # 正确解，满足目标条件
            # print ("right solution",steps)
            success_count += 1
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

    print("success:", success_count, "failure:", failure_count)  # 算法成功和失败次数
    print("Total Tree Size: mean=", np.mean(total_tree_size), "std=", np.std(total_tree_size, ddof=1))  # 1000次测试树大小
    print("Total Steps Num: mean=", np.mean(total_steps_num), "std=", np.std(total_steps_num, ddof=1))
    print("Average Number of States:", np.mean(total_state_num))  # 1000次问题的平均状态数
    print("Average Number of Actions", np.mean(total_action_num))  # 1000次问题的平均行动数
    print("Planning Time Total:", planning_time_total, planning_time_total / 1000.0)
    print("Average Number of Ticks", np.mean(total_tick), "std=", np.std(total_tick, ddof=1))
    print("Average Cost of Execution:", np.mean(total_cost), "std=", np.std(total_cost, ddof=1))


