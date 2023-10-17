import tiktoken
import random
import requests
import time
import json
import concurrent.futures
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OPENAI_API_KEY = open('openai_api_key.txt', 'r').read().split('\n')


def get_tokens_num(text, model):
    encoding = tiktoken.encoding_for_model(model)
    tokens_num = len(encoding.encode(text))
    return tokens_num


def get_chatgpt(user, system='', question='', model='gpt-3.5-turbo-16k-0613', temperature=1.0, max_tokens=2048,
                top_p=0.8,
                frequency_penalty=0.0, presence_penalty=0.0):
    try_count = 0
    while try_count < 20:
        key_choice = random.choice(OPENAI_API_KEY)
        url = r'https://api.openai.com/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + key_choice,
        }
        try:
            prompt = {
                'model': model,
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': user}
                ],
                'temperature': temperature,
                'max_tokens': max_tokens,
                'top_p': top_p,
                'frequency_penalty': frequency_penalty,
                'presence_penalty': presence_penalty
            }
            resp = requests.post(url, json=prompt, headers=headers, verify=False, timeout=60)
            answer = json.loads(resp.text)
            if 'choices' in answer:
                result = answer['choices'][0]['message']['content']
            else:
                time.sleep(1)
                continue
            if result == '':
                time.sleep(1)
                continue
            else:
                if question:
                    return {'question': question, 'answer': result}
                else:
                    return {'system': system, 'user': user, 'answer': result}
        except Exception as e:
            print(key_choice + ': query request failed \n' + str(e))
            print('retrying...')
            try_count += 1
            time.sleep(1)


def get_chatgpt_concurrent(user_input, system_input, question_input, model='gpt-3.5-turbo-16k-0613', temperature=1.0,
                           max_tokens=2048,
                           top_p=0.8,
                           frequency_penalty=0.0, presence_penalty=0.0):
    work_count = 0
    result = []
    print('Query size is ' + str(len(user_input)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(get_chatgpt, user, system, question, model, temperature, max_tokens, top_p,
                                   frequency_penalty,
                                   presence_penalty) for user, system, question in
                   zip(user_input, system_input, question_input)]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                result.append(future.result())
            work_count += 1
            print(str(work_count) + '/' + str(len(user_input)) + ' finished')
    return result
