import requests
import urllib3
from robowaiter.llm_client.tool_api import run_conversation
########################################
#   该文件实现了与大模型的简单通信、多轮对话，输入end表示对话结束
########################################

# 忽略https的安全性警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://45.125.46.134:25344/v1/chat/completions"
headers = {"Content-Type": "application/json"}

#在这里输入你的问题
k=input()
data_memory=[]
n=1
while k!='end':
	question_now=k
	user_dict={"role": "user","content":question_now}
	data_memory.append(user_dict)
	#print(data_memory)
	response = run_conversation(str(data_memory))
	answer=str(response)
	print(answer)
	assistant_dict={"role": "assistant","content":answer}
	data_memory.append(assistant_dict)
	n=n+2
	k=input()
