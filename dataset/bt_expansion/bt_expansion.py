import random
import numpy as np
import copy
import time
#定义行动类，行动包括前提、增加和删除影响
class Action:
    def __init__(self,name='anonymous action'):
        self.pre=set()
        self.add=set()
        self.del_set=set()
        self.name=name

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
#叶结点
class Leaf:
    def __init__(self,type,content):
        self.type=type
        self.content=content #conditionset or action
        self.parent=None
        self.parent_index=0

    # tick 叶节点，返回返回值以及对应的条件或行动对象self.content
    def tick(self,state):
        if self.type=='cond':
            if self.content <= state:
                return 'success',self.content
            else:
                return 'failure',self.content
        if self.type=='act':
            if self.content.pre<=state:
                return 'running',self.content #action
            else:
                return 'failure',self.content

    def __str__(self):
        print( self.content)
        return ''

    def print_nodes(self):
        print(self.content)

    def count_size(self):
        return 1
#可能包含控制结点的行为树
class ControlBT:
    def __init__(self,type):
        self.type=type
        self.children=[]
        self.parent=None
        self.parent_index=0


    def add_child(self,subtree_list):
        for subtree in subtree_list:
            self.children.append(subtree)
            subtree.parent=self
            subtree.parent_index=len(self.children)-1

    # tick行为树，根据不同控制结点逻辑tick子结点
    def tick(self,state):
        if len(self.children) < 1:
            print("error,no child")
        if self.type =='?':#选择结点，即或结点
            for child in self.children:
                val,obj=child.tick(state)
                if val=='success':
                    return val,obj
                if val=='running':
                    return val,obj
            return 'failure','?fails'
        if self.type =='>':#顺序结点，即与结点
            for child in self.children:
                val,obj=child.tick(state)
                if val=='failure':
                    return val,obj
                if val=='running':
                    return val,obj
            return 'success', '>success'
        if self.type =='act':#行动结点
            return self.children[0].tick(state)
        if self.type =='cond':#条件结点
            return self.children[0].tick(state)

    def getFirstChild(self):
        return self.children[0]

    def __str__(self):
        print(self.type+'\n')
        for child in self.children:
            print (child)
        return ''

    def print_nodes(self):
        print(self.type)
        for child in self.children:
            child.print_nodes()

    # 递归统计树中结点数
    def count_size(self):
        result=1
        for child in self.children:
            result+= child.count_size()
        return result


#本文所提出的完备规划算法
class BTalgorithm:
    def __init__(self):
        self.bt = None
        self.nodes=[]
        self.traversed=[]
        self.conditions=[]
        self.conditions_index=[]
        #print (self.conditions_list[0])

    def clear(self):
        self.bt = None
        self.nodes = []
        self.traversed = []
        self.conditions = []
        self.conditions_index = []

    #运行规划算法，从初始状态、目标状态和可用行动，计算行为树self.bt
    def run_algorithm(self,start,goal,actions):
        # 初始行为树只包含目标条件
        self.bt = ControlBT(type='cond')
        g_node = Leaf(type='cond', content=goal)
        self.bt.add_child([g_node])


        self.conditions.append(goal)
        self.nodes.append(g_node) #condition node list
        # 尝试在初始状态执行行为树
        val, obj = self.bt.tick(start)
        canrun = False
        if val == 'success' or val == 'running':
            canrun = True
        # 循环扩展，直到行为树能够在初始状态运行
        while not canrun:
            index = -1
            for i in range(0,len(self.nodes)):
                if self.nodes[i].content in self.traversed:
                    continue
                else:
                    c_node = self.nodes[i]
                    index = i
                    break
            if index == -1:#树中结点扩展完毕，仍无法运行行为树，返回失败
                print('Failure')
                return False
            #根据所选择条件结点扩展子树
            subtree = ControlBT(type='?')
            subtree.add_child([copy.deepcopy(c_node)])#子树首先保留所扩展结点
            c = c_node.content#子树所扩展结点对应的条件（一个文字的set）

            for i in range(0,len(actions)):#选择符合条件的行动，
                #print("have action")
                if not c & ( (actions[i].pre | actions[i].add)-actions[i].del_set) <=set():
                    #print ("pass add")
                    if (c - actions[i].del_set) == c:
                        #print("pass delete")
                        c_attr = (actions[i].pre | c )-actions[i].add
                        valid = True
                        for j in self.traversed:#剪枝操作
                            if j<=c_attr:
                                valid = False
                                break
                        if valid:
                            #print("pass prune")
                            # 构建行动的顺序结构
                            sequence_structure=ControlBT(type='>')
                            c_attr_node = Leaf(type='cond', content=c_attr)
                            a_node = Leaf(type='act', content=actions[i])
                            sequence_structure.add_child([c_attr_node,a_node])
                            # 将顺序结构添加到子树
                            subtree.add_child([sequence_structure])

                            self.nodes.append(c_attr_node)
            # 将原条件结点c_node替换为扩展后子树subtree
            parent_of_c = c_node.parent
            parent_of_c.children[0] = subtree
            #记录已扩展条件
            self.traversed.append(c)
            # 尝试在初始状态运行行为树
            val, obj = self.bt.tick(start)
            canrun = False
            if val == 'success' or val == 'running':
                canrun = True
        return True

    def print_solution(self):
        print(len(self.nodes))
        # for i in self.nodes:
        #     if isinstance(i,Node):
        #         print (i.content)
        #     else:
        #         print (i)

