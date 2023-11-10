
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


def ask_llm(question):
    ans = single_round(question)
    return ans


if __name__ == '__main__':
    question = '''
    python中如何通过类名字符串的方式来代替isinstance的作用
    '''

    print(ask_llm(question))