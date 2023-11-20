import json
import time

import openai
from colorama import init, Fore
from loguru import logger
import json
from robowaiter.llm_client.tool_register import get_tools, dispatch_tool
import requests
import json
from collections import deque

import urllib3
import copy
init(autoreset=True)
from robowaiter.utils import get_root_path
import os
import re
from robowaiter.llm_client.single_round import single_round
########################################
#   该文件实现了与大模型的通信以及工具调用
########################################

# 忽略https的安全性警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://45.125.46.134:25344" # 本地部署的地址,或者使用你访问模型的API地址

root_path = get_root_path()
# load test questions
file_path = os.path.join(root_path,"robowaiter/llm_client/data/fix_questions.txt")

functions = get_tools()

fix_questions_dict = {}
no_reply_functions = ["create_sub_task"]

with open(file_path,'r',encoding="utf-8") as f:
     #读取所有行
    lines = f.read().strip()
    sections = re.split(r'\n\s*\n', lines)
    for s in sections:
        x = s.strip().splitlines()
        if len(x) == 2:
            fix_questions_dict[x[0]] = {
                "answer": x[1],
                "function": None
            }
        else:
            fix_questions_dict[x[0]] = {
                "answer": x[1],
                "function": x[2],
                "args": x[3]
            }


role_system = [{
        "role": "system",
        "content": "你是RoboWaiter,一个由HPCL团队开发的机器人服务员，你在咖啡厅工作。接受顾客的指令并调用工具函数来完成各种服务任务。如果顾客问你们这里有什么，或者想要点单，你说我们咖啡厅提供咖啡，水，点心，酸奶等食物。如果顾客不需要你了，你就回到吧台招待。如果顾客叫你去做某事，你回复：好的，我马上去做这件事。",
    }]

def new_history(max_length=7):
    history = deque(maxlen=max_length)

    return history

def new_response():
    return {'choices': [{'index': 0, 'message':{} }]}

def parse_fix_question(question):
    response = new_response()
    fix_ans = fix_questions_dict[question]
    if not fix_ans['function']: #简单对话
        message = {'role': 'assistant', 'content': fix_ans["answer"], 'name': None,
         'function_call': None}
    else:
        func = fix_ans["function"]
        args = fix_ans["args"]
        # tool_response = dispatch_tool(function_call["name"], json.loads(args))
        # logger.info(f"Tool Call Response: {tool_response}")
        message = {'role': 'assistant',
         'content': f"\n <|assistant|>  {func}({args})\n ```python\ntool_call(goal={args})\n```",
         'name': None,
         'function_call': {'name': func, 'arguments': args}}

    response["choices"][0]["message"] = message
    return response

def get_response(sentence, history, allow_function_call = True):
    if sentence:
        history.append({"role": "user", "content": sentence})

    if sentence in fix_questions_dict:
        time.sleep(2)
        return parse_fix_question(sentence)

    params = dict(model="RoboWaiter")
    params['messages'] = role_system + list(history)
    if allow_function_call:
        params["functions"] = functions


    response = requests.post(f"{base_url}/v1/chat/completions", json=params, stream=False, verify=False)
    decoded_line = response.json()
    return decoded_line

def deal_response(response, history, func_map=None ):
    if response["choices"][0]["message"].get("function_call"):
        function_call = response["choices"][0]["message"]["function_call"]
        logger.info(f"Function Call Response: {function_call}")

        function_name = function_call["name"]
        function_args = json.loads(function_call["arguments"])
        if func_map:
            tool_response = func_map[function_name](**function_args)
        else:
            try:
                tool_response = dispatch_tool(function_call["name"], function_args)
                logger.info(f"Tool Call Response: {tool_response}")
            except:
                logger.info(f"重试工具调用")
        # tool_response = dispatch_tool(function_call["name"], function_args)
            return function_name,None

        return_message = response["choices"][0]["message"]

        history.append(return_message)
        t = {
            "role": "function",
            "name": function_call["name"],
            "content": str(tool_response),  # 调用函数返回结果
        }

        history.append(t)
        return function_call["name"], tool_response

    else:
        return_message = response["choices"][0]["message"]
        reply = return_message["content"]

        history.append(return_message)
        logger.info(f"Final Reply: \n{reply}")

        return False, reply


def ask_llm(question,history, func_map=None, retry=3):
    response = get_response(question, history)

    function_call,result = deal_response(response, history, func_map)
    if function_call:
        if question in fix_questions_dict:
            if fix_questions_dict[question]['function'] in  no_reply_functions:
                reply = fix_questions_dict[question]["answer"]
                result = single_round(reply,
                                      "你是机器人服务员，请把以下句子换一种表述方式对顾客说，但是意思不变，尽量简短：\n")
            else:
                reply = fix_questions_dict[question]["answer"]
                result = single_round(f"你是机器人服务员，顾客想知道{question}, 你的具身场景查询返回的是{result},把返回的英文名词翻译成中文,请把按照以下句子对顾客说，{reply}, 尽量简短。\n")

            message = {'role': 'assistant', 'content': result, 'name': None,
                       'function_call': None}
            history.append(message)

        else:
            response = get_response(None, history,allow_function_call=False)
            _,result = deal_response(response, history, func_map)


    print(f'{len(history)}条历史记录:')
    for x in history:
        print(x)
    return function_call, result

if __name__ == "__main__":
    question = input("\n顾客：")
    history = new_history()
    n = 1
    max_retry = 2

    while question != 'end':
        function_call, return_message = ask_llm(question,history)


        question = input("\n顾客：")
