import random
import numpy as np
import copy
import time
from BehaviorTree import Leaf,ControlBT # 行为结点类：叶子结点和非叶子节点
from OptimalBTExpansionAlgorithm_single_goal import Action,OptBTExpAlgorithm # 调用最优行为树扩展算法
from OptimalBTExpansionAlgorithm_single_goal import OptBTExpAlgorithm
from OptimalBTExpansionAlgorithm_single_goal import generate_random_state,state_transition
from tools import print_action_data_table,BTTest,BTTest_act_start_goal,get_act_start_goal
from Examples import MoveBtoB_num,MoveBtoB,Cond2BelongsToCond3 # 导入三个例子
from Examples import *
# from utils.bt.draw import render_dot_tree
# from utils.bt.load import load_bt_from_ptml,find_node_by_name,print_tree_from_root
import os
output_path = os.path.join(os.path.dirname(__file__), "outputs")

if __name__ == '__main__' :

    # todo: Example Cafe
    # todo: Define goal, start, actions
    # actions=[]
    # a = Action(name="Move(b,ab)")
    # a.pre={'Free(ab)','WayClear'}
    # a.add={'At(b,ab)'} #{3}
    # a.del_set= {'Free(ab)','At(b,pb)'}
    # a.cost = 1
    # actions.append(a)
    # ……………………
    # start = {'Free(ab)','Free(as)','At(b,pb)','At(s,ps)'}
    # goal= {'At(b,ab)'}

    # Put(P,O)  pre={'Holding(O)','At(Robot,P)'}, add={'At(P,O)','NotHolding'}, del_set={'Holding(O)'}
    # Grasp(O)  pre={'NotHolding','At(Robot,O)'}, add={'Holding(O)'}, del_set={'NotHolding'}
    # MoveTo(P) pre={'Available(P)'}, add={'At(Robot,P)'}, del_set={'At(……)'}

    # actions=[
    #     Action(name='PutDown(Table,Coffee)', pre={'Holding(Coffee)','At(Robot,Table)'}, add={'At(Table,Coffee)','NotHolding'}, del_set={'Holding(Coffee)'}, cost=1),
    #     Action(name='PutDown(Table,VacuumCup)', pre={'Holding(VacuumCup)','At(Robot,Table)'}, add={'At(Table,VacuumCup)','NotHolding'}, del_set={'Holding(VacuumCup)'}, cost=1),
    #
    #     Action(name='PickUp(Coffee)', pre={'NotHolding','At(Robot,Coffee)'}, add={'Holding(Coffee)'}, del_set={'NotHolding'}, cost=2),
    #
    #     Action(name='MoveTo(Table)', pre={'Available(Table)'}, add={'At(Robot,Table)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Coffee)','At(Robot,CoffeeMachine)'}, cost=5),
    #     Action(name='MoveTo(Coffee)', pre={'Available(Coffee)'}, add={'At(Robot,Coffee)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Table)','At(Robot,CoffeeMachine)'}, cost=6),
    #     Action(name='MoveTo(CoffeeMachine)', pre={'Available(CoffeeMachine)'}, add={'At(Robot,CoffeeMachine)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Coffee)','At(Robot,Table)'}, cost=7),
    #
    #     Action(name='OpCoffeeMachine', pre={'At(Robot,CoffeeMachine)','NotHolding'}, add={'Available(Coffee)','At(Robot,Coffee)'}, del_set=set(), cost=10),
    # ]
    #
    # start = {'At(Robot,Bar)','Holding(VacuumCup)','Available(Table)','Available(CoffeeMachine)','Available(FrontDesk)'}
    # goal = {'At(Table,Coffee)'}
    #
    ptml_file_name = "SoftdrinkCost" #MakeCoffee


    # 从已定义好的例子中直接导入
    goal, start, actions = Cond2BelongsToCond3()  # Examples里的例子: MoveBtoB_num,MoveBtoB,Cond2BelongsToCond3,SoftdrinkCost
    # goal, start, actions = Test()
    # goal, start, actions = MakeCoffeeCost()
    # print_action_data_table(goal,start,actions) # 打印所有变量


    # todo: 运行算法得到行为树为 algo.bt
    algo = OptBTExpAlgorithm(verbose=True)
    algo.clear()
    algo.run_algorithm(start, goal, actions)
    # algo.print_solution() # 打印行为树
    # todo: 输出 MakeCoffee.ptml
    print("=========== PTML ============")
    ptml_string = algo.save_ptml_file(ptml_file_name)
    print(ptml_string)
    print("========= End PTML ==========\n")



    # todo: 执行行为树查看结果
    print("=========== Run BT ============")
    state = start
    steps = 0
    val, obj = algo.bt.tick(state)
    while val != 'success' and val != 'failure':
        state = state_transition(state, obj)
        print (obj.name)
        val, obj = algo.bt.tick(state)
        if (val == 'failure'):
            print("bt fails at step", steps)
        steps += 1
    if not goal <= state:
        print ("wrong solution",steps)
    else:
        print ("right solution",steps)
    #algo.bt.print_nodes()
    print ("The number of nodes in BT:",algo.bt.count_size()-1)
    algo.clear()
    print("============ End Run BT ===========\n")
    '''

    '''
    # 新增测试 cost
    # algo = OptBTExpAlgorithm(verbose=False)
    # algo.clear()
    # algo.run_algorithm(start, goal, actions)
    # # algo.print_solution() # 打印行为树
    # print("=========== Run OptBT ============")
    # state = start
    # steps = 0
    # cost_tatol = 0
    # val, obj,cost,ticks = algo.bt.cost_tick(state,0,0)
    # cost_tatol+=cost
    # while val != 'success' and val != 'failure':
    #     state = state_transition(state, obj)
    #     print (obj.name)
    #     val, obj,cost,ticks = algo.bt.cost_tick(state,0,ticks)
    #     cost_tatol += cost
    #     if (val == 'failure'):
    #         print("bt fails at step", steps)
    #     steps += 1
    # if not goal <= state:
    #     print ("wrong solution steps",steps)
    # else:
    #     print ("right solution steps",steps)
    # algo.clear()
    # print("OptBT cost:", cost_tatol)
    # print("OptBT ticks:", ticks)
    # print("============ End Run OptBT ===========\n")

    
    algo2 = OptBTExpAlgorithm(verbose=False)
    algo2.clear()
    algo2.run_algorithm(start, goal, actions)
    # algo2.print_solution() # 打印行为树
    print("=========== Run XiaoCaiBT ============")
    state = start
    steps = 0
    cost_tatol2 = 0
    val, obj,cost,ticks = algo2.bt.cost_tick(state,0,0)
    cost_tatol2+=cost
    while val != 'success' and val != 'failure':
        state = state_transition(state, obj)
        print (obj.name)
        val, obj,cost,ticks = algo2.bt.cost_tick(state,0,ticks)
        cost_tatol2 += cost
        if (val == 'failure'):
            print("bt fails at step", steps)
        steps += 1
    if not goal <= state:
        print ("wrong solution steps",steps)
    else:
        print ("right solution steps",steps)
    algo2.clear()
    print("XiaoCaiBT cost:", cost_tatol2)
    print("XiaoCaiBT ticks:", ticks)
    print("============ End Run XiaoCaiBT ===========\n")



    # todo: 行为树鲁棒性测试，随机生成规划问题
    # # 设置生成规划问题集的超参数：文字数、解深度、迭代次数
    # seed=1
    # literals_num= 3
    # depth = 3
    # iters= 3


    # act_list, start_list, goal_list = get_act_start_goal(seed=seed,literals_num=literals_num,depth=depth,iters=iters,total_count=1)
    # BTTest_act_start_goal(bt_algo_opt=True,act_list=act_list, start_list=start_list, goal_list=goal_list)
    # print("\n")
    # BTTest_act_start_goal(bt_algo_opt=False, act_list=act_list, start_list=start_list, goal_list=goal_list)

    # BTTest(bt_algo_opt=True,seed=seed,literals_num=literals_num,depth=depth,iters=iters)
    # print("\n")
    # 对比
    # BTTest(bt_algo_opt=False,seed=seed,literals_num=literals_num,depth=depth,iters=iters)
