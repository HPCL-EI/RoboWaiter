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
    [Condition] 
Near_Robot_<food_place>, On_<food>_<place>, Holding_<food>, Exist_<food>, Is_<furniture>_<furniture_state>

[Object] 
<food>=['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk','VacuumCup','Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater']
<place>=['Bar', 'Bar2', 'WaterTable', 'CoffeeTable', 'Table1', 'Table2', 'Table3','BrightTable6']
<food_place>=<food>+<place>
<furniture>=['AC','TubeLight','HallLight','Curtain','ACTemperature','Table1','Floor','Chairs']
<furniture_state>=['On','Off','Up','Down','Clean','Dirty']

[Examples]
Please put the soft drink on the watertable.
On_Softdrink_WaterTable

Please deliver the coffee to table number one and turn on the hall light.
On_Coffee_Table & Is_HallLight_On

Do not place the water on the bar counter, and please remember to deliver coffee or bernachon to table 2
~On_Water_Bar & (On_Coffee_Table2 | On_Bernachon_Table2)

Please raise the air conditioning temperature and tidy up the chairs.
Is_ACTemperature_On & Is_Chairs_Clean

[Prompt]
[Condition] Lists all predicates representing conditions and their optional parameter sets.
[Object] Lists all parameter sets.
[Examples] Provide several examples of Instruction to Goal mapping.
Please follow the predicate format requirements strictly and, based on the given Instructions, generate Goals that comply with the specifications in predicate formula format. Please generate directly interpretable predicate formulas without additional explanations.
For example, if the Instruction is: "Please raise the air conditioning temperature and tidy up the chairs," your output should only be: 
Is_ACTemperature_On & Is_Chairs_Clean
without any additional information. do not start with Goal:!!

Please put the soft drink on the watertable.
    '''
    import timeit

    cur_time = time.time()
    # print(single_round(question))
    print(single_round(question))
    print(f"单次生成耗时：{time.time() - cur_time} s \n")
