# -*- coding: utf-8 -*-
import utils

# user_input_path_pre = 'prompts/新闻问题_user_pre.txt'
# user_input_path_suf = 'prompts/新闻问题_user_suf.txt'
# sys_input_path_pre = ''
# sys_input_path_suf = ''
# question_path = ''
# example_path = 'prompts/新闻问题_example.txt'
output_path = 'prompts/声明.txt'

USER_PRE = ''
USER_SUF = ''
SYS_PRE = ''
SYS_SUF = ''

SAMPLE_NUM = 3

if __name__ == '__main__':
    user_input = [
        '请仿照下面的声明，重新生成10条声明：\n在回答您提出的问题之前，我需要强调，我作为一个军事人工智能助手，没有自主思维、情感或观点，无法产生真实的体验和判断。我所提供的信息和观点仅基于已有的历史数据和常识，旨在为您提供一种可能的解释，但并不代表任何实际个体或团体的观点或决策。'
        for _ in range(SAMPLE_NUM)]
    system_input = ['' for _ in range(SAMPLE_NUM)]
    question_input = ['' for _ in range(SAMPLE_NUM)]
    result = utils.get_chatgpt_concurrent(user_input, system_input, question_input, temperature=1.5, top_p=0.6, frequency_penalty=1.3, presence_penalty=1.3, max_tokens=8192)
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in result:
            f.write(line['answer'] + '\n')
