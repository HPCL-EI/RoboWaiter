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
    '''
    [round 2]
Invalid Output: Clear_Water_From_Table
there are 3 errors: 
Format Error: 0
Predicate Error: Clear_Water_From_Table -- Clear is not a valid predicate
Object Error: From is not a valid object
Object Error: Or,Present  is not a valid object

[round 3]
Invalid Output: Clear_Water_From_Table & (On_Coffee_Table | On_Yogurt_Table)
Invalid Predicates: Clear
Invalid Objects: From


please try again and output without errors.

    '''




    question = '''
    [Condition] 
Near_Robot_<food_place>

[Object] 
<food>=['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk','VacuumCup','Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater']
<place>=['Bar', 'Bar2', 'WaterTable', 'CoffeeTable', 'Table1', 'Table2', 'Table3','BrightTable6']


[Examples] 
Input: Please put the soft drink on the watertable.
Output: On_Softdrink_WaterTable

Input: Please deliver the coffee to table number one and turn on the hall light.
Output: On_Coffee_Table & Is_HallLight_On

Input: Do not place the water on the bar counter, and please remember to deliver coffee or bernachon to table 2
Output: ~On_Water_Bar & (On_Coffee_Table2 | On_Bernachon_Table2)

Input: Please raise the air conditioning temperature and tidy up the chairs.
Output: & Is_Chairs_Clean

Input: Could you please clear the water from the table? I would like a cup of coffee or yogurt.

please output the right well-formed formula, Clear_Water_From_Table is wrong, don't output it
    '''
    import timeit

    cur_time = time.time()
    # print(single_round(question))
    print(single_round(question))
    print(f"单次生成耗时：{time.time() - cur_time} s \n")
