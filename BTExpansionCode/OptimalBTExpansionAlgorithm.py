import copy
import random
from BehaviorTree import Leaf,ControlBT
import re


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
    for str in c:
        if 'At' in str:
            if not have_at:
                have_at = True
            else:
                return True
    return False


#本文所提出的完备规划算法
class OptBTExpAlgorithm:
    def __init__(self,verbose=False):
        self.bt = None
        self.nodes=[]
        self.traversed=[]
        self.mounted=[]
        self.conditions=[]
        self.conditions_index=[]
        self.verbose=verbose
        self.goal=None
        self.bt_merge = True

    def clear(self):
        self.bt = None
        self.nodes = []
        self.traversed = [] #存cond
        self.expanded = [] #存整个
        self.conditions = []
        self.conditions_index = []

    #运行规划算法，从初始状态、目标状态和可用行动，计算行为树self.bt
    # def run_algorithm(self,goal,actions,scene):
    def run_algorithm_selTree(self, start, goal, actions):
        # self.scene = scene

        self.goal = goal

        if self.verbose:
            print("\n算法开始！")


        bt = ControlBT(type='cond')
        # 初始行为树只包含目标条件
        gc_node = Leaf(type='cond', content=goal, mincost=0) # 为了统一，都成对出现
        ga_node = Leaf(type='act', content=None, mincost=0)
        subtree = ControlBT(type='?')
        subtree.add_child([copy.deepcopy(gc_node)])  # 子树首先保留所扩展结
        bt.add_child([subtree])

        # self.conditions.append(goal)
        cond_anc_pair = CondActPair(cond_leaf=gc_node,act_leaf=ga_node)
        self.nodes.append(copy.deepcopy(cond_anc_pair)) # the set of explored but unexpanded conditions
        self.traversed = [goal] # the set of expanded conditions

        while len(self.nodes)!=0:

            #  Find the condition for the shortest cost path
            pair_node = None
            min_cost = float ('inf')
            index= -1
            for i,cond_anc_pair in enumerate(self.nodes):

                ########### 剪枝操作
                # cond_tmp = cond_anc_pair.cond_leaf.content
                # valid = True
                # for pn in self.expanded:  # 剪枝操作
                #     if isinstance(pn.act_leaf.content,Action):
                #         if pn.act_leaf.content.name==cond_anc_pair.act_leaf.content.name and cond_tmp <= pn.cond_leaf.content:
                #             valid = False
                #             break
                # if not valid:
                #     continue
                ########### 剪枝操作

                if cond_anc_pair.cond_leaf.mincost < min_cost:
                    min_cost = cond_anc_pair.cond_leaf.mincost
                    pair_node = copy.deepcopy(cond_anc_pair)
                    index = i

            if self.verbose:
                print("选择扩展条件结点：",pair_node.cond_leaf.content)
            # Update self.nodes and self.traversed
            self.nodes.pop(index) #  the set of explored but unexpanded conditions. self.nodes.remove(pair_node)
            c = pair_node.cond_leaf.content  # 子树所扩展结点对应的条件（一个文字的set）

            # Mount the action node and extend BT. T = Eapand(T,c,A(c))
            if c!=goal:
                if c!=set():

                    # 挂在上去的时候判断要不要挂载
                    ########### 剪枝操作 发现行不通
                    # valid = True
                    # for pn in self.expanded:  # 剪枝操作
                    #     if isinstance(pn.act_leaf.content,Action):
                    #         if pn.act_leaf.content.name==pair_node.act_leaf.content.name and c <= pn.cond_leaf.content:
                    #             valid = False
                    #             break
                    # if valid:
                    ########### 剪枝操作
                    sequence_structure = ControlBT(type='>')
                    sequence_structure.add_child(
                        [copy.deepcopy(pair_node.cond_leaf), copy.deepcopy(pair_node.act_leaf)])
                    subtree.add_child([copy.deepcopy(sequence_structure)])  # subtree 是回不断变化的，它的父亲是self.bt
                    self.expanded.append(copy.deepcopy(pair_node))
                    # 增加实时条件判断，满足条件就不再扩展
                    # if c <= self.scene.state["condition_set"]:
                    # if c <= start:
                    #     # 要不要继续扩展完全
                    #     # self.merge_adjacent_conditions_stack()
                    #     # self.merge_adjacent_conditions_stack_old()
                    #     # self.merge_adjacent_conditions()
                    #     return True

                    if c <= start:
                        if self.bt_merge:
                            bt = self.merge_adjacent_conditions_stack(bt)
                        return bt,min_cost
                else:
                    subtree.add_child([copy.deepcopy(pair_node.act_leaf)])


                if self.verbose:
                    print("完成扩展 a_node= %s,对应的新条件 c_attr= %s,mincost=%d" \
                          % (cond_anc_pair.act_leaf.content.name, cond_anc_pair.cond_leaf.content,
                             cond_anc_pair.cond_leaf.mincost))

            if self.verbose:
                print("遍历所有动作, 寻找符合条件的动作")
            # 遍历所有动作, 寻找符合条件的动作
            current_mincost = pair_node.cond_leaf.mincost # 当前的最短路径是多少

            traversed_current=[]

            for i in range(0, len(actions)):

                # if "MoveTo(WaterTable)" in actions[i].name:
                #     print(actions[i].name,"cost=",actions[i].cost)


                if not c & ((actions[i].pre | actions[i].add) - actions[i].del_set) <= set()  :
                    if (c - actions[i].del_set) == c:
                        if self.verbose:
                            print("———— 满足条件可以扩展")
                        c_attr = (actions[i].pre | c) - actions[i].add

                        # 这样剪枝存在错误性
                        # if conflict(c_attr):
                        #     continue

                        # 剪枝操作,现在的条件是以前扩展过的条件的超集
                        valid = True
                        for j in self.traversed:  # 剪枝操作
                            if j <= c_attr:
                                valid = False
                                if self.verbose:
                                    print("———— --被剪枝")
                                break

                        if valid:
                            c_attr_node = Leaf(type='cond', content=c_attr, mincost=current_mincost + actions[i].cost)
                            a_attr_node = Leaf(type='act', content=actions[i], mincost=current_mincost + actions[i].cost)
                            cond_anc_pair = CondActPair(cond_leaf=c_attr_node, act_leaf=a_attr_node)
                            self.nodes.append(copy.deepcopy(cond_anc_pair))  # condition node list
                            traversed_current.append(c_attr)
                            # self.traversed.append(c_attr) # 重点 the set of expanded conditions
                            # 把符合条件的动作节点都放到列表里
                            if self.verbose:
                                print("———— -- %s 符合条件放入列表,对应的c为 %s" % (actions[i].name,c_attr))
            self.traversed.extend(traversed_current)
        if self.bt_merge:
            bt = self.merge_adjacent_conditions_stack(bt)
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

    def run_algorithm_test(self, start, goal, actions):
        self.bt,mincost = self.run_algorithm_selTree(start, goal, actions)
        return True


    def merge_adjacent_conditions_stack(self,bt_sel):
        # 只针对第一层合并，之后要考虑层层递归合并
        bt = ControlBT(type='cond')
        sbtree = ControlBT(type='?')
        # gc_node = Leaf(type='cond', content=self.goal, mincost=0)  # 为了统一，都成对出现
        # sbtree.add_child([copy.deepcopy(gc_node)])  # 子树首先保留所扩展结
        bt.add_child([sbtree])

        parnode = bt_sel.children[0]
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
                        stack.append(tmp_tree)

                    else:
                        stack.append(child)
                else:
                    stack.append(child)
            else:
                stack.append(child)

        for tree in stack:
            sbtree.add_child([tree])
        bt_sel = bt
        return bt_sel


    def merge_adjacent_conditions_stack_correct_2023(self):
        # 只针对第一层合并，之后要考虑层层递归合并
        bt = ControlBT(type='cond')
        sbtree = ControlBT(type='?')
        # gc_node = Leaf(type='cond', content=self.goal, mincost=0)  # 为了统一，都成对出现
        # sbtree.add_child([copy.deepcopy(gc_node)])  # 子树首先保留所扩展结
        bt.add_child([sbtree])

        parnode = copy.deepcopy(self.bt.children[0])
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

                    # 如果后面的动作和前面的一样,删掉前面的
                    # 应该是两棵子树完全相同的情况，先暂时只判断动作
                    if set1>=set2 or set1<=set2:
                        if isinstance(last_child.children[1], Leaf) and isinstance(child.children[1], Leaf):
                            if last_child.children[1].content.name == child.children[1].content.name:
                                stack.pop()
                                stack.append(child)
                                continue

                    inter = set1 & set2
                    if inter!=set():
                        c1 = set1-set2
                        c2 = set2-set1

                        if c1!=set():
                            seq1 = ControlBT(type='>')
                            c1_node = Leaf(type='cond', content=c1)
                            a1 = copy.deepcopy(last_child.children[1])
                            seq1.add_child(
                                [copy.deepcopy(c1_node), copy.deepcopy(a1)])
                        else:
                            seq1 = copy.deepcopy(last_child.children[1])

                        if c2!=set():
                            seq2 = ControlBT(type='>')
                            c2_node = Leaf(type='cond', content=c2)
                            a2 = copy.deepcopy(child.children[1])
                            seq2.add_child(
                                [copy.deepcopy(c2_node), copy.deepcopy(a2)])
                        else:
                            seq2 = copy.deepcopy(child.children[1])


                        # 如果动作还是一样的
                        # if isinstance(last_child.children[1], Leaf) and isinstance(child.children[1], Leaf) \
                        #     and isinstance(last_child.children[1].content, Action) and isinstance(child.children[1].content, Action)\
                        #     and last_child.children[1].content.name == child.children[1].content.name: # a1=a2
                        #     # 第三次优化合并
                        #     # 将来这些地方都写成递归的
                        #
                        #     if c1!=set() and c2!=set():
                        #         _sel = ControlBT(type='?')
                        #         c1_node = Leaf(type='cond', content=c1)
                        #         c2_node = Leaf(type='cond', content=c2)
                        #         _sel.add_child([copy.deepcopy(c1_node), copy.deepcopy(c2_node)])
                        #         tmp_tree = ControlBT(type='>')
                        #         inter_c = Leaf(type='cond', content=inter)
                        #         tmp_tree.add_child(
                        #             [copy.deepcopy(inter_c), copy.deepcopy(_sel),copy.deepcopy(last_child.children[1])])
                        #     elif c1!=set() and c2==set():
                        #         tmp_tree = ControlBT(type='>')
                        #         # inter_c = Leaf(type='cond', content=inter)
                        #         # c1_node = Leaf(type='cond', content=c1)
                        #         # a1 = copy.deepcopy(last_child.children[1])
                        #         tmp_tree.add_child(
                        #             [copy.deepcopy(last_child.children[0]), copy.deepcopy(last_child.children[1])])
                        #     else:
                        #         tmp_tree = ControlBT(type='>')
                        #         inter_c = Leaf(type='cond', content=inter)
                        #         a1 = copy.deepcopy(last_child.children[1])
                        #         tmp_tree.add_child(
                        #             [copy.deepcopy(inter_c), copy.deepcopy(a1)])
                        #     # 下面这个是以前写错的
                        #     # sel.add_child([copy.deepcopy(c1), copy.deepcopy(c2),copy.deepcopy(last_child.children[1])])
                        # else:
                        sel = ControlBT(type='?')
                        sel.add_child([copy.deepcopy(seq1), copy.deepcopy(seq2)])
                        tmp_tree = ControlBT(type='>')
                        inter_c = Leaf(type='cond', content=inter)
                        tmp_tree.add_child(
                            [copy.deepcopy(inter_c), copy.deepcopy(sel)])

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
        self.bt = copy.deepcopy(bt)

    def merge_adjacent_conditions_stack_old(self):
        # 递归合并
        bt = ControlBT(type='cond')
        sbtree = ControlBT(type='?')
        gc_node = Leaf(type='cond', content=self.goal, mincost=0)  # 为了统一，都成对出现
        sbtree.add_child([copy.deepcopy(gc_node)])  # 子树首先保留所扩展结
        bt.add_child([sbtree])

        parnode = copy.deepcopy(self.bt.children[0])

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

                    if set1>=set2:
                        inter = set1 & set2
                        dif = set1 - set2

                        tmp_sub_seq = ControlBT(type='>')
                        c2 = Leaf(type='cond', content=dif)
                        a1 = copy.deepcopy(last_child.children[1])
                        tmp_sub_seq.add_child(
                            [copy.deepcopy(c2), copy.deepcopy(a1)])

                        tmp_sub_tree_sel = ControlBT(type='?')
                        a2 = copy.deepcopy(child.children[1])
                        tmp_sub_tree_sel.add_child(
                            [copy.deepcopy(tmp_sub_seq), copy.deepcopy(a2)])

                        tmp_tree = ControlBT(type='>')
                        c1 = Leaf(type='cond', content=inter)
                        tmp_tree.add_child(
                            [copy.deepcopy(c1), copy.deepcopy(tmp_sub_tree_sel)])

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
        self.bt = copy.deepcopy(bt)


    def merge_adjacent_conditions(self):
        # bt合并====================================================
        bt = ControlBT(type='cond')
        sbtree = ControlBT(type='?')
        # gc_node = Leaf(type='cond', content=self.goal, mincost=0)  # 为了统一，都成对出现
        # sbtree.add_child([copy.deepcopy(gc_node)])  # 子树首先保留所扩展结
        bt.add_child([sbtree])

        parnode = copy.deepcopy(self.bt.children[0])
        skip_next = False
        for i in range(len(parnode.children) - 1):
            current_child = parnode.children[i]
            next_child = parnode.children[i + 1]

            if isinstance(current_child, ControlBT) and isinstance(next_child, ControlBT) and current_child.type == '>' and next_child.type == '>':

                if not skip_next:
                    # 检查合并的条件，前面一个的条件包含了后面的条件，把包含部分提取出来
                    set1 = current_child.children[0].content
                    set2 = next_child.children[0].content
                    if set1>=set2:
                        inter = set1 & set2
                        dif = set1 - set2


                        tmp_sub_seq = ControlBT(type='>')
                        c2 = Leaf(type='cond', content=dif)
                        a1 = Leaf(type='act', content=current_child.children[1].content)
                        tmp_sub_seq.add_child(
                            [copy.deepcopy(c2), copy.deepcopy(a1)])

                        tmp_sub_tree_sel = ControlBT(type='?')
                        a2 = Leaf(type='act', content=next_child.children[1].content)
                        tmp_sub_tree_sel.add_child(
                            [copy.deepcopy(tmp_sub_seq), copy.deepcopy(a2)])

                        tmp_tree = ControlBT(type='>')
                        c1 = Leaf(type='cond', content=inter)
                        tmp_tree.add_child(
                            [copy.deepcopy(c1), copy.deepcopy(tmp_sub_tree_sel)])

                        sbtree.add_child([tmp_tree])
                        skip_next = True

                elif skip_next:
                    sbtree.add_child([current_child])
            else:
                # 否咋要放进去
                sbtree.add_child([current_child])

            # 还有最后一个孩子还没放进去
            sbtree.add_child([next_child])

        self.bt = copy.deepcopy(bt)
        # bt合并====================================================


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

    def save_ptml_file(self,file_name):
        self.ptml_string = "selector{\n"
        self.dfs_ptml(self.bt.children[0])
        self.ptml_string += '}\n'
        with open(f'./{file_name}.ptml', 'w') as file:
            file.write(self.ptml_string)
        return self.ptml_string
