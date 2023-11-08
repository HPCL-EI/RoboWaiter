
import requests
import urllib3

########################################
#   该文件实现了与大模型的简单通信
########################################

# 忽略https的安全性警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ask_llm(question):
    url = "https://45.125.46.134:25344/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "RoboWaiter",
        "messages": [
          {
            "role": "system",
            "content": "你是一个机器人服务员：RoboWaiter. 你的职责是为顾客提供对话及具身服务。"
          },
          {
            "role": "user",
            "content": question
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
    以下是环境信息，请回答对话和目标状态
    [环境信息]
    State: {At(Robot, Table), NotHolding, Available(SpongeGourd)}
    chat_list: [(Customer, "桌子有点脏，能帮我擦一下吗？")]
    '''

    print(ask_llm(question))