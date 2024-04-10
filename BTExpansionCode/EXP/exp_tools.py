


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
from EXP.behavior_lib._base.Behavior import Bahavior
from EXP.behavior_lib.cond import Holding

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
                literal=literal.replace('~', 'Not ')
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

def collect_action_nodes_multiple_num(random,multiple_num=1):

    behavior_dict = load_behavior_tree_lib()
    action_list = []

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
                # for num in range(multiple_num):
                for num in range(multiple_num):
                    for args in cls.valid_args:
                        # xx += 1
                        info = cls.get_info(*args)
                        action_list.append(Action(name=cls.get_ins_name(*args) + str(num),**info))

    action_list = sorted(action_list, key=lambda x: x.name)
    for i in range(len(action_list)):
        cost = random.randint(1, 100)
        action_list[i].cost=cost

    return action_list



def collect_action_nodes(random,multiple_num=1,iters_times=1):

    behavior_dict = load_behavior_tree_lib()

    iter_action_ls=[]
    for iter in range(iters_times):
        action_list = []

        for cls in behavior_dict["act"].values():
            if cls.can_be_expanded:
                print(f"可扩展动作：{cls.__name__}, 存在{len(cls.valid_args)}个有效论域组合")
                if cls.num_args == 0:
                    mr = random.randint(1, multiple_num+1)
                    for num in range(mr):
                        info = cls.get_info()
                        action_list.append(Action(name=cls.get_ins_name() + str(num), **info))
                if cls.num_args == 1:
                    mr = random.randint(1, multiple_num+1)
                    for num in range(mr):
                        for arg in cls.valid_args:
                            info = cls.get_info(arg)
                            action_list.append(Action(name=cls.get_ins_name(arg) + str(num), **info))
                if cls.num_args > 1:
                    # for num in range(multiple_num):
                    mr = random.randint(1, multiple_num+1)
                    for num in range(mr):
                        for args in cls.valid_args:
                            # xx += 1
                            info = cls.get_info(*args)
                            action_list.append(Action(name=cls.get_ins_name(*args) + str(num),**info))
                        # if xx%2==0 or xx%3==0:
                        #     break


        action_list = sorted(action_list, key=lambda x: x.name)
        for i in range(len(action_list)):
            cost = random.randint(1, 100)
            action_list[i].cost=cost
        iter_action_ls.append(action_list)
        print("len(action_list):",len(action_list))
    if iters_times==1:
        return action_list
    else:
        return iter_action_ls



def collect_action_nodes_old(random):
    action_list = []
    behavior_dict = load_behavior_tree_lib()
    behavior_ls = list()    # behavior_ls.sort()

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


def collect_cond_nodes():
    cond_list = []
    behavior_dict = load_behavior_tree_lib()
    num=0
    vaild_num=1
    vaild_num = f"{vaild_num:.2e}"
    for cls in behavior_dict["cond"].values():
        if cls.can_be_expanded:
            print(f"可扩展条件：{cls.__name__}, 存在{len(cls.valid_args)}个有效论域组合")
            if cls.num_params == 0:
                num+=1
                # vaild_num*=2
            if cls.num_params == 1:
                num += len(cls.valid_args)
                # if cls.__name__=="Holding" or cls.__name__=='RobotNear':
                #     vaild_num *= (len(cls.valid_args))
                # else:
                #     vaild_num *= (2**len(cls.valid_args))
            if cls.num_params > 1:
                cartesian_product_size=1
                for s in cls.valid_args:
                    cartesian_product_size *= len(s)
                num += cartesian_product_size
                # if cls.__name__ == "On":
                    # vaild_num *= (len(cls.valid_args[1])**len(cls.valid_args[0]))
    return num,vaild_num


