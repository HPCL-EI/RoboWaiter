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

def run_conversation(query: str, stream=False,  max_retry=5):
    params = dict(model="chatglm3", messages=[{"role": "user", "content": query}], stream=stream)
    params["functions"] = functions
    response = get_response(**params)

    for _ in range(max_retry):
        if response["choices"][0]["message"].get("function_call"):
            function_call = response["choices"][0]["message"]["function_call"]
            logger.info(f"Function Call Response: {function_call}")
            if "sub_task" in function_call["name"]:
                return {
                    "Answer": "好的",
                    "Goal": json.loads(function_call["arguments"])["goal"]
                }

            function_args = json.loads(function_call["arguments"])
            tool_response = dispatch_tool(function_call["name"], function_args)
            logger.info(f"Tool Call Response: {tool_response}")

            params["messages"].append(response["choices"][0]["message"])
            params["messages"].append(
                {
                    "role": "function",
                    "name": function_call["name"],
                    "content": tool_response,  # 调用函数返回结果
                }
            )
        else:
            reply = response["choices"][0]["message"]["content"]
            return {
                "Answer": reply,
                "Goal": None
            }
            logger.info(f"Final Reply: \n{reply}")
            return

        response = get_response(**params)



if __name__ == "__main__":
    query = "可以带我去吗"
    print(run_conversation(query, stream=False))
