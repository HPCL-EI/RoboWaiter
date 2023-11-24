import os
import requests
import urllib3
########################################
#   该文件实现了与大模型的简单通信
########################################

# 忽略https的安全性警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def single_round(question,prefix=""):
    url = "https://45.125.46.134:25344/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "RoboWaiter",
        "messages": [
          {
            "role": "system",
            # "content": "你是一个机器人服务员：RoboWaiter. 你的职责是为顾客提供对话及具身服务。"
            "content": "请将以下你对咖啡厅服务员说的话改写成更清晰更合理的顾客表述。"
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
    with open('goal_states_with_description.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        tmp = line[:-1].split('\t')
        #file.write("""{"title":"%s","text":"%s"}\n""" % (tmp[1], tmp[0]))
        question = tmp[1]
        #print(single_round(question))
        #print(tmp[1])
        with open('output1.txt', 'a',encoding='utf-8') as file:
            file.write(tmp[0]+"\t"+single_round(question)+'\n')
    print("输出完成")