#所对比的基准算法，具体扩展细节有差异
class Weakalgorithm:
    def __init__(self):
        self.bt=None
        self.nodes=[]
        self.traversed=[]
        self.conditions=[]
        self.conditions_index=[]
        self.danger=False
        #print (self.conditions_list[0])

    def clear(self):
        self.bt=None
        self.nodes = []
        self.traversed = []
        self.conditions = []
        self.conditions_index = []
        self.danger = False

    def run_algorithm(self,start,goal,actions):
        self.bt = ControlBT(type='cond')
        g_node = Leaf(type='cond', content=goal)
        self.bt.add_child([g_node])

        # self.nodes.append(goal)
        self.conditions.append(goal)
        self.nodes.append(g_node)  # condition node list
        # nodes_start_index=0
        # self.conditions_index.append(0)
        val, obj = self.bt.tick(start)
        canrun = False
        if val == 'success' or val == 'running':
            canrun = True
        while not canrun:
            #print ("loop begin")
            index = -1
            for i in range(0,len(self.nodes)):
                if self.nodes[i].content in self.traversed:
                    continue
                else:
                    c_node = self.nodes[i]
                    index = i
                    break
            #print (index)
            if index == -1:
                print('Algorithm Failure, all conditions expanded')
                return False
            subtree = ControlBT(type='?')
            subtree.add_child([copy.deepcopy(c_node)])
            c = c_node.content

            for i in range(0,len(actions)):
                if not c &  actions[i].add <= set():
                    if not (c - actions[i].del_set) == c:
                        danger = True
                        self.danger = True
                        #continue
                    c_attr = actions[i].pre
                    valid = True
                    if valid:
                        sequence_structure = ControlBT(type='>')

                        for j in c_attr:
                            if j in self.traversed:
                                continue
                            c_attr_node = Leaf(type='cond', content={j})


                            sequence_structure.add_child([c_attr_node])
                            if j in start:
                                continue
                            self.nodes.append(c_attr_node)

                        a_node = Leaf(type='act', content=actions[i])
                        sequence_structure.add_child([ a_node])
                        subtree.add_child([sequence_structure])


            parent_of_c = c_node.parent
            p_index = c_node.parent_index
            parent_of_c.children[p_index] = subtree

            self.traversed.append(c)
            val, obj = self.bt.tick(start)
            canrun = False
            if val == 'success' or val == 'running':
                canrun = True
        return True

    def print_solution(self):
        print(len(self.nodes))




