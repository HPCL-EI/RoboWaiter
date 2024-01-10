import requests
import json
import threading
import queue
import time
import httpx
import asyncio
import re

# API_KEY = ["wxACDRkIWRr0rG4g6GkxKl0f", "K3o8g2Zref6Cdd6rlrSthqTs"]
# SECRET_KEY = ["dBdFoFSgbYGX0GGXY39LEXxTSCcS2Nb1","NVxhNg7u5fjIdwGdnsCOLEpmj96hmDuZ"]

API_KEY = []
SECRET_KEY = []
key_file = "ERNIE_KEYS.txt"
with open(key_file, 'r', encoding="utf-8") as f:
    keys = f.read().strip()
sections = re.split(r'\n\s*\n', keys)
for s in sections:
    x,y = s.strip().splitlines()
    x = x.strip()
    y = y.strip()
    API_KEY.append(x)
    SECRET_KEY.append(y)


question_queue = queue.Queue()
data_queue = queue.Queue()

def get_access_token(apy_key,secret_key):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": apy_key, "client_secret": secret_key}
    return str(requests.post(url, params=params).json().get("access_token"))

def llm_client(access_token):
    while True:
        if question_queue.empty():
            time.sleep(0.001)
        else:
            question_id, question, prompt = question_queue.get()
            if question_id == "<CLOSE>":
                return

            url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token

            payload = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": prompt + "\n" + question
                    },
                ],
                "disable_search": False,
                "enable_citation": False
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            result = json.loads(response.text)["result"]

            # print(question+ "----" + result)
            data_queue.put((question_id,question,result))


class LLMERNIE():
    def __init__(self):
        global data_queue
        data_queue = queue.Queue()
        self.api_index = 0
        self.api_num = len(API_KEY)
        self.threads = []

        self.access_token_list = []
        for i in range(self.api_num):
            access_token = get_access_token(API_KEY[i], SECRET_KEY[i])

            t = threading.Thread(target=llm_client, args=(access_token,))
            t.start()
            self.threads.append(t)

        self.api_time_list = [0.] * self.api_num
        self.speed = 0.5
        self.question_id = 0

    def change_api(self):
        self.api_index = (self.api_index+1)%self.api_num

    def ask(self,question, prompt="",tag=""):
        # select api
        # while True:
        #     t = time.time()
        #     time_gap = time.time() - self.api_time_list[self.api_index]
        #     if time_gap >= self.speed:
        #         break
        #     else:
        #         time.sleep(0.001)
        #         self.change_api()

        question_queue.put((tag, question,prompt))
        # access_token = self.access_token_list[self.api_index]
        # print(access_token)
        #
        # self.api_time_list[self.api_index] = time.time()

        # self.change_api()

    def close(self):
        for i in range(self.api_num):
            question_queue.put(("<CLOSE>","",""))

    def join(self):
        for t in self.threads:
            t.join()

    def get_result(self):
        if not data_queue.empty():
            return data_queue.get()
        else:
            return None

if __name__ == '__main__':
    llm = LLMERNIE()
    result_list = []
    # llm.ask("是吗","")
    # llm.ask("是吗","")
    # llm.ask("是吗","")
    # llm.ask("是吗","")
    llm.close()

    llm.join()
    while not data_queue.empty():
        print(data_queue.get())
    # print(question_queue)

    # llm.join()
    # print(question_queue)
    # print(llm.ask("不是",""))
    # print(llm.ask("是吗",""))
    # print(llm.ask("不是",""))
    # print(llm.ask("是吗",""))
    # print(llm.ask("不是",""))
    # print(llm.ask("是吗",""))
    # print(llm.ask("不是",""))
    # print(llm.ask("是吗",""))
    # print(llm.ask("不是",""))
