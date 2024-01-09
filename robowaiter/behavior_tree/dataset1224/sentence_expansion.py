import os
import requests
import urllib3
from tqdm import tqdm

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
                "content": """
                假设现在你是咖啡厅的一个顾客，请将以下你对咖啡厅服务员说的话改写成更清晰更合理的顾客表述。注意：句中的你指的是咖啡厅服务员，也不要说能帮我。
                例如：麻烦你去一下吧台。可以转述成：服务员，你能去下吧台吗？ 
                另一个例子：请你拿一下酸奶到吧台位置。可以转述成：服务员，拿一杯酸奶来吧台。
                
                """
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
    with open('./goal_states_with_description.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_file = './expansion_out/output2.txt'
    with open(output_file, 'a', encoding='utf-8') as file:
        file.truncate(0)
    for line in tqdm(lines):
        tmp = line[:-1].split('\t')
        # file.write("""{"title":"%s","text":"%s"}\n""" % (tmp[1], tmp[0]))
        question = tmp[1]
        # print(single_round(question))
        # print(tmp[1])
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(tmp[0] + "\t" + single_round(question, prefix="现在改写一下句子：") + '\n')
    print("输出完成")
