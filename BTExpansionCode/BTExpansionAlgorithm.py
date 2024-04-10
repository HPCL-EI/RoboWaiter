import random
import numpy as np
import copy
import time

from OptimalBTExpansionAlgorithm import ControlBT,Leaf,generate_random_state,Action,state_transition,conflict
import re


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
        self.traversed_state_num=0
        self.fot_times =0
        self.expand_conds = 0
        self.tree_size = 0

    def run_algorithm_selTree(self, start, goal, actions):
        self.traversed_state_num=0
        # 初始行为树只包含目标条件
        bt = ControlBT(type='cond')
        g_node = Leaf(type='cond', content=goal,mincost=0)
        bt.add_child([g_node])
        self.expand_conds +=1
        self.conditions.append(goal)
        self.nodes.append(g_node)  # condition node list
        self.traversed_state_num+=1
        # 尝试在初始状态执行行为树
        val, obj = bt.tick(start)
        canrun = False
        if val == 'success' or val == 'running':
            canrun = True
        # 循环扩展，直到行为树能够在初始状态运行
        while not canrun:

            self.fot_times += 1

            # print("canrun:",canrun)
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
            subtree.add_child([copy.deepcopy(c_node)])  # 子树首先保留所扩展结点 # copy
            c = c_node.content  # 子树所扩展结点对应的条件（一个文字的set）

            if self.verbose:
                print("选择扩展条件结点：",c)

            if c != goal:
                if c <= start:
                    return bt

            act_num = 0

            for i in range(0, len(actions)):  # 选择符合条件的行动，
                # print("have action")

                if c=={'RobotNear(Chips)', 'Holding(Nothing)'} and actions[i].name=='Clean(Chairs)0':
                    xx=1


                if not c & ((actions[i].pre | actions[i].add) - actions[i].del_set) <= set():
                    # print ("pass add")
                    if (c - actions[i].del_set) == c:
                        # print("pass delete")
                        c_attr = (actions[i].pre | c) - actions[i].add
                        valid = True

                        # if "PickUp(ADMilk)0" in actions[i].name:
                        #     xx = 1

                        if conflict(c_attr):
                            continue

                        for j in self.traversed:  # 剪枝操作
                            if j <= c_attr:
                                valid = False
                                break

                        if valid:
                            # print("pass prune")
                            # 构建行动的顺序结构
                            sequence_structure = ControlBT(type='>')
                            c_attr_node = Leaf(type='cond', content=c_attr, mincost=0)
                            a_node = Leaf(type='act', content=actions[i], mincost=0)
                            sequence_structure.add_child([c_attr_node, a_node])
                            # 将顺序结构添加到子树
                            subtree.add_child([sequence_structure])
                            self.nodes.append(c_attr_node)
                            self.expand_conds += 1
                            act_num+=1
                            # self.traversed_state_num+=1
                            if self.verbose:
                                print("完成扩展 a_node= %s,对应的新条件 c_attr= %s" \
                                      % (actions[i].name, c_attr))

            # print(act_num)
            self.traversed_state_num += act_num
            # 将原条件结点c_node替换为扩展后子树subtree
            parent_of_c = c_node.parent
            parent_of_c.children[0] = subtree
            # 记录已扩展条件
            self.traversed.append(c)
            # 尝试在初始状态运行行为树
            val, obj = bt.tick(start)
            canrun = False
            if val == 'success' or val == 'running':
                canrun = True
            self.tree_size = self.bfs_cal_tree_size_subtree(bt)
        return bt


    def run_algorithm_test(self, start, goal, actions):
        self.bt = self.run_algorithm_selTree(start, goal, actions)
        return True



    def run_algorithm(self, start, goal, actions):
        # goal_ls = goal.replace(" ", "")
        # goal_ls = goal_ls.split("|")
        self.bt = ControlBT(type='cond')
        subtree = ControlBT(type='?')
        if len(goal) > 1:
            for g in goal:
                # print("goal",g)
                bt_sel_tree = self.run_algorithm_selTree(start, g, actions)
                # print("bt_sel_tree.children",bt_sel_tree.children)
                # print(bt_sel_tree.children[0])
                # subtree.add_child([copy.deepcopy(bt_sel_tree.children[0])])
                subtree.add_child([bt_sel_tree.children[0]])
            self.bt.add_child([subtree])
        else:
            self.bt = self.run_algorithm_selTree(start, goal[0], actions)
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


    def dfs_ptml_many_act(self, parnode, is_root=False):
        for child in parnode.children:
            if isinstance(child, Leaf):
                if child.type == 'cond':

                    if is_root and len(child.content) > 1:
                        # 把多个 cond 串起来
                        self.ptml_string += "sequence{\n"
                        self.ptml_string += "cond "
                        c_set_str = '\n cond '.join(map(str, child.content)) + "\n"
                        self.ptml_string += c_set_str
                        self.ptml_string += '}\n'
                    else:
                        self.ptml_string += "cond "
                        c_set_str = '\n cond '.join(map(str, child.content)) + "\n"
                        self.ptml_string += c_set_str

                elif child.type == 'act':

                    child.content.name = re.sub(r'\d+', '', child.content.name)

                    if '(' not in child.content.name:
                        self.ptml_string += 'act ' + child.content.name + "()\n"
                    else:
                        self.ptml_string += 'act ' + child.content.name + "\n"
            elif isinstance(child, ControlBT):
                if child.type == '?':
                    self.ptml_string += "selector{\n"
                    self.dfs_ptml_many_act(parnode=child)
                elif child.type == '>':
                    self.ptml_string += "sequence{\n"
                    self.dfs_ptml_many_act(parnode=child)
                self.ptml_string += '}\n'

    def get_ptml_many_act(self):
        self.ptml_string = "selector{\n"
        self.dfs_ptml_many_act(self.bt.children[0],is_root=True)
        self.ptml_string += '}\n'
        return self.ptml_string


    def bfs_cal_tree_size(self):
        from collections import deque
        queue = deque([self.bt.children[0]])

        if isinstance(self.bt.children[0], Leaf):
            # print("扩展后的结点数=0")
            return 0

        count = 0
        while queue:
            current_node = queue.popleft()
            count += 1
            for child in current_node.children:
                if isinstance(child, Leaf):
                    count += 1
                else:
                    queue.append(child)
        return count

    def bfs_cal_tree_size_subtree(self,bt):
        from collections import deque
        queue = deque([bt.children[0]])

        if isinstance(bt.children[0], Leaf):
            # print("扩展后的结点数=0")
            return 0

        count = 0
        while queue:
            current_node = queue.popleft()
            count += 1
            for child in current_node.children:
                if isinstance(child, Leaf):
                    count += 1
                else:
                    queue.append(child)
        return count


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
