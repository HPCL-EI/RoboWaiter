import requests
import urllib3

########################################
#   该文件实现了与大模型的简单通信
########################################

# 忽略https的安全性警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#在这里输入你的问题
question = "假设你是一个咖啡厅的机器人服务员，有一个顾客的请求是'请给我一杯咖啡'，请生成对应的行为树来控制机器人完成该动作"

url = "https://45.125.46.134:25344/v1/completions"
headers = {"Content-Type": "application/json"}
data = {
    "prompt": question
}

response = requests.post(url, headers=headers, json=data, verify=False)

if response.status_code == 200:
    result = response.json()
    print(f'问题：{question}')
    print('回答：' + result['choices'][0]['text'])
else:
    print("请求失败:", response.status_code)

