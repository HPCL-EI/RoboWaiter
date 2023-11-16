
from robowaiter.behavior_tree.obtea.OptimalBTExpansionAlgorithm import Action,OptBTExpAlgorithm,state_transition # 调用最优行为树扩展算法

from robowaiter.behavior_tree.obtea.examples import *


# 封装好的主接口
class BTOptExpInterface:
    def __init__(self, action_list,scene):
        """
        Initialize the BTOptExpansion with a list of actions.
        :param action_list: A list of actions to be used in the behavior tree.
        """
        # self.actions = []
        # for act in action_list:
        #     a = Action(name=act.name)
        #     a.pre=act['pre']
        #     a.add=act['add']
        #     a.del_set= act['del_set']
        #     a.cost = 1
        #     self.actions.append(a)
        self.actions = action_list
        self.has_processed = False

        self.scene = scene

    def process(self, goal):
        """
        Process the input sets and return a string result.
        :param input_set: The set of goal states and the set of initial states.
        :return: A PTML string representing the outcome of the behavior tree.
        """
        self.goal = goal
        self.algo = OptBTExpAlgorithm(verbose=True)
        self.algo.clear()
        self.algo.run_algorithm(self.goal, self.actions,self.scene) # 调用算法得到行为树保存至 algo.bt
        self.ptml_string = self.algo.get_ptml()
        self.has_processed = True
        # algo.print_solution() # print behavior tree

        return self.ptml_string

    # 方法一：查找所有初始状态是否包含当前状态
    def find_all_leaf_states_contain_start(self,start):
        if not self.has_processed:
            raise RuntimeError("The process method must be called before find_all_leaf_states_contain_start!")
        # 返回所有能到达目标状态的初始状态
        state_leafs = self.algo.get_all_state_leafs()
        for state in state_leafs:
            if start >= state:
                return True
        return False

    # 方法二：模拟跑一遍行为树，看 start 能够通过执行一系列动作到达 goal
    def run_bt_from_start(self,goal,start):
        if not self.has_processed:
            raise RuntimeError("The process method must be called before run_bt_from_start!")
        # 检查是否能到达目标
        right_bt = True
        state = start
        steps = 0
        val, obj = self.algo.bt.tick(state)
        while val != 'success' and val != 'failure':
            state = state_transition(state, obj)
            val, obj = self.algo.bt.tick(state)
            if (val == 'failure'):
                # print("bt fails at step", steps)
                right_bt = False
            steps += 1
        if not goal <= state:
            # print("wrong solution", steps)
            right_bt = False
        else:
            pass
            # print("right solution", steps)
        return right_bt




if __name__ == '__main__' :

    # todo: Example Cafe
    # todo: Define goal, start, actions
    actions=[
        Action(name='PutDown(Table,Coffee)', pre={'Holding(Coffee)','At(Robot,Table)'}, add={'At(Table,Coffee)','NotHolding'}, del_set={'Holding(Coffee)'}, cost=1),
        Action(name='PutDown(Table,VacuumCup)', pre={'Holding(VacuumCup)','At(Robot,Table)'}, add={'At(Table,VacuumCup)','NotHolding'}, del_set={'Holding(VacuumCup)'}, cost=1),

        Action(name='PickUp(Coffee)', pre={'NotHolding','At(Robot,Coffee)'}, add={'Holding(Coffee)'}, del_set={'NotHolding'}, cost=1),

        Action(name='MoveTo(Table)', pre={'Available(Table)'}, add={'At(Robot,Table)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Coffee)','At(Robot,CoffeeMachine)'}, cost=1),
        Action(name='MoveTo(Coffee)', pre={'Available(Coffee)'}, add={'At(Robot,Coffee)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Table)','At(Robot,CoffeeMachine)'}, cost=1),
        Action(name='MoveTo(CoffeeMachine)', pre={'Available(CoffeeMachine)'}, add={'At(Robot,CoffeeMachine)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Coffee)','At(Robot,Table)'}, cost=1),

        Action(name='OpCoffeeMachine', pre={'At(Robot,CoffeeMachine)','NotHolding'}, add={'Available(Coffee)','At(Robot,Coffee)'}, del_set=set(), cost=1),
    ]
    algo = BTOptExpInterface(actions)


    goal = {'At(Table,Coffee)'}
    ptml_string = algo.process(goal)
    print(ptml_string)

    file_name = "sub_task"
    with open(f'./{file_name}.ptml', 'w') as file:
        file.write(ptml_string)


    # 判断初始状态能否到达目标状态
    start = {'At(Robot,Bar)', 'Holding(VacuumCup)', 'Available(Table)', 'Available(CoffeeMachine)','Available(FrontDesk)'}
    # 方法一：算法返回所有可能的初始状态，在里面看看有没有对应的初始状态
    right_bt = algo.find_all_leaf_states_contain_start(start)
    if not right_bt:
        print("ERROR1: The current state cannot reach the goal state!")
    else:
        print("Right1: The current state can reach the goal state!")
    # 方法二：预先跑一边行为树，看能否到达目标状态
    right_bt2 = algo.run_bt_from_start(goal,start)
    if not right_bt2:
        print("ERROR2: The current state cannot reach the goal state!")
    else:
        print("Right2: The current state can reach the goal state!")
