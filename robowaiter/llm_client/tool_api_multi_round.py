import json

import openai
from colorama import init, Fore
from loguru import logger
import json
from robowaiter.llm_client.tool_register import get_tools, dispatch_tool
import requests
import json

import urllib3
init(autoreset=True)

########################################
#   该文件实现了与大模型的通信以及工具调用
########################################

# 忽略https的安全性警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://45.125.46.134:25344" # 本地部署的地址,或者使用你访问模型的API地址

def get_response(**kwargs):
    data = kwargs

    response = requests.post(f"{base_url}/v1/chat/completions", json=data, stream=data["stream"], verify=False)
    decoded_line = response.json()
    return decoded_line

functions = get_tools()




if __name__ == "__main__":
    question = input("\n顾客：")
    data_memory = [{
            "role": "system",
            "content": "你是RoboWaiter,一个由HPCL团队开发的机器人服务员，你在咖啡厅工作。接受顾客的指令并调用工具函数来完成各种服务任务。",
        },]
    n = 1
    max_retry = 5
    params = dict(model="RoboWaiter",messages=data_memory, stream=False)
    params["functions"] = functions

    while question != 'end':
        user_dict = {"role": "user", "content": question}
        params["messages"].append(user_dict)

        # print(data_memory)
        response = get_response(**params)
        for _ in range(max_retry):
            if response["choices"][0]["message"].get("function_call"):
                function_call = response["choices"][0]["message"]["function_call"]
                logger.info(f"Function Call Response: {function_call}")

                function_args = json.loads(function_call["arguments"])
                tool_response = dispatch_tool(function_call["name"], function_args)
                logger.info(f"Tool Call Response: {tool_response}")

                return_message = response["choices"][0]["message"]
                params["messages"].append(return_message)
                t = {
                        "role": "function",
                        "name": function_call["name"],
                        "content": tool_response,  # 调用函数返回结果
                    }
                params["messages"].append(t)
                response = get_response(**params)

            else:
                return_message = response["choices"][0]["message"]
                reply = return_message["content"]
                params["messages"].append(return_message)
                logger.info(f"Final Reply: \n{reply}")
                break

        question = input("\n顾客：")