def get_start():
    # start_robowaiter = {'At(Robot,Bar)', 'Is(AC,Off)',
    #         'Exist(Yogurt)', 'Exist(BottledDrink)', 'Exist(Softdrink)', 'Exist(ADMilk)',
    #         'On(Yogurt,Bar)','On(BottledDrink,Bar)','On(ADMilk,Bar)','On(Chips,Bar)',
    #         'Exist(Milk)', 'On(Softdrink,Table1)', 'On(Softdrink,Table3)',
    #         'Exist(Chips)', 'Exist(NFCJuice)', 'Exist(Bernachon)', 'Exist(ADMilk)', 'Exist(SpringWater)', 'Exist(MilkDrink)',
    #         'Exist(ADMilk)','On(ADMilk,Bar)','On(Bernachon,Bar)','On(SpringWater,Bar2)','On(MilkDrink,Bar)',
    #         'Holding(Nothing)',
    #         'Exist(VacuumCup)', 'On(VacuumCup,Table2)',
    #         'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
    #         'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
    start_robowaiter = {'RobotNear(Bar)',
                        'Not Active(AC)','Not Active(HallLight)','Active(TubeLight)','Not Closed(Curtain)',
                        'Not Exists(Coffee)','Not Exists(Water)','Not Exists(Dessert)',
                        'Holding(Nothing)',
                        'Not IsClean(Table1)', 'Not IsClean(Floor)', 'Not IsClean(Chairs)',
                        'On(Softdrink,Table1)','On(VacuumCup,Table2)',

            # 'On(Yogurt,Bar)','On(BottledDrink,Bar)','On(ADMilk,Bar)','On(Chips,Bar)',
            # 'On(Softdrink,Table1)', 'On(Softdrink,Table3)',
            # 'On(ADMilk,Bar)','On(Bernachon,Bar)','On(SpringWater,Bar2)','On(MilkDrink,Bar)',
            # 'On(VacuumCup,Table2)',
            }

    all_obj_place= Bahavior.all_object | Bahavior.tables_for_placement | Bahavior.tables_for_guiding
    start_robowaiter |= {f'Not RobotNear({place})' for place in all_obj_place if place != 'Bar'}
    start_robowaiter |= {f'Not Holding({obj})' for obj in Bahavior.all_object}
    start_robowaiter |= {f'Exists({obj})' for obj in Bahavior.all_object if obj != 'Coffee' and obj != 'Water' and obj != 'Dessert'}
    # 'Softdrink' 在Table1
    start_robowaiter |= {f'Not On(Softdrink,{place})' for place in Bahavior.all_place if place!="Table1"}
    start_robowaiter |= {f'Not On(VacuumCup,{place})' for place in Bahavior.all_place if place != "Table2"}


    # 默认物品都在 Bar 上
    start_robowaiter |= {f'On({obj},Bar)' for obj in Bahavior.all_object if obj != 'Coffee' and obj != 'Water' and obj != 'Dessert' \
                         and obj != 'Softdrink'  and obj != 'VacuumCup' }
    for place in Bahavior.all_place:
        if place!="Bar":
            start_robowaiter |= {f'Not On({obj},{place})' for obj in Bahavior.all_object}
        # start_robowaiter |= {f'On({obj},{place})' for obj in Bahavior.all_object if
        #                      obj != 'Coffee' and obj != 'Water' and obj != 'Dessert'}

    # 这三样哪里都没有
    make_obj = {"Coffee",'Water','Dessert'}
    for place in Bahavior.all_place:
        start_robowaiter |= {f'Not On({obj},{place})' for obj in make_obj }
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


