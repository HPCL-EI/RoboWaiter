import requests
import urllib3

########################################
#   该文件实现了与大模型的简单通信
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
	response = requests.post(url, headers=headers, json={"messages":data_memory, "repetition_penalty": 1.0}, verify=False)
	answer=response.json()['choices'][n]['message']['content']
	print(answer)
	assistant_dict={"role": "assistant","content":answer}
	data_memory.append(assistant_dict)
	n=n+2
	k=input()