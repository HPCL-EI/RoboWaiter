import copy
import random
from robowaiter.behavior_tree.obtea.BehaviorTree import Leaf,ControlBT



class CondActPair:
    def __init__(self, cond_leaf,act_leaf):
        self.cond_leaf = cond_leaf
        self.act_leaf = act_leaf

#定义行动类，行动包括前提、增加和删除影响
class Action:
    def __init__(self,name='anonymous action',pre=set(),add=set(),del_set=set(),cost=1):
        self.pre=copy.deepcopy(pre)
        self.add=copy.deepcopy(add)
        self.del_set=copy.deepcopy(del_set)
        self.name=name
        self.cost=cost

    def __str__(self):
        return self.name
    # 从状态随机生成一个行动
    def generate_from_state(self,state,num):
        for i in range(0,num):
            if i in state:
                if random.random() >0.5:
                    self.pre.add(i)
                    if random.random() >0.5:
                        self.del_set.add(i)
                    continue
            if random.random() > 0.5:
                self.add.add(i)
                continue
            if random.random() >0.5:
                self.del_set.add(i)
    def print_action(self):
        print (self.pre)
        print(self.add)
        print(self.del_set)

#生成随机状态
def generate_random_state(num):
    result = set()
    for i in range(0,num):
        if random.random()>0.5:
            result.add(i)
    return result
#从状态和行动生成后继状态
def state_transition(state,action):
    if not action.pre <= state:
        print ('error: action not applicable')
        return state
    new_state=(state | action.add) - action.del_set
    return new_state


def conflict(c):
    have_at = False
    have_holding = False
    for str in c:
        if 'At' in str:
            if not have_at:
                have_at = True
            else:
                return True

        if 'Holding' in str:
            if not have_holding:
                have_holding = True
            else:
                return True
    return False