def BTTest_easy_medium_hard(bt_algo_opt,goal_states,action_list,start_robowaiter):

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
    planning_time_ls=[]
    states=[] ####？？？
    actions = copy.deepcopy(action_list)
    start = copy.deepcopy(start_robowaiter)

    error=False

    total_count = len(goal_states)
    total_cond_tick = []

    for count, goal_str in enumerate(goal_states):

        goal = copy.deepcopy(goal_transfer_str(goal_str))
        # goal = goal_str
        # print("count:", count, "goal:", goal)


        if bt_algo_opt:
            # if count==874:
            #     algo = OptBTExpAlgorithm(verbose=False)
            # else:
            algo = OptBTExpAlgorithm(verbose=False)
        else:
            algo = BTExpAlgorithm(verbose=False)
        algo.clear()

        # algo = Weakalgorithm()

        # if count == 6 : #874:
        #     print_action_data_table(goal, start, list(actions))
        # print_action_data_table(goal, start, list(actions))

        start_time = time.time()
        algo_right = algo.run_algorithm(start, goal, actions)
        end_time = time.time()
        planning_time_ls.append(end_time - start_time)
        planning_time_total += (end_time - start_time)

        # print("xxxx")

        if algo_right:  # 运行算法，规划后行为树为algo.bt
            # total_tree_size.append(algo.bt.count_size() - 1)
            total_tree_size.append(algo.bfs_cal_tree_size())
            # if count==10:
            #     algo.print_solution()
            # algo.print_solution()  # 打印行为树
            # 画出行为树
            # if count == 2:
            # ptml_string = algo.get_ptml_many_act()
            # print(ptml_string)
            # file_name = "sub_task"
            # file_path = f'{file_name}.ptml'
            # with open(file_path, 'w') as file:
            #     file.write(ptml_string)
            # ptml_path = os.path.join(root_path, 'BTExpansionCode/EXP/sub_task.ptml')
            # behavior_lib_path = os.path.join(root_path, 'BTExpansionCode/EXP/behavior_lib')
            # bt = load_bt_from_ptml(None, ptml_path, behavior_lib_path)
            # if bt_algo_opt:
            #     render_dot_tree(bt.root, target_directory="", name="expanded_bt_obt", png_only=False)
            # else:
            #     render_dot_tree(bt.root, target_directory="", name="expanded_bt_xiaocai", png_only=False)
        else:
            print("error")

        # 开始从初始状态运行行为树，测试
        state = start
        steps = 0
        current_cost = 0
        current_tick_time = 0
        current_cond_tick_time=0
        # val, obj, cost, tick_time = algo.bt.cost_tick(state, 0, 0)  # tick行为树，obj为所运行的行动
        val, obj, cost, tick_time, cond_times = algo.bt.cost_tick_cond(state, 0, 0, 0)
        current_cond_tick_time += cond_times
        current_tick_time += tick_time
        current_cost += cost
        while val != 'success' and val != 'failure':  # 运行直到行为树成功或失败
            state = state_transition(state, obj)
            # val, obj, cost, tick_time = algo.bt.cost_tick(state, 0, 0)
            val, obj, cost, tick_time, cond_times = algo.bt.cost_tick_cond(state, 0, 0, 0)
            current_cond_tick_time += cond_times
            current_cost += cost
            current_tick_time += tick_time
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
            if gg<=state:
                error = False
                success_count += 1
                total_steps_num.append(steps)
                break
        if error:
            failure_count += 1
        # if not goal[0] <= state:  # 错误解，目标条件不在执行后状态满足
        #     # print ("wrong solution",steps)
        #     failure_count += 1
        #     error = True
        # else:  # 正确解，满足目标条件
        #     # print ("right solution",steps)
        #     success_count += 1
        #     total_steps_num.append(steps)
        if error:
            # print_action_data_table(goal, start, list(actions))
            # algo.print_solution()
            break

        algo.clear()
        total_action_num.append(len(actions))
        total_state_num.append(len(states))
        total_cost.append(current_cost)
        total_tick.append(current_tick_time)
        total_cond_tick.append(current_cond_tick_time)

    print("success:", success_count, "failure:", failure_count)  # 算法成功和失败次数
    print("*** Total Tree Size: mean=", round(np.mean(total_tree_size),2), "std=", round(np.std(total_tree_size, ddof=1),2))  # 1000次测试树大小
    print("Total Steps Num: mean=", np.mean(total_steps_num), "std=", np.std(total_steps_num, ddof=1))
    print("Average Number of States:", np.mean(total_state_num))  # 1000次问题的平均状态数
    print("Average Number of Actions", np.mean(total_action_num))  # 1000次问题的平均行动数
    print("Planning Time Total:", planning_time_total)
    print("*** Planning Time mean=:",  round(np.mean(planning_time_ls),3), "std=", round(np.std(planning_time_ls),3))
    print("*** Average Number of Ticks", round(np.mean(total_tick),3), "std=", round(np.std(total_tick, ddof=1),3))
    print("*** Average Cost of Execution:", round(np.mean(total_cost),3), "std=", round(np.std(total_cost, ddof=1),3))
    print("*** Cond Ticks:", round(np.mean(total_cond_tick), 3), "std=", round(np.std(total_cond_tick, ddof=1), 3))

    tree_size = [round(np.mean(total_tree_size), 3), round(np.std(total_tree_size, ddof=1), 3)]
    ticks = [round(np.mean(total_tick), 3), round(np.std(total_tick, ddof=1), 3)]
    cond_ticks = [round(np.mean(total_cond_tick), 3)]
    cost = [round(np.mean(total_cost), 3), round(np.std(total_cost, ddof=1), 3)]
    plan_time = [round(np.mean(planning_time_ls), 5), round(np.std(planning_time_ls), 5), round(planning_time_total, 5)]

    tmp_ls=[]
    tmp_ls.extend(tree_size)
    tmp_ls.extend(ticks)
    tmp_ls.extend(cond_ticks)
    tmp_ls.extend(cost)
    tmp_ls.extend(plan_time)
    return tmp_ls




