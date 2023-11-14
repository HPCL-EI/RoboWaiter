import os

import requests
import urllib3
from robowaiter.utils import get_root_path
from robowaiter.llm_client.single_round import single_round
########################################
#   该文件实现了与大模型的简单通信
########################################

# 忽略https的安全性警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

root_path = get_root_path()
# load test questions
file_path = os.path.join(root_path,"robowaiter/llm_client/data/test_questions.txt")

with open(file_path,'r',encoding="utf-8") as f:
    test_questions_dict = eval(f.read())

def ask_llm(question):
    if question in test_questions_dict:
        ans = test_questions_dict[question]
    else:
        ans = single_round(question)
    print(f"大模型输出： {ans}")
    return ans


if __name__ == '__main__':
    question = '''测试VLM：做一杯咖啡'''

    print(ask_llm(question))