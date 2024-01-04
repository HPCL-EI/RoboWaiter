import time

import requests
import urllib3

########################################
#   该文件实现了与大模型的简单通信
########################################

# 忽略https的安全性警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def single_round(question, prefix=""):
    url = "https://45.125.46.134:25344/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "RoboWaiter",
        "messages": [
            {
                "role": "system",
                # "content": "你是一个机器人服务员：RoboWaiter. 你的职责是为顾客提供对话及具身服务。"
                "content": ""
                # "content":
                # """
                # 你是一个熟悉行为树的工程师，你的职责是根据用户需求，为一个人型的机器人设计完成用户需求的行为树序列。
                # 行为树是一种有向根树，他的内部节点称为控制节点，控制节点包括选择、顺序，顺序节点只有所有子节点返回成功之后他才成功。
                # 选择节点只要有一个子节点返回成功最后就成功。叶节点称为执行节点，执行节点包括动作节点和条件节点。动作节点执行具体的动作，条件节点检查环境中的条件是否满足。
                # """
                # "content": "你是一个优秀的目标状态规划师，能够根据用户输入，规划出所需要的目标状态。例如：打开窗帘的目标状态可以是Is(Curtain, On)"
            },
            {
                "role": "user",
                "content": prefix + question
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return "大模型请求失败:", response.status_code


if __name__ == '__main__':
    question = '''
from actions import MoveTo (<obj>/<place>), PickUp (<obj>), PutDown (<obj>,<place>), PutDown(Anything,Anywhere), Make (<obj2>), Clean (<obj3>), Turn (<obj4>,<obj4state>)
from states import At (Robor,<obj>/<place>), On (<obj>,<place>), Holding (<obj>), Is (<obj4>,<obj4state>), Exist (<obj>)

obj=['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk','VacuumCup','Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater']
place=['Bar', 'Bar2', 'WaterTable', 'CoffeeTable', 'Table1', 'Table2', 'Table3','BrightTable6']
obj2=['Coffee', 'Water', 'Dessert']
obj3=['Table1','Floor','Chairs']
obj4=['AC','TubeLight','HallLight','Curtain','ACTemperature']
obj4state=['On','Off','Up','Down']

currents_state={'At(Robot,Bar)', 'Is(AC,Off)',
                  'Exist(Yogurt)', 'Exist(BottledDrink)','Exist(Softdrink)','Exist(VacuumCup)', 
                  'Holding(Coffee)',
                  'On(VacuumCup,Table2)', 'On(Yogurt,Bar)', 'On(BottledDrink,Bar)', 'On(Softdrink,Table1)',
                  'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
                  'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
def Put_SoftDrink_on_WaterTable(currents_state):
    selector
        sequence
            cond At(Robot, Table1)
            cond Holding(Nothing)
            cond On(Softdrink, Table1)
            act PickUp(Softdrink)
        sequence
            cond At(Robot, Table1)
            act MoveTo(WaterTable)
        sequence
            cond Holding(Softdrink)
            cond At(Robot, WaterTable)
            act PutDown(Softdrink, WaterTable)
        sequence
            act MoveTo(Table1)
         

currents_state={'At(Robot,Bar)', 'Is(AC,On)',
                  'Exist(Yogurt)', 'Exist(BottledDrink)',
                  'Exist(Chips)', 'Exist(VacuumCup)', 'Exist(ADMilk)',
                  'Holding(Nothing)',
                  'On(VacuumCup,Table2)', 'On(Chips,Bar)','On(ADMilk,Bar)',
                  'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
                  'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
def Put_Dessert_on_Bar(currents_state):
    selector
        cond On(Dessert,Bar)
        sequence
            cond Holding(Nothing)
            act Make(Dessert)


currents_state={'At(Robot,Bar)', 'Is(AC,Off)',
                  'Exist(VacuumCup)','Exist(Coffee)',
                  'On(VacuumCup,Table2)', 'On(Coffee,CoffeeTable)',
                  'Holding(Nothing)',
                  'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
                  'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
def Put_Coffee_on_Bar(currents_state):
    selector
        sequence
            cond At(Robot, Bar)
            cond Exist(Coffee)
            cond Holding(Nothing)
            act PickUp(Coffee)
        sequence
            cond Holding(Coffee)
            act PutDown(Coffee, Bar)
        sequence
            cond At(Robot, Bar)
            act MoveTo(Bar)


currents_state={'At(Robot,Bar)', 'Is(AC,Off)',
              'Exist(Yogurt)', 'Exist(BottledDrink)','Exist(Softdrink)',
              'Exist(Chips)', 'Exist(NFCJuice)', 'Exist(Bernachon)', 'Exist(ADMilk)', 'Exist(SpringWater)',
              'Holding(Softdrink)',
              'Exist(VacuumCup)', 'On(VacuumCup,Table2)',
              'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
              'Is(Table1,Clean)', 'Is(Floor,Clean)', 'Is(Chairs,Clean)'}  
def Turn_AC_Temperature_Down(currents_state):
    selector
        cond Is(ACTemperature,Down)
        sequence
            cond Is(AC,On)
            selector
                sequence
                    cond Holding(Nothing)
                    act Turn(ACTemperature,Down)
                act PutDown(Anything,Anywhere)
        sequence
            cond Is(AC,Off)
            selector
                sequence
                    cond Holding(Nothing)
                    act Turn(AC,On)
                act PutDown(Anything,Anywhere)
                

currents_state={'At(Robot,Bar)', 'Is(AC,Off)',
                  'Exist(Yogurt)','Exist(VacuumCup)',
                  'Holding(Nothing)',
                  'On(Yogurt,Bar)','On(VacuumCup,Table2)',
                  'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
                  'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}   
def Put_Coffee_on_Table3(currents_state):


Please complete the function Put_Coffee_on_Table3(currents_state) by constructing a behavior tree. In this tree, only use 'selectors' and 'sequences' as control nodes. For the leaf nodes, exclusively utilize the actions and states that are defined in the previously imported 'actions' and 'states' modules. 
    '''
    import timeit

    cur_time = time.time()
    print(single_round(question))
    # print(single_round(question, prefix='现在给出符合这句话要求的目标状态: '))
    print(f"单次生成耗时：{time.time() - cur_time} s \n")