def BTTest_Merge_easy_medium_hard(bt_algo_opt,goal_states,action_list,start_robowaiter,merge_time=99999):

    merge_time = merge_time

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
    planning_time_ls=[]
    states=[] ####？？？
    actions = copy.deepcopy(action_list)
    start = copy.deepcopy(start_robowaiter)

    total_cond_tick = []

    error=False

    total_count = len(goal_states)

    for count, goal_str in enumerate(goal_states):

        goal = copy.deepcopy(goal_transfer_str(goal_str))
        # goal = goal_str
        # print("count:", count, "goal:", goal)


        if bt_algo_opt:
            # if count==874:
            #     algo = OptBTExpAlgorithm(verbose=False)
            # else:
            algo = OptBTExpAlgorithm(verbose=False)
        else:
            algo = BTExpAlgorithm(verbose=False)
        algo.clear()

        # algo = Weakalgorithm()

        # if count == 6 : #874:
        #     print_action_data_table(goal, start, list(actions))
        # print_action_data_table(goal, start, list(actions))

        start_time = time.time()
        # algo_right = algo.run_algorithm(start, goal, actions)
        algo_right = algo.run_algorithm(start, goal, actions, merge_time)
        end_time = time.time()
        planning_time_ls.append(end_time - start_time)
        planning_time_total += (end_time - start_time)

        if algo_right:  # 运行算法，规划后行为树为algo.bt
            # total_tree_size.append(algo.bt.count_size() - 1)
            total_tree_size.append(algo.bfs_cal_tree_size())
            # if count==10:
            #     algo.print_solution()
            # algo.print_solution()  # 打印行为树
            # 画出行为树
            # if count == 2:
            # ptml_string = algo.get_ptml_many_act()
            # # print(ptml_string)
            # file_name = "sub_task"
            # file_path = f'{file_name}.ptml'
            # with open(file_path, 'w') as file:
            #     file.write(ptml_string)
            # ptml_path = os.path.join(root_path, 'BTExpansionCode/EXP/sub_task.ptml')
            # behavior_lib_path = os.path.join(root_path, 'BTExpansionCode/EXP/behavior_lib')
            # bt = load_bt_from_ptml(None, ptml_path, behavior_lib_path)
            # if bt_algo_opt:
            #     render_dot_tree(bt.root, target_directory="", name="expanded_bt_obt", png_only=False)
            # else:
            #     render_dot_tree(bt.root, target_directory="", name="expanded_bt_xiaocai", png_only=False)
        else:
            print("error")

        # 开始从初始状态运行行为树，测试
        state = start
        steps = 0
        current_cost = 0
        current_tick_time = 0
        current_cond_tick_time = 0
        val, obj, cost, tick_time,cond_times = algo.bt.cost_tick_cond(state, 0, 0,0)  # tick行为树，obj为所运行的行动
        # val, obj, cost, tick_time = algo.bt.cost_tick(state, 0, 0)

        current_tick_time += tick_time
        current_cost += cost
        current_cond_tick_time+=cond_times
        while val != 'success' and val != 'failure':  # 运行直到行为树成功或失败
            state = state_transition(state, obj)
            val, obj, cost, tick_time,cond_times = algo.bt.cost_tick_cond(state, 0, 0,0)
            # val, obj, cost, tick_time = algo.bt.cost_tick(state, 0, 0)
            current_cost += cost
            current_tick_time += tick_time
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
            if gg<=state:
                error = False
                success_count += 1
                total_steps_num.append(steps)
                break
        if error:
            failure_count += 1
        # if not goal[0] <= state:  # 错误解，目标条件不在执行后状态满足
        #     # print ("wrong solution",steps)
        #     failure_count += 1
        #     error = True
        # else:  # 正确解，满足目标条件
        #     # print ("right solution",steps)
        #     success_count += 1
        #     total_steps_num.append(steps)
        if error:
            # print_action_data_table(goal, start, list(actions))
            # algo.print_solution()
            break

        algo.clear()
        total_action_num.append(len(actions))
        total_state_num.append(len(states))
        total_cost.append(current_cost)
        total_tick.append(current_tick_time)
        total_cond_tick.append(current_cond_tick_time)

    print("success:", success_count, "failure:", failure_count)  # 算法成功和失败次数
    print("*** Total Tree Size: mean=", round(np.mean(total_tree_size),2), "std=", round(np.std(total_tree_size, ddof=1),2))  # 1000次测试树大小
    print("Total Steps Num: mean=", np.mean(total_steps_num), "std=", np.std(total_steps_num, ddof=1))
    print("Average Number of States:", np.mean(total_state_num))  # 1000次问题的平均状态数
    print("Average Number of Actions", np.mean(total_action_num))  # 1000次问题的平均行动数
    print("Planning Time Total:", planning_time_total)
    print("*** Planning Time mean=:",  round(np.mean(planning_time_ls),3), "std=", round(np.std(planning_time_ls),3))
    print("*** Average Number of Ticks", round(np.mean(total_tick),3), "std=", round(np.std(total_tick, ddof=1),3))
    print("*** Average Number of Cond Ticks", round(np.mean(total_cond_tick), 3), "std=", round(np.std(total_cond_tick, ddof=1), 3))
    print("*** Average Cost of Execution:", round(np.mean(total_cost),3), "std=", round(np.std(total_cost, ddof=1),3))

    tree_size = [round(np.mean(total_tree_size), 3), round(np.std(total_tree_size, ddof=1), 3)]
    ticks = [round(np.mean(total_tick), 3), round(np.std(total_tick, ddof=1), 3)]
    cond_ticks = [round(np.mean(total_cond_tick), 3), round(np.std(total_cond_tick, ddof=1), 3)]
    cost = [round(np.mean(total_cost), 3), round(np.std(total_cost, ddof=1), 3)]
    plan_time = [round(np.mean(planning_time_ls), 5), round(np.std(planning_time_ls), 5), round(planning_time_total, 5)]

    tmp_ls=[]
    tmp_ls.extend(tree_size)
    tmp_ls.extend(ticks)
    tmp_ls.extend(cond_ticks)
    tmp_ls.extend(cost)
    tmp_ls.extend(plan_time)
    return tmp_ls




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
    planning_time_ls=[]
    states=[] ####？？？
    actions = copy.deepcopy(action_list)
    start = copy.deepcopy(start_robowaiter)

    error=False

    total_count = len(goal_states)

    for count, goal_str in enumerate(goal_states):

        goal = copy.deepcopy(goal_transfer_str(goal_str))
        # goal = goal_str
        print("count:", count, "goal:", goal)


        if bt_algo_opt:
            # if count==874:
            #     algo = OptBTExpAlgorithm(verbose=False)
            # else:
            algo = OptBTExpAlgorithm(verbose=True)
        else:
            algo = BTExpAlgorithm(verbose=False)
        algo.clear()

        # algo = Weakalgorithm()

        # if count == 6 : #874:
        #     print_action_data_table(goal, start, list(actions))
        # print_action_data_table(goal, start, list(actions))

        start_time = time.time()
        algo_right = algo.run_algorithm(start, goal, actions)
        end_time = time.time()
        planning_time_ls.append(end_time - start_time)
        planning_time_total += (end_time - start_time)

        if algo_right:  # 运行算法，规划后行为树为algo.bt
            # total_tree_size.append(algo.bt.count_size() - 1)
            total_tree_size.append(algo.bfs_cal_tree_size())
            # if count==10:
            #     algo.print_solution()
            algo.print_solution()  # 打印行为树
            # 画出行为树
            # if count == 2:
            ptml_string = algo.get_ptml_many_act()
            # # print(ptml_string)
            file_name = "sub_task"
            file_path = f'./EXP/{file_name}.ptml'
            with open(file_path, 'w') as file:
                file.write(ptml_string)
            ptml_path = os.path.join(root_path, 'BTExpansionCode/EXP/sub_task.ptml')
            behavior_lib_path = os.path.join(root_path, 'BTExpansionCode/EXP/behavior_lib')
            bt = load_bt_from_ptml(None, ptml_path, behavior_lib_path)
            if bt_algo_opt:
                render_dot_tree(bt.root, target_directory="", name="expanded_bt_obt", png_only=False)
            else:
                render_dot_tree(bt.root, target_directory="", name="expanded_bt_xiaocai", png_only=False)
        else:
            print("error")

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
            # print_action_data_table(goal, start, list(actions))
            # algo.print_solution()
            break

        algo.clear()
        total_action_num.append(len(actions))
        total_state_num.append(len(states))
        total_cost.append(current_cost)
        total_tick.append(current_tick_time)

    print("success:", success_count, "failure:", failure_count)  # 算法成功和失败次数
    print("*** Total Tree Size: mean=", round(np.mean(total_tree_size),2), "std=", round(np.std(total_tree_size, ddof=1),2))  # 1000次测试树大小
    print("Total Steps Num: mean=", np.mean(total_steps_num), "std=", np.std(total_steps_num, ddof=1))
    print("Average Number of States:", np.mean(total_state_num))  # 1000次问题的平均状态数
    print("Average Number of Actions", np.mean(total_action_num))  # 1000次问题的平均行动数
    print("Planning Time Total:", planning_time_total)
    print("*** Planning Time mean=:",  round(np.mean(planning_time_ls),3), "std=", round(np.std(planning_time_ls),3))
    print("*** Average Number of Ticks", round(np.mean(total_tick),3), "std=", round(np.std(total_tick, ddof=1),3))
    print("*** Average Cost of Execution:", round(np.mean(total_cost),3), "std=", round(np.std(total_cost, ddof=1),3))