if __name__ == '__main__':
    random.seed(1)
    # 设置生成规划问题集的超参数：文字数、解深度、迭代次数
    literals_num=10
    depth = 10
    iters= 10
    total_tree_size = []
    total_action_num = []
    total_state_num = []
    total_steps_num=[]
    #fail_count=0
    #danger_count=0
    success_count =0
    failure_count = 0
    planning_time_total = 0.0
    # 实验1000次
    for count in range (0,1000):
        # 生成一个规划问题，包括随机的状态和行动，以及目标状态
        states = []
        actions = []
        start = generate_random_state(literals_num)
        state = start
        states.append(state)
        #print (state)
        for i in range (0,depth):
            a = Action()
            a.generate_from_state(state,literals_num)
            if not a in actions:
                actions.append(a)
            state = state_transition(state,a)
            if state in states:
                pass
            else:
                states.append(state)
                #print(state)

        goal = states[-1]
        state = start
        for i in range (0,iters):
            a = Action()
            a.generate_from_state(state,literals_num)
            if not a in actions:
                actions.append(a)
            state = state_transition(state,a)
            if state in states:
                pass
            else:
                states.append(state)
            state = random.sample(states,1)[0]
        # 选择测试本文算法btalgorithm，或对比算法weakalgorithm
        algo = BTalgorithm()
        #algo = Weakalgorithm()
        start_time = time.time()
        if algo.run_algorithm(start, goal, list(actions)):#运行算法，规划后行为树为algo.bt
            total_tree_size.append( algo.bt.count_size()-1)
        else:
            print ("error")
        end_time = time.time()
        planning_time_total += (end_time-start_time)


        #开始从初始状态运行行为树，测试
        state=start
        steps=0
        val, obj = algo.bt.tick(state)#tick行为树，obj为所运行的行动
        while val !='success' and val !='failure':#运行直到行为树成功或失败
            state = state_transition(state,obj)
            val, obj = algo.bt.tick(state)
            if(val == 'failure'):
                print("bt fails at step",steps)
            steps+=1
            if(steps>=500):#至多运行500步
                break
        if not goal <= state:#错误解，目标条件不在执行后状态满足
            #print ("wrong solution",steps)
            failure_count+=1

        else:#正确解，满足目标条件
            #print ("right solution",steps)
            success_count+=1
            total_steps_num.append(steps)
        algo.clear()
        total_action_num.append(len(actions))
        total_state_num.append(len(states))
    print (success_count,failure_count)#算法成功和失败次数

    print(np.mean(total_tree_size), np.std(total_tree_size, ddof=1))#1000次测试树大小
    print (np.mean(total_steps_num),np.std(total_steps_num,ddof=1))
    print (np.mean(total_state_num))#1000次问题的平均状态数
    print (np.mean(total_action_num))#1000次问题的平均行动数
    print(planning_time_total,planning_time_total/1000.0)

    #print(total_state_num)

#casestudy begin 对应论文的case study，包含三个行动的移动机械臂场景

    # actions=[]
    # a = Action(name='movebtob')
    # a.pre={1,2}
    # a.add={3}
    # a.del_set={1,4}
    # actions.append(a)
    # a=Action(name='moveatob')
    # a.pre={1}
    # a.add={5,2}
    # a.del_set={1,6}
    # actions.append(a)
    # a=Action(name='moveatoa')
    # a.pre={7}
    # a.add={8,2}
    # a.del_set={7,6}
    # actions.append(a)
    #
    # start = {1,7,4,6}
    # goal={3}
    # algo = BTalgorithm()
    # algo.clear()
    # algo.run_algorithm(start, goal, list(actions))
    # state = start
    # steps = 0
    # val, obj = algo.bt.tick(state)
    # while val != 'success' and val != 'failure':
    #     state = state_transition(state, obj)
    #     print (obj.name)
    #     val, obj = algo.bt.tick(state)
    #     if (val == 'failure'):
    #         print("bt fails at step", steps)
    #     steps += 1
    # if not goal <= state:
    #     print ("wrong solution",steps)
    # else:
    #     print ("right solution",steps)
    # #algo.bt.print_nodes()
    # print (algo.bt.count_size()-1)
    # algo.clear()

#case study end
