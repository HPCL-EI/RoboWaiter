import copy
import random
from opt_bt_expansion.BehaviorTree import Leaf,ControlBT

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

    def clear(self):
        self.bt = None
        self.nodes = []
        self.traversed = []
        self.conditions = []
        self.conditions_index = []

    #运行规划算法，从初始状态、目标状态和可用行动，计算行为树self.bt
    def run_algorithm(self,goal,actions):
        if self.verbose:
            print("\n算法开始！")


        self.bt = ControlBT(type='cond')
        # 初始行为树只包含目标条件
        gc_node = Leaf(type='cond', content=goal,mincost=0) # 为了统一，都成对出现
        ga_node = Leaf(type='act', content=None, mincost=0)
        subtree = ControlBT(type='?')
        subtree.add_child([copy.deepcopy(gc_node)])  # 子树首先保留所扩展结
        self.bt.add_child([subtree])

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
                if cond_anc_pair.cond_leaf.mincost < min_cost:
                    min_cost = cond_anc_pair.cond_leaf.mincost
                    pair_node = copy.deepcopy(cond_anc_pair)
                    index = i
                    break

            if self.verbose:
                print("选择扩展条件结点：",pair_node.cond_leaf.content)
            # Update self.nodes and self.traversed
            self.nodes.pop(index) #  the set of explored but unexpanded conditions. self.nodes.remove(pair_node)
            c = pair_node.cond_leaf.content  # 子树所扩展结点对应的条件（一个文字的set）

            # Mount the action node and extend BT. T = Eapand(T,c,A(c))
            if c!=goal:
                sequence_structure = ControlBT(type='>')
                sequence_structure.add_child(
                    [copy.deepcopy(pair_node.cond_leaf), copy.deepcopy(pair_node.act_leaf)])
                subtree.add_child([copy.deepcopy(sequence_structure)])  # subtree 是回不断变化的，它的父亲是self.bt
                if self.verbose:
                    print("完成扩展 a_node= %s,对应的新条件 c_attr= %s,mincost=%d" \
                          % (cond_anc_pair.act_leaf.content.name, cond_anc_pair.cond_leaf.content,
                             cond_anc_pair.cond_leaf.mincost))

            if self.verbose:
                print("遍历所有动作, 寻找符合条件的动作")
            # 遍历所有动作, 寻找符合条件的动作
            current_mincost = pair_node.cond_leaf.mincost # 当前的最短路径是多少

            for i in range(0, len(actions)):
                if not c & ((actions[i].pre | actions[i].add) - actions[i].del_set) <= set():
                    if (c - actions[i].del_set) == c:
                        if self.verbose:
                            print("———— 满足条件可以扩展")
                        c_attr = (actions[i].pre | c) - actions[i].add

                        # 剪枝操作,现在的条件是以前扩展过的条件的超集
                        valid = True
                        for j in self.traversed:  # 剪枝操作
                            if j <= c_attr:
                                valid = False
                                if self.verbose:
                                    print("———— --被剪枝")
                                break

                        if valid:
                            # 把符合条件的动作节点都放到列表里
                            if self.verbose:
                                print("———— -- %s 符合条件放入列表" % actions[i].name)
                            c_attr_node = Leaf(type='cond', content=c_attr, mincost=current_mincost + actions[i].cost)
                            a_attr_node = Leaf(type='act', content=actions[i], mincost=current_mincost + actions[i].cost)
                            cond_anc_pair = CondActPair(cond_leaf=c_attr_node, act_leaf=a_attr_node)
                            self.nodes.append(copy.deepcopy(cond_anc_pair))  # condition node list
                            self.traversed.append(c_attr) # 重点 the set of expanded conditions

        if self.verbose:
            print("算法结束！\n")
        return True

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
    def dfs_ptml(self,parnode):
        for child in parnode.children:
            if isinstance(child, Leaf):
                if child.type == 'cond':
                    self.ptml_string += "cond "
                    c_set_str = ', '.join(map(str, child.content)) + "\n"
                    self.ptml_string += c_set_str
                elif child.type == 'act':
                    self.ptml_string += 'act '+child.content.name+"\n"
            elif isinstance(child, ControlBT):
                if parnode.type == '?':
                    self.ptml_string += "selector{\n"
                    self.dfs_ptml(parnode=child)
                elif parnode.type == '>':
                    self.ptml_string += "sequence{\n"
                    self.dfs_ptml( parnode=child)
                self.ptml_string += '}\n'


    def get_ptml(self):
        self.ptml_string = "selector{\n"
        self.dfs_ptml(self.bt.children[0])
        self.ptml_string += '}\n'
        return self.ptml_string


    def save_ptml_file(self,file_name):
        self.ptml_string = "selector{\n"
        self.dfs_ptml(self.bt.children[0])
        self.ptml_string += '}\n'
        with open(f'./{file_name}.ptml', 'w') as file:
            file.write(self.ptml_string)
        return self.ptml_string
