import random
import numpy as np
import copy
import time

from OptimalBTExpansionAlgorithm import ControlBT,Leaf,generate_random_state,Action,state_transition,conflict

# 本文所提出的完备规划算法
class BTExpAlgorithm:
    def __init__(self,verbose=False):
        self.bt = None
        self.nodes = []
        self.traversed = []
        self.conditions = []
        self.conditions_index = []
        self.verbose = verbose
        # print (self.conditions_list[0])

    def clear(self):
        self.bt = None
        self.nodes = []
        self.traversed = []
        self.conditions = []
        self.conditions_index = []

    # 运行规划算法，从初始状态、目标状态和可用行动，计算行为树self.bt
    def run_algorithm(self, start, goal, actions):
        # 初始行为树只包含目标条件
        self.bt = ControlBT(type='cond')
        g_node = Leaf(type='cond', content=goal)
        self.bt.add_child([g_node])

        self.conditions.append(goal)
        self.nodes.append(g_node)  # condition node list
        # 尝试在初始状态执行行为树
        val, obj = self.bt.tick(start)
        canrun = False
        if val == 'success' or val == 'running':
            canrun = True
        # 循环扩展，直到行为树能够在初始状态运行
        while not canrun:
            index = -1
            for i in range(0, len(self.nodes)):
                if self.nodes[i].content in self.traversed:
                    continue
                else:
                    c_node = self.nodes[i]
                    index = i
                    break
            if index == -1:  # 树中结点扩展完毕，仍无法运行行为树，返回失败
                print('Failure')
                return False
            # 根据所选择条件结点扩展子树
            subtree = ControlBT(type='?')
            subtree.add_child([copy.deepcopy(c_node)])  # 子树首先保留所扩展结点
            c = c_node.content  # 子树所扩展结点对应的条件（一个文字的set）

            for i in range(0, len(actions)):  # 选择符合条件的行动，
                # print("have action")
                if not c & ((actions[i].pre | actions[i].add) - actions[i].del_set) <= set():
                    # print ("pass add")
                    if (c - actions[i].del_set) == c:
                        # print("pass delete")
                        c_attr = (actions[i].pre | c) - actions[i].add
                        valid = True

                        # 这样剪枝存在错误性
                        # if conflict(c_attr):
                        #     continue

                        for j in self.traversed:  # 剪枝操作
                            if j <= c_attr:
                                valid = False
                                break
                        if valid:
                            # print("pass prune")
                            # 构建行动的顺序结构
                            sequence_structure = ControlBT(type='>')
                            c_attr_node = Leaf(type='cond', content=c_attr)
                            a_node = Leaf(type='act', content=actions[i])
                            sequence_structure.add_child([c_attr_node, a_node])
                            # 将顺序结构添加到子树
                            subtree.add_child([sequence_structure])

                            self.nodes.append(c_attr_node)
            # 将原条件结点c_node替换为扩展后子树subtree
            parent_of_c = c_node.parent
            parent_of_c.children[0] = subtree
            # 记录已扩展条件
            self.traversed.append(c)
            # 尝试在初始状态运行行为树
            val, obj = self.bt.tick(start)
            canrun = False
            if val == 'success' or val == 'running':
                canrun = True
        return True

    def print_solution(self):
        print("========= XiaoCaoBT ==========")  # 树的bfs遍历
        nodes_ls = []
        nodes_ls.append(self.bt)
        while len(nodes_ls) != 0:
            parnode = nodes_ls[0]
            print("Parrent:", parnode.type)
            for child in parnode.children:
                if isinstance(child, Leaf):
                    print("---- Leaf:", child.content)
                elif isinstance(child, ControlBT):
                    print("---- ControlBT:", child.type)
                    nodes_ls.append(child)
            print()
            nodes_ls.pop(0)
        print("========= XiaoCaoBT ==========\n")

if __name__ == '__main__':

    bt_algo_opt = False


    # casestudy begin 对应论文的case study，包含三个行动的移动机械臂场景

    actions = []
    a = Action(name='movebtob')
    a.pre = {1, 2}
    a.add = {3}
    a.del_set = {1, 4}
    actions.append(a)
    a = Action(name='moveatob')
    a.pre = {1}
    a.add = {5, 2}
    a.del_set = {1, 6}
    actions.append(a)
    a = Action(name='moveatoa')
    a.pre = {7}
    a.add = {8, 2}
    a.del_set = {7, 6}
    actions.append(a)

    start = {1, 7, 4, 6}
    goal = {3}
    algo = BTExpAlgorithm()
    algo.clear()
    algo.run_algorithm(start, goal, list(actions))
    state = start
    steps = 0
    val, obj = algo.bt.tick(state)
    while val != 'success' and val != 'failure':
        state = state_transition(state, obj)
        print(obj.name)
        val, obj = algo.bt.tick(state)
        if (val == 'failure'):
            print("bt fails at step", steps)
        steps += 1
    if not goal <= state:
        print("wrong solution", steps)
    else:
        print("right solution", steps)
    # algo.bt.print_nodes()
    print(algo.bt.count_size() - 1)
    algo.clear()

# case study end
