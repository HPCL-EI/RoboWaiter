
from opt_bt_expansion.OptimalBTExpansionAlgorithm import Action



def MakeCoffee():
    actions=[
        Action(name='Put(Table,Coffee)', pre={'Holding(Coffee)','At(Table)'}, add={'At(Table,Coffee)','NotHolding'}, del_set={'Holding(Coffee)'}, cost=1),
        Action(name='Put(Table,VacuumCup)', pre={'Holding(VacuumCup)','At(Table)'}, add={'At(Table,VacuumCup)','NotHolding'}, del_set={'Holding(VacuumCup)'}, cost=1),

        Action(name='Grasp(Coffee)', pre={'NotHolding','At(Coffee)'}, add={'Holding(Coffee)'}, del_set={'NotHolding'}, cost=1),

        Action(name='MoveTo(Table)', pre={'Exist(Table)'}, add={'At(Table)'}, del_set={'At(FrontDesk)','At(Coffee)','At(CoffeeMachine)'}, cost=1),
        Action(name='MoveTo(Coffee)', pre={'Exist(Coffee)'}, add={'At(Coffee)'}, del_set={'At(FrontDesk)','At(Table)','At(CoffeeMachine)'}, cost=1),
        Action(name='MoveTo(CoffeeMachine)', pre={'Exist(CoffeeMachine)'}, add={'At(CoffeeMachine)'}, del_set={'At(FrontDesk)','At(Coffee)','At(Table)'}, cost=1),

        Action(name='OpCoffeeMachine', pre={'At(CoffeeMachine)','NotHolding'}, add={'Exist(Coffee)','At(Coffee)'}, del_set=set(), cost=1),
    ]

    start = {'At(FrontDesk)','Holding(VacuumCup)','Exist(Table)','Exist(CoffeeMachine)','Exist(FrontDesk)'}
    goal = {'At(Table,Coffee)'}
    return goal,start,actions

# 本例子中，将 VacuumCup 放到 FrontDesk，比 MoveTo(Table) 再 Put(Table,VacuumCup) 的 cost 要小
def MakeCoffeeCost():
    actions=[
        Action(name='PutDown(Table,Coffee)', pre={'Holding(Coffee)','At(Robot,Table)'}, add={'At(Table,Coffee)','NotHolding'}, del_set={'Holding(Coffee)'}, cost=1),
        Action(name='PutDown(Table,VacuumCup)', pre={'Holding(VacuumCup)','At(Robot,Table)'}, add={'At(Table,VacuumCup)','NotHolding'}, del_set={'Holding(VacuumCup)'}, cost=1),

        Action(name='PickUp(Coffee)', pre={'NotHolding','At(Robot,Coffee)'}, add={'Holding(Coffee)'}, del_set={'NotHolding'}, cost=1),

        Action(name='MoveTo(Table)', pre={'Available(Table)'}, add={'At(Robot,Table)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Coffee)','At(Robot,CoffeeMachine)'}, cost=1),
        Action(name='MoveTo(Coffee)', pre={'Available(Coffee)'}, add={'At(Robot,Coffee)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Table)','At(Robot,CoffeeMachine)'}, cost=1),
        Action(name='MoveTo(CoffeeMachine)', pre={'Available(CoffeeMachine)'}, add={'At(Robot,CoffeeMachine)'}, del_set={'At(Robot,FrontDesk)','At(Robot,Coffee)','At(Robot,Table)'}, cost=1),

        Action(name='OpCoffeeMachine', pre={'At(Robot,CoffeeMachine)','NotHolding'}, add={'Available(Coffee)','At(Robot,Coffee)'}, del_set=set(), cost=1),
    ]

    start = {'At(Robot,Bar)','Holding(VacuumCup)','Available(Table)','Available(CoffeeMachine)','Available(FrontDesk)'}
    goal = {'At(Table,Coffee)'}

    return goal,start,actions