import heapq
#本文所提出的完备规划算法
class OptBTExpAlgorithm:
    def __init__(self,verbose=False,lit_act_dic=None):
        self.bt = None
        self.nodes=[]
        self.traversed=[]
        self.mounted=[]
        self.conditions=[]
        self.conditions_index=[]
        self.verbose=verbose
        self.goal=None
        self.bt_merge = True
        self.lit_act_dic = lit_act_dic

    def clear(self):
        self.bt = None
        self.nodes = []
        self.traversed = [] #存cond
        self.expanded = [] #存整个
        self.conditions = []
        self.conditions_index = []
        self.traversed_state_num=0
        self.fot_times = 0
        self.expand_conds=0
        self.tree_size=0
        self.bt_without_merge = None
        self.subtree_count=1

    #运行规划算法，从初始状态、目标状态和可用行动，计算行为树self.bt
    # def run_algorithm(self,goal,actions,scene):
    #运行规划算法，从初始状态、目标状态和可用行动，计算行为树self.bt
    # def run_algorithm(self,goal,actions,scene):
    def run_algorithm_selTree(self, start, goal, actions,merge_time=99999999):


        self.traversed_state_num=0

        self.goal = goal
        if self.verbose:
            print("\n算法开始！")
        bt = ControlBT(type='cond')
        # 初始行为树只包含目标条件
        gc_node = Leaf(type='cond', content=goal, mincost=0) # 为了统一，都成对出现
        ga_node = Leaf(type='act', content=None, mincost=0)
        subtree = ControlBT(type='?')
        subtree.add_child([gc_node])  # 子树首先保留所扩展结
        self.expand_conds+=1
        bt.add_child([subtree])
        cond_anc_pair = CondActPair(cond_leaf=gc_node,act_leaf=ga_node)

        heapq.heappush(self.nodes, cond_anc_pair)
        self.expanded.append(goal)
        self.traversed_state_num += 1

        self.traversed = [goal] # the set of expanded conditions
        min_cost = float('inf')

        # if goal <= start:
        #     self.bt_without_merge = bt
        #     return bt, 0

        while len(self.nodes)!=0:

            self.fot_times+=1

            #  Find the condition for the shortest cost path
            # ======================== Next Goal ============================ #
            min_cost = float ('inf')
            pair_node = heapq.heappop(self.nodes)

            if self.verbose:
                print("选择扩展条件结点：",pair_node.cond_leaf.content)
            # Update self.nodes and self.traversed
            c = pair_node.cond_leaf.content  # 子树所扩展结点对应的条件（一个文字的set）
            # Mount the action node and extend BT. T = Eapand(T,c,A(c))



            if c!=goal:
                if c!=set():
                    sequence_structure = ControlBT(type='>')
                    sequence_structure.add_child(
                        [pair_node.cond_leaf, pair_node.act_leaf])
                    subtree.add_child([copy.deepcopy(sequence_structure)])  # subtree 是回不断变化的，它的父亲是self.bt
                    # self.expanded.append(copy.deepcopy(pair_node))
                    # self.expanded.append(pair_node.cond_leaf.content)
                    #
                    # if c <= start:
                    #     if self.bt_merge:
                    #         # bt = self.merge_adjacent_conditions_stack(bt)
                    #         bt = self.merge_adjacent_conditions_stack_time(bt,merge_time=merge_time)
                    #     return bt, min_cost
                else:
                    subtree.add_child([copy.deepcopy(pair_node.act_leaf)])
                self.expand_conds += 1
                self.expanded.append(c)
                if c <= start:
                    self.tree_size = self.bfs_cal_tree_size_subtree(bt)
                    self.bt_without_merge = bt
                    if self.bt_merge:
                        # bt = self.merge_adjacent_conditions_stack(bt)
                        bt = self.merge_adjacent_conditions_stack_time(bt,merge_time=merge_time)
                    return bt, min_cost



                if self.verbose:
                    print("完成扩展 a_node= %s,对应的新条件 c_attr= %s,mincost=%d" \
                          % (cond_anc_pair.act_leaf.content.name, cond_anc_pair.cond_leaf.content,
                             cond_anc_pair.cond_leaf.mincost))

            if self.verbose:
                print("遍历所有动作, 寻找符合条件的动作")
            # 遍历所有动作, 寻找符合条件的动作
            current_mincost = pair_node.cond_leaf.mincost # 当前的最短路径是多少
            # ======================== End Next Goal ============================ #

            # ====================== Action Trasvers ============================ #
            traversed_current = []

            # act_tmp_set = set()
            # for lit in c:
            #     act_tmp_set |= self.lit_act_dic[lit]

            # for i in act_tmp_set:
            for i in range(0, len(actions)):

                # if c=={'RobotNear(Chips)', 'Holding(Nothing)'} and actions[i].name=='Clean(Chairs)0':
                #     xx=1
                if not c & ((actions[i].pre | actions[i].add) - actions[i].del_set) <= set()  :
                    if (c - actions[i].del_set) == c:
                        if self.verbose:
                            print("———— 满足条件可以扩展")
                        c_attr = (actions[i].pre | c) - actions[i].add

                        if conflict(c_attr):
                            if self.verbose:
                                print("———— 冲突：动作 %s， 条件 %s"% (actions[i].name,c_attr))
                            continue

                        # 剪枝操作,现在的条件是以前扩展过的条件的超集
                        valid = True

                        for j in self.expanded:
                            if j <= c_attr:
                                valid = False
                                break

                        # tmp_heap = list(self.nodes)
                        # # tmp_heap = copy.deepcopy(self.nodes)
                        # while tmp_heap:  # 剪枝操作 self.expanded?
                        #     cond_anc_pair = heapq.heappop(tmp_heap)
                        #     j = cond_anc_pair.cond_leaf.content
                        #     if j <= c_attr:
                        #         if cond_anc_pair.cond_leaf.mincost < current_mincost + actions[i].cost:
                        #             valid = False
                        #             break


                        if valid:
                            # c_attr_string = "".join(sorted(list(c_attr)))
                            c_attr_node = Leaf(type='cond', content=c_attr, mincost=current_mincost + actions[i].cost)
                            a_attr_node = Leaf(type='act', content=actions[i], mincost=current_mincost + actions[i].cost)
                            cond_anc_pair = CondActPair(cond_leaf=c_attr_node, act_leaf=a_attr_node)
                            # heapq.heappush(self.nodes, copy.deepcopy(cond_anc_pair))
                            heapq.heappush(self.nodes, cond_anc_pair)


                            self.traversed_state_num+=1
                            traversed_current.append(c_attr)
                            # 把符合条件的动作节点都放到列表里
                            if self.verbose:
                                print("———— -- %s 符合条件放入列表,对应的c为 %s" % (actions[i].name,c_attr))

            # print(len(traversed_current))
            self.traversed.extend(traversed_current)
            # ====================== End Action Trasvers ============================ #
        # self.tree_size = self.bfs_cal_tree_size_subtree(bt)
        self.bt_without_merge = bt
        if self.bt_merge:
            # bt = self.merge_adjacent_conditions_stack(bt)
            bt = self.merge_adjacent_conditions_stack_time(bt,merge_time=merge_time)
        if self.verbose:
            print("算法结束！\n")
        return bt,min_cost

    def run_algorithm(self, start, goal, actions):
        self.bt = ControlBT(type='cond')
        subtree = ControlBT(type='?')

        subtree_with_costs_ls=[]

        if len(goal) > 1:
            for g in goal:
                bt_sel_tree,mincost = self.run_algorithm_selTree(start, g, actions)
                subtree_with_costs_ls.append((bt_sel_tree,mincost))
            # 要排个序再一次add
            # subtree.add_child([copy.deepcopy(bt_sel_tree.children[0])])
            # self.bt.add_child([subtree])
            sorted_trees = sorted(subtree_with_costs_ls, key=lambda x: x[1])
            for tree,cost in sorted_trees:
                subtree.add_child([copy.deepcopy(tree.children[0])])
            self.bt.add_child([subtree])
        else:
            self.bt,mincost = self.run_algorithm_selTree(start, goal[0], actions)
        return True



    def merge_adjacent_conditions_stack_time(self,bt_sel,merge_time=9999999):

        merge_time = min(merge_time,500)

        # 只针对第一层合并，之后要考虑层层递归合并
        bt = ControlBT(type='cond')
        sbtree = ControlBT(type='?')
        # gc_node = Leaf(type='cond', content=self.goal, mincost=0)  # 为了统一，都成对出现
        # sbtree.add_child([copy.deepcopy(gc_node)])  # 子树首先保留所扩展结
        bt.add_child([sbtree])

        parnode = bt_sel.children[0]
        stack=[]
        time_stack=[]
        for child in parnode.children:
            if isinstance(child, ControlBT) and child.type == '>':
                if stack==[]:
                    stack.append(child)
                    time_stack.append(0)
                    continue
                # 检查合并的条件，前面一个的条件包含了后面的条件，把包含部分提取出来
                last_child = stack[-1]
                last_time = time_stack[-1]



                if last_time<merge_time and isinstance(last_child, ControlBT) and last_child.type == '>':
                    set1 = last_child.children[0].content
                    set2 = child.children[0].content
                    inter = set1 & set2

                    # print("merge time:", last_time,set1,set2)

                    if inter!=set():
                        c1 = set1-set2
                        c2 = set2-set1
                        inter_node = Leaf(type='cond', content=inter)
                        c1_node = Leaf(type='cond', content=c1)
                        c2_node = Leaf(type='cond', content=c2)
                        a1_node = last_child.children[1]
                        a2_node = child.children[1]


                        # set1<=set2,此时set2对应的动作永远不会执行
                        if (c1==set() and isinstance(last_child.children[1], Leaf) and isinstance(child.children[1], Leaf) \
                               and isinstance(last_child.children[1].content, Action) and isinstance(child.children[1].content, Action)):
                            continue

                        # 再写一个特殊情况处理，三个结点动作last 遇到 两个结点 且动作相同
                        if len(last_child.children)==3 and \
                            isinstance(last_child.children[2], Leaf) and isinstance(child.children[1], Leaf) \
                                and isinstance(last_child.children[2].content, Action) and isinstance( child.children[1].content, Action) \
                                and last_child.children[2].content.name == child.children[1].content.name \
                                and c1==set() and c2!=set():
                                    last_child.children[1].add_child([c2_node])
                                    continue
                        elif len(last_child.children)==3:
                            stack.append(child)
                            time_stack.append(0)
                            continue

                        # 判断动作相不相同
                        if isinstance(last_child.children[1], Leaf) and isinstance(child.children[1], Leaf) \
                            and isinstance(last_child.children[1].content, Action) and isinstance(child.children[1].content, Action) \
                                and last_child.children[1].content.name == child.children[1].content.name:

                            if c2==set():
                                tmp_tree = ControlBT(type='>')
                                tmp_tree.add_child(
                                    [inter_node, a1_node])
                            else:
                                _sel = ControlBT(type='?')
                                _sel.add_child([c1_node, c2_node])
                                tmp_tree = ControlBT(type='>')
                                tmp_tree.add_child(
                                    [inter_node, _sel,a1_node])
                        else:
                            if c1 == set():
                                seq1 = last_child.children[1]
                            else:
                                seq1 = ControlBT(type='>')
                                seq1.add_child([c1_node, a1_node])

                            if c2 == set():
                                seq2 = child.children[1]
                            else:
                                seq2 = ControlBT(type='>')
                                seq2.add_child([c2_node, a2_node])
                            sel = ControlBT(type='?')
                            sel.add_child([seq1, seq2])
                            tmp_tree = ControlBT(type='>')
                            tmp_tree.add_child(
                                [inter_node,sel])

                        stack.pop()
                        time_stack.pop()
                        stack.append(tmp_tree)
                        time_stack.append(last_time+1)

                    else:
                        stack.append(child)
                        time_stack.append(0)
                else:
                    stack.append(child)
                    time_stack.append(0)
            else:
                stack.append(child)
                time_stack.append(0)

        for tree in stack:
            sbtree.add_child([tree])
        bt_sel = bt
        return bt_sel



    def merge_adjacent_conditions_stack(self,bt_sel):
        # 只针对第一层合并，之后要考虑层层递归合并
        bt = ControlBT(type='cond')
        sbtree = ControlBT(type='?')
        # gc_node = Leaf(type='cond', content=self.goal, mincost=0)  # 为了统一，都成对出现
        # sbtree.add_child([copy.deepcopy(gc_node)])  # 子树首先保留所扩展结
        bt.add_child([sbtree])

        parnode = copy.deepcopy(bt_sel.children[0])
        stack=[]
        for child in parnode.children:
            if isinstance(child, ControlBT) and child.type == '>':
                if stack==[]:
                    stack.append(child)
                    continue
                # 检查合并的条件，前面一个的条件包含了后面的条件，把包含部分提取出来
                last_child = stack[-1]
                if isinstance(last_child, ControlBT) and last_child.type == '>':
                    set1 = last_child.children[0].content
                    set2 = child.children[0].content
                    inter = set1 & set2
                    if inter!=set():
                        c1 = set1-set2
                        c2 = set2-set1
                        inter_node = Leaf(type='cond', content=inter)
                        c1_node = Leaf(type='cond', content=c1)
                        c2_node = Leaf(type='cond', content=c2)
                        a1_node = copy.deepcopy(last_child.children[1])
                        a2_node = copy.deepcopy(child.children[1])


                        # set1<=set2,此时set2对应的动作永远不会执行
                        if (c1==set() and isinstance(last_child.children[1], Leaf) and isinstance(child.children[1], Leaf) \
                               and isinstance(last_child.children[1].content, Action) and isinstance(child.children[1].content, Action)):
                            continue

                        # 再写一个特殊情况处理，三个结点动作last 遇到 两个结点 且动作相同
                        if len(last_child.children)==3 and \
                            isinstance(last_child.children[2], Leaf) and isinstance(child.children[1], Leaf) \
                                and isinstance(last_child.children[2].content, Action) and isinstance( child.children[1].content, Action) \
                                and last_child.children[2].content.name == child.children[1].content.name \
                                and c1==set() and c2!=set():
                                    last_child.children[1].add_child([copy.deepcopy(c2_node)])
                                    continue
                        elif len(last_child.children)==3:
                            stack.append(child)
                            continue

                        # 判断动作相不相同
                        if isinstance(last_child.children[1], Leaf) and isinstance(child.children[1], Leaf) \
                            and isinstance(last_child.children[1].content, Action) and isinstance(child.children[1].content, Action) \
                                and last_child.children[1].content.name == child.children[1].content.name:

                            if c2==set():
                                tmp_tree = ControlBT(type='>')
                                tmp_tree.add_child(
                                    [copy.deepcopy(inter_node), copy.deepcopy(a1_node)])
                            else:
                                _sel = ControlBT(type='?')
                                _sel.add_child([copy.deepcopy(c1_node), copy.deepcopy(c2_node)])
                                tmp_tree = ControlBT(type='>')
                                tmp_tree.add_child(
                                    [copy.deepcopy(inter_node), copy.deepcopy(_sel),copy.deepcopy(a1_node)])
                        else:
                            if c1 == set():
                                seq1 = copy.deepcopy(last_child.children[1])
                            else:
                                seq1 = ControlBT(type='>')
                                seq1.add_child([copy.deepcopy(c1_node), copy.deepcopy(a1_node)])

                            if c2 == set():
                                seq2 = copy.deepcopy(child.children[1])
                            else:
                                seq2 = ControlBT(type='>')
                                seq2.add_child([copy.deepcopy(c2_node), copy.deepcopy(a2_node)])
                            sel = ControlBT(type='?')
                            sel.add_child([copy.deepcopy(seq1), copy.deepcopy(seq2)])
                            tmp_tree = ControlBT(type='>')
                            tmp_tree.add_child(
                                [copy.deepcopy(inter_node), copy.deepcopy(sel)])

                        stack.pop()
                        stack.append(tmp_tree)

                    else:
                        stack.append(child)
                else:
                    stack.append(child)
            else:
                stack.append(child)

        for tree in stack:
            sbtree.add_child([tree])
        bt_sel = copy.deepcopy(bt)
        return bt_sel



    def print_solution(self):
        print("========= BT ==========")  # 树的bfs遍历
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
        print("========= BT ==========\n")

    # 返回所有能到达目标状态的初始状态
    def get_all_state_leafs(self):
        state_leafs=[]

        nodes_ls = []
        nodes_ls.append(self.bt)
        while len(nodes_ls) != 0:
            parnode = nodes_ls[0]
            for child in parnode.children:
                if isinstance(child, Leaf):
                    if child.type == "cond":
                        state_leafs.append(child.content)
                elif isinstance(child, ControlBT):
                    nodes_ls.append(child)
            nodes_ls.pop(0)

        return state_leafs


    # 树的dfs
    def dfs_ptml(self,parnode,is_root=False):
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
                    if '(' not in child.content.name:
                        self.ptml_string += 'act ' + child.content.name + "()\n"
                    else:
                        self.ptml_string += 'act ' + child.content.name + "\n"
            elif isinstance(child, ControlBT):
                if child.type == '?':
                    self.ptml_string += "selector{\n"
                    self.dfs_ptml(parnode=child)
                elif child.type == '>':
                    self.ptml_string += "sequence{\n"
                    self.dfs_ptml( parnode=child)
                self.ptml_string += '}\n'


    def get_ptml(self):
        self.ptml_string = "selector{\n"
        self.dfs_ptml(self.bt.children[0],is_root=True)
        self.ptml_string += '}\n'
        return self.ptml_string


    def save_ptml_file(self,file_name):
        self.ptml_string = "selector{\n"
        self.dfs_ptml(self.bt.children[0])
        self.ptml_string += '}\n'
        with open(f'./{file_name}.ptml', 'w') as file:
            file.write(self.ptml_string)
        return self.ptml_string