def BTTest_Merge(bt_algo_opt,goal_states,action_list,start_robowaiter,merge_time=3):

    total_tree_size = []
    total_action_num = []
    total_state_num = []
    total_steps_num = []
    total_cost = []
    total_tick = []
    success_count = 0
    failure_count = 0
    planning_time_total = 0.0
    planning_time_ls=[]
    states=[] ####？？？
    actions = copy.deepcopy(action_list)
    start = copy.deepcopy(start_robowaiter)

    error=False

    total_count = len(goal_states)

    total_time_dic={}


    for count, goal_str in enumerate(goal_states):
        goal = copy.deepcopy(goal_transfer_str(goal_str))

        if bt_algo_opt:
            algo = OptBTExpAlgorithm(verbose=False)
        else:
            algo = BTExpAlgorithm(verbose=False)
        algo.clear()

        start_time = time.time()
        algo_right,time_dic = algo.run_algorithm(start, goal, actions,merge_time)
        end_time = time.time()
        planning_time_ls.append(end_time - start_time)
        planning_time_total += (end_time - start_time)

        if algo_right:  # 运行算法，规划后行为树为algo.bt
            # total_tree_size.append(algo.bt.count_size() - 1)
            total_tree_size.append(algo.bfs_cal_tree_size())
            # if count==10:
            #     algo.print_solution()
            # algo.print_solution()  # 打印行为树
            # 画出行为树
            # if count == 2:
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

    # print("success:", success_count, "failure:", failure_count)  # 算法成功和失败次数
    # print("*** Total Tree Size: mean=", round(np.mean(total_tree_size),2), "std=", round(np.std(total_tree_size, ddof=1),2))  # 1000次测试树大小
    # print("Total Steps Num: mean=", np.mean(total_steps_num), "std=", np.std(total_steps_num, ddof=1))
    # print("Average Number of States:", np.mean(total_state_num))  # 1000次问题的平均状态数
    # print("Average Number of Actions", np.mean(total_action_num))  # 1000次问题的平均行动数
    # print("Planning Time Total:", planning_time_total)
    # print("*** Planning Time mean=:",  round(np.mean(planning_time_ls),3), "std=", round(np.std(planning_time_ls),3))
    # print("*** Average Number of Ticks", round(np.mean(total_tick),3), "std=", round(np.std(total_tick, ddof=1),3))
    # print("*** Average Cost of Execution:", round(np.mean(total_cost),3), "std=", round(np.std(total_cost, ddof=1),3))

    tree_size=[round(np.mean(total_tree_size),2), round(np.std(total_tree_size, ddof=1),2)]
    plan_time=[round(np.mean(planning_time_ls),3), round(np.std(planning_time_ls),3),round(planning_time_total,3)]
    ticks=[round(np.mean(total_tick),3),round(np.std(total_tick, ddof=1),3)]
    cost=[round(np.mean(total_cost),3),round(np.std(total_cost, ddof=1),3)]
    return tree_size,plan_time,ticks,cost


