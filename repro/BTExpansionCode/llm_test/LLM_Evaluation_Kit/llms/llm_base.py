import requests
import json
import threading
import queue
import time
import httpx
import asyncio
import re


def llm_client(thread_idx, llm):
    while True:
        if llm.question_queue.empty():
            time.sleep(0.001)
        else:
            question_id, question, prompt = llm.question_queue.get()
            if question_id == "<CLOSE>":
                return

            result = llm.send_mesage(thread_idx, question, prompt)

            llm.data_queue.put((question_id,question,result))


class LLMBase():
    def __init__(self):
        self.data_queue = queue.Queue()
        self.question_queue = queue.Queue()

        self.api_index = 0
        self.api_num = 0
        self.rpm = 20
        self.threads = []

    def create_threads(self):
        self.access_token_list = []
        for i in range(self.api_num):
            access_token = get_access_token(API_KEY[i], SECRET_KEY[i])

            t = threading.Thread(target=llm_client, args=(access_token,self))
            t.start()
            self.threads.append(t)

        self.api_time_list = [0.] * self.api_num
        self.speed = 0.5
        self.question_id = 0

    def change_thread(self):
        self.api_index = (self.api_index+1)%self.api_num

    def ask(self,question, prompt="",tag=""):
        self.question_queue.put((tag, question,prompt))


    def close(self):
        for i in range(self.api_num):
            self.question_queue.put(("<CLOSE>","",""))

    def join(self):
        for t in self.threads:
            t.join()

    def get_result(self):
        if not self.data_queue.empty():
            return self.data_queue.get()
        else:
            return None

if __name__ == '__main__':
    llm = LLMERNIE()
    result_list = []
    llm.ask("是吗","")
    llm.ask("是吗","")
    llm.ask("是吗","")
    llm.ask("是吗","")
    llm.close()

    llm.join()
    while not llm.data_queue.empty():
        print(llm.data_queue.get())
    # print(question_queue)

    # llm_client.join()
    # print(question_queue)
    # print(llm_client.ask("不是",""))
    # print(llm_client.ask("是吗",""))
    # print(llm_client.ask("不是",""))
    # print(llm_client.ask("是吗",""))
    # print(llm_client.ask("不是",""))
    # print(llm_client.ask("是吗",""))
    # print(llm_client.ask("不是",""))
    # print(llm_client.ask("是吗",""))
    # print(llm_client.ask("不是",""))