# test
def Test():
    actions=[
        Action(name='a1', pre={6}, add={0,2,4}, del_set={1,5}, cost=1),
        Action(name='a2', pre=set(), add={0,1}, del_set=set(), cost=1),
        Action(name='a3', pre={1,6}, add={0,2,3,5}, del_set={1,6}, cost=1),
        Action(name='a4', pre={0,2,3}, add={4,5}, del_set={0,6}, cost=1),
        Action(name='a5', pre={0,1,4}, add={2,3,6}, del_set={0}, cost=1),
    ]

    start = {1,2,6}
    goal={0,1,2,4,6}
    return goal,start,actions

# def Test():
#     actions=[
#         Action(name='a1', pre={2}, add={1}, del_set=set(), cost=1),
#         Action(name='a2', pre=set(), add={1}, del_set={0,2}, cost=1),
#         Action(name='a3', pre={1}, add=set(), del_set={0,2}, cost=1),
#         Action(name='a4', pre=set(), add={0}, del_set=set(), cost=1),
#         Action(name='a5', pre={1}, add={0,2}, del_set={1}, cost=1),
#         Action(name='a6', pre={1}, add=set(), del_set={0,1,2}, cost=1),
#         Action(name='a7', pre={1}, add={2}, del_set={0, 2}, cost=1),
#     ]
#
#     start = {1,2}
#     goal={0,1}
#     return goal,start,actions


# todo: 最原始的例子
def MoveBtoB_num ():
    actions=[]
    a = Action(name='a1')
    a.pre={1,4}
    a.add={"c_goal"}
    a.del_set={1,4}
    a.cost = 1
    actions.append(a)

    a=Action(name='a2')
    a.pre={1,2,3}
    a.add={"c_goal"}
    a.del_set={1,2,3}
    a.cost = 1
    actions.append(a)

    a=Action(name='a3')
    a.pre={1,2}
    a.add={4}
    a.del_set={2}
    a.cost = 1
    actions.append(a)

    a=Action(name='a4')
    a.pre={"c_start"}
    a.add={1,2,3}
    a.del_set={"c_start",4}
    a.cost = 1
    actions.append(a)

    start = {"c_start"}
    goal={"c_goal"}
    return goal,start,actions


# todo: 最原始的例子
def MoveBtoB ():
    actions=[]
    a = Action(name="Move(b,ab)") #'movebtob'
    a.pre={'Free(ab)','WayClear'}  #{1,2}
    a.add={'At(b,ab)'} #{3}
    a.del_set= {'Free(ab)','At(b,pb)'}         #{1,4}
    a.cost = 1
    actions.append(a)

    a=Action(name="Move(s,ab)") #'moveatob'
    a.pre={'Free(ab)'} #{1}
    a.add={'Free(ab)','WayClear'} #{5,2}
    a.del_set={'Free(ab)','At(s,ps)'}  #{1,6}
    a.cost = 1
    actions.append(a)

    a=Action(name="Move(s,as)") #'moveatoa'
    a.pre={'Free(as)'} #{7}
    a.add={'At(s,ps)','WayClear'} #{8,2}
    a.del_set={'Free(as)','At(s,ps)'} #{7,6}
    a.cost = 1
    actions.append(a)

    start = {'Free(ab)','Free(as)','At(b,pb)','At(s,ps)'} #{1,7,4,6}
    goal= {'At(b,ab)'} #{3}
    return goal,start,actions


# 小蔡师兄论文里的例子
def Cond2BelongsToCond3():
    actions=[]
    a = Action(name='a1')
    a.pre={1,4}
    a.add={"c_goal"}
    a.del_set={1,4}
    a.cost = 1
    actions.append(a)

    a=Action(name='a2')
    a.pre={1,2,3}
    a.add={"c_goal"}
    a.del_set={1,2,3}
    a.cost = 100
    actions.append(a)

    a=Action(name='a3')
    a.pre={1,2}
    a.add={4}
    a.del_set={2}
    a.cost = 1
    actions.append(a)

    a=Action(name='a4')
    a.pre={"c_start"}
    a.add={1,2,3}
    a.del_set={"c_start",4}
    a.cost = 1
    actions.append(a)

    start = {"c_start"}
    goal={"c_goal"}
    return goal,start,actions

