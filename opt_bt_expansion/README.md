

## 代码说明

### 1. `BehaviorTree.py` 实现行为树叶子结点和非叶子结点的定义

- **Leaf**：表示叶节点，可以是动作（`act`）或条件（`cond`）。
- **ControlBT**：代表可能包含控制节点的行为树。它们可以是选择器（`?`）、序列（`>`）、动作节点（`act`）或条件节点（`cond`）。
- 上述两个类都包含 `tick` 方法。

### 2.  `OptimalBTExpansionAlgorithm.py` 实现最优行为树扩展算法

![image-20231103191141047](README.assets/image-20231103191141047.png)

定义行动类
```python
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
```

调用算法
```python
algo = OptBTExpAlgorithm(verbose=True)
algo.clear()
algo.run_algorithm(start, goal, actions) # 使用算法得到行为树在 algo.bt
algo.print_solution() # 打印行为树 
val, obj = algo.bt.tick(state) # 执行行为树
algo.save_ptml_file("bt.ptml") # 保存行为树为 ptml 文件
```

### 3. **`tools.py`**  实现打印数据、行为树测试等模块

使用方法

```python
print_action_data_table(goal,start,actions) # 打印所有变量

# 行为树鲁棒性测试，随机生成规划问题
# 设置生成规划问题集的超参数：文字数、解深度、迭代次数
seed=1
literals_num=10
depth = 10
iters= 10
BTTest(seed=seed,literals_num=literals_num,depth=depth,iters=iters)
```

### 4. `example.py` 中设计规划案例 goals, start,actions

```python
def MoveBtoB ():
    actions=[]
    a = Action(name="Move(b,ab)") 
    a.pre={'Free(ab)','WayClear'}  
    a.add={'At(b,ab)'} 
    a.del_set= {'Free(ab)','At(b,pb)'}         
    a.cost = 1
    actions.append(a)

    a=Action(name="Move(s,ab)") 
    a.pre={'Free(ab)'} 
    a.add={'Free(ab)','WayClear'} 
    a.del_set={'Free(ab)','At(s,ps)'}  
    a.cost = 1
    actions.append(a)

    a=Action(name="Move(s,as)")
    a.pre={'Free(as)'} 
    a.add={'At(s,ps)','WayClear'} 
    a.del_set={'Free(as)','At(s,ps)'} 
    a.cost = 1
    actions.append(a)

    start = {'Free(ab)','Free(as)','At(b,pb)','At(s,ps)'} 
    goal= {'At(b,ab)'} 
    return goal,start,actions
```

### 5. `opt_bt_exp_main.py` 为主函数，在此演示如何调用最优行为树扩展算法得到完全扩展最优行为树
```python
actions=[
    Action(name='PutDown(Table,Coffee)', pre={'Holding(Coffee)','At(Robot,Table)'}, add={'At(Table,Coffee)','NotHolding'}, del_set={'Holding(Coffee)'}, cost=1)
	…………
]
algo = BTOptExpInterface(actions)

goal = {'At(Table,Coffee)'}
ptml_string = algo.process(goal,start)
print(ptml_string)

```
两种检测方法，用于检测当前状态 `start` 能否到达目标状态 `goal`

```python
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

```