def get_act_start_goal(seed=1, literals_num=10, depth=10, iters=10, total_count=1000):

    max_copy_time = 5

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
        state_set = {i for i in range(literals_num)}
        state = copy.deepcopy(start)
        states.append(state)

        # for i in range(0, depth):
        #     a = Action()
        #     a.generate_from_state_local(state, literals_num_set)
        #     a.cost = random.randint(1, 100)
        #     if not a in actions:
        #         a.name = "a" + str(action_num)
        #         action_num += 1
        #         actions.append(a)
        #     state = state_transition(state, a)
        #     if state in states:
        #         pass
        #     else:
        #         states.append(state)
        #         # print(state)
        # goal = states[-1]

        # k_act_total = int(iters*np.random.uniform()/depth)
        # if k_act_total<1:
        #     k_act_total = random.randint(1, 5)
        # for k in range(k_act_total):
        for i in range(0, depth):
            start_time = time.time()
            a = Action()
            a.generate_from_state_local(state, literals_num_set)
            a.cost = random.randint(1, 100)
            if not a in actions:
                a.name = "a" + str(action_num)
                action_num += 1
                actions.append(a)
            copy_times = random.randint(1, max_copy_time)
            # copy_times = 0
            for ct in range(copy_times):
                ca = copy.deepcopy(a)
                ca.cost = random.randint(1, 100)
                if not ca in actions:
                    ca.name = "a" + str(action_num)
                    action_num += 1
                    actions.append(ca)
            end_time = time.time()
            total_time_dic["start_to_goal"] += end_time - start_time
            state = state_transition(state, a)
            if state in states:
                pass
            else:
                states.append(state)

            if not goal <= states[-1]:
                a = Action()
                pre_num = random.randint(0, len(states[-1]))
                a.pre = set(random.sample(states[-1], pre_num))
                a.add = goal - states[-1]
                def_set = state_set - goal
                def_num = random.randint(0, len(def_set))
                a.del_set = set(random.sample(def_set, def_num))
                a.cost = random.randint(1, 100)
                a.name = "a" + str(action_num)
                action_num += 1
                actions.append(a)

                # copy_times = random.randint(1, 5)
                copy_times = 0
                for ct in range(copy_times):
                    ca = copy.deepcopy(a)
                    ca.cost = random.randint(1, 100)
                    if not ca in actions:
                        ca.name = "a" + str(action_num)
                        action_num += 1
                        actions.append(ca)


        state = copy.deepcopy(start)
        last_act_total=iters+2*depth-len(actions)
        if last_act_total<0:
            last_act_total = 0
        for i in range(last_act_total):
            a = Action()
            start_time = time.time()
            a.generate_from_state_local(state, literals_num_set)
            end_time = time.time()
            total_time_dic["random_act"] += end_time - start_time

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



