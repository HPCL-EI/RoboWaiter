import time

import numpy as np

from llm_test.ERNIE_Bot_4 import LLMERNIE
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, Not, Or, And, to_dnf
from sympy import symbols, simplify_logic
import re
from dataset.data_process_check import format_check,word_correct,goal_transfer_ls_set

def get_feedback_prompt_last(id,prompt,result,error_list,error_black_set):
    # wrong_format_set,wrong_predicate_set,wrong_object_set = error_list

    error_message=""


    if error_list[0]!=None:
        error_message += "It contains syntax errors or illegal characters."
            # ("It Contains syntax errors or illegal characters that cannot be converted to disjunctive normal form (DNF) using sympy.to_dnf. ")
                          # "Please check the syntax in your input and ensure there are no prohibited characters. The answer should consist only of ~, |, &, and the given [Condition] and  [Object].. ")
    else:
        if error_list[1]!=set():
            # error_strings = ", ".join(error_list[1])
            # error_message += f"\"{error_strings}\" have format errors. They should consist only of ~, |, &, and the given [Condition] and  [Object].\n"
            error_black_set[0] |= set(error_list[1])
        if error_list[2]!=set():
            # error_strings = ", ".join(error_list[2])
            # error_message +=  f"\"{error_strings}\" are not in [Condition]. Please select the closest predicates from the [Condition] table to form the answer.\n"
            error_black_set[1] |= set(error_list[2])
        if error_list[3]!=set():
            # error_strings = ", ".join(error_list[3])
            # error_message +=  f"\"{error_strings}\" are not in [Object]. Please select the closest parameter from the [Object] table to form the answer.\n"
            error_black_set[2] |= set(error_list[3])

    # error_strings = "Do not include: "+", ".join(list(error_black_set))+"." +"Please select the closest parameter from the [Condition] and [Object] table to form the answer."

    er_word0 = ", ".join(list(error_black_set[0]))
    er_word1 = ", ".join(list(error_black_set[1]))
    er_word2 = ", ".join(list(error_black_set[2]))

    error_message += f"\"{er_word0}\" have format errors. The answer should consist only of ~, |, &, and the given [Condition] and  [Object].\n"
    error_message += f"\"{er_word1}\" are not in [Condition]. Please select the closest predicates from the [Condition] table to form the answer.\n"
    error_message += f"\"{er_word2}\" are not in [Object]. Please select the closest parameter from the [Object] table to form the answer.\n"


    print("** Error_message: ",error_message)
    prompt += "\n"+ error_message
    return prompt

def get_feedback_prompt0123(id,prompt,result,error_list,error_black_set):
    # wrong_format_set,wrong_predicate_set,wrong_object_set = error_list

    error_message=""

    if error_list[0]!=None:
        error_message += "It contains syntax errors or illegal characters."
    else:
        if error_list[1]!=set():
            error_black_set[0] |= set(error_list[1])
            er_word0 = ", ".join(list(error_black_set[0]))
            error_message += f"\"{er_word0}\" have format errors. The answer should consist only of ~, |, &, and the given [Condition] and  [Object].\n"

        if error_list[2]!=set():
            error_black_set[1] |= set(error_list[2])
            er_word1 = ", ".join(list(error_black_set[1]))
            error_message += f"\"{er_word1}\" are not in [Condition]. Please select the closest predicates from the [Condition] table to form the answer.\n"

        if error_list[3]!=set():
            error_black_set[2] |= set(error_list[3])
            er_word2 = ", ".join(list(error_black_set[2]))
            error_message += f"\"{er_word2}\" are not in [Object]. Please select the closest parameter from the [Object] table to form the answer.\n"

    print("** Error_message: ",error_message)
    prompt += "\n"+ error_message
    return prompt




def get_feedback_prompt(id,prompt1,prompt2,question,result,error_list,error_black_set):

    error_message=""
    er_word0=""
    er_word1=""
    er_word2=""

    if error_list[0]!=None:
        error_message = ""
    else:
        if error_list[1]!=set():
            error_black_set[0] |= set(error_list[1])

        if error_list[2]!=set():
            error_black_set[1] |= set(error_list[2])

        if error_list[3]!=set():
            error_black_set[2] |= set(error_list[3])

        er_word0 = ", ".join(list(error_black_set[0]))
        er_word1 = ", ".join(list(error_black_set[1]))
        er_word2 = ", ".join(list(error_black_set[2]))

        error_message += f"\n[Blacklist]\n<Illegal Condition>=[{er_word1}]\n<Illegal Object>=[{er_word2}]\n<Other Illegal Words or Characters>=[{er_word0}]\n"
        error_message += "\n[Blacklist] Contains restricted elements.\n"+\
    "If a word from <Illegal Condition> is encountered, choose the nearest parameter with a similar meaning from the [Condition] table to formulate the answer.\n"+\
    "If a word from <Illegal Object> is encountered, choose the nearest parameter with a similar meaning from the [Object] table to formulate the answer."

    print("** Blacklist: ",f"[Blacklist]\n<Illegal Characters>=[{er_word0}]\n<Illegal Condition>=[{er_word1}]\n<Illegal Object>=[{er_word2}]")

    # prompt = prompt1+prompt2+error_message
    # prompt = error_message
    # print(prompt)
    prompt = prompt1+prompt2
    # prompt+= question + result
    prompt += error_message
    print(error_message)
    return prompt




# data_set_file = "easy.txt"

easy_data_set_file = "../dataset/easy_instr_goal.txt"
medium_data_set_file = "../dataset/medium_instr_goal.txt"
hard_data_set_file = "../dataset/hard_instr_goal.txt"

test_data_set_file = "../dataset/test.txt"

data_set_file = "../dataset/data100.txt"
prompt_file1 = "prompt_test1.txt"
prompt_file2 = "prompt_test2.txt"
# prompt_file1 = "prompt1.txt"
# prompt_file2 = "prompt2.txt"
test_num = 1


with open(easy_data_set_file, 'r', encoding="utf-8") as f:
    easy_data_set = f.read().strip()
with open(medium_data_set_file, 'r', encoding="utf-8") as f:
    medium_data_set = f.read().strip()
with open(hard_data_set_file, 'r', encoding="utf-8") as f:
    hard_data_set = f.read().strip()
# with open(data_set_file, 'r', encoding="utf-8") as f:
#     data_set = f.read().strip()

# easy_sections = re.split(r'\n\s*\n', easy_data_set)
# print("easy:",len(easy_sections))
# medium_sections = re.split(r'\n\s*\n', medium_data_set)
# print("medium:",len(medium_sections))
# hard_sections = re.split(r'\n\s*\n', hard_data_set)
# print("hard:",len(hard_sections))
# data_set = easy_data_set & medium_data_set
# print(data_set)

with open(test_data_set_file, 'r', encoding="utf-8") as f:
    test_data_set = f.read().strip()
data_set = test_data_set
# data_set =hard_data_set

# data_set = easy_data_set + medium_data_set + hard_data_set

with open(prompt_file1, 'r', encoding="utf-8") as f:
    prompt1 = f.read().strip()
with open(prompt_file2, 'r', encoding="utf-8") as f:
    prompt2 = f.read().strip()

prompt = prompt1+prompt2

sections = re.split(r'\n\s*\n', data_set)
# print("data_set:",len(sections))
count = 0



llm = LLMERNIE()
question_list = []
correct_answer_list = []
correct_answer_ls_set = []
outputs_list = [[] for _ in range(len(sections))]


# 批量提交问题
# for i,s in enumerate(sections[:test_num]):
for i, s in enumerate(sections):
    x, y = s.strip().splitlines()
    x = x.strip()
    y = y.strip().replace("Goal: ", "")
    # print(f"x: {x.strip()}, y: {y.strip()}")
    question_list.append(x)
    correct_answer_list.append(y)
    correct_answer_ls_set.append(goal_transfer_ls_set(y))
    llm.ask(x, prompt=prompt, tag=i)

total_num = len(question_list)

error_black_ls = [[set(),set(),set()] for _ in range(total_num)]



try_times = 1
# total_GR_ls = np.zeros(5)
total_GR_ls=[]
total_SR_ls = []
total_GCR_ls = []

# for time in range(try_times):
finish_num = 0
SR = 0
GR = 0
GCR = 0
# 统计语法正确的数量
GR_ls=np.zeros(6)

while finish_num < total_num:
    result = llm.get_result()

    if result:
        # print(result)
        id,question,answer = result
        # print(correct_answer_list[id])
        outputs_list[id].append(answer)

        #如果不正确，且回答次数<5，则反馈
        answer = "(On_Juice_Table6 | ~Exist_Juice=>On_Coffee_Table6 ) & ( ~Low_AC | Open_Curtain )"
        format_correct,error_list = format_check(answer)
        print("error_list:",error_list)

        print(f"===== id:{id}   Q: {question} =====")

        if not format_correct:
            if len(outputs_list[id]) < 6:
                print("*** answer:",answer)
                # new_prompt = get_feedback_prompt(id,prompt1,prompt2,answer,error_list,error_black_ls[id])

                new_prompt = get_feedback_prompt(id, prompt1,prompt2, question_list[id],answer, error_list, error_black_ls[id])
                llm.ask(question, prompt=new_prompt, tag=id)
                # llm.ask(question, prompt=prompt, tag=id)
                print(f"   Retry:{len(outputs_list[id])} A:{outputs_list[id]}")
                # print(f"id: {id} Retry:{len(outputs_list[id])} A:{outputs_list[id]}, Q: {question}")
            else:
                finish_num += 1
                print(f"A:  {outputs_list[id]}")
                print(f"CA: {correct_answer_list[id]}")
                GR_r = GR_ls / finish_num
                gr_s = 0
                for i in range(len(GR_r)):
                    gr_s += GR_r[i]
                    GR_r[i] = gr_s
                print(f"Correct:False GR:{GR_r[0],GR_r[1],GR_r[-1]} SR:{SR / finish_num} GCR:{GCR / finish_num}")

        else:
            GR_ls[len(outputs_list[id])-1] += 1

            correct = False
            answer_ls_set = goal_transfer_ls_set(answer)


            if answer_ls_set == correct_answer_ls_set[id]:
                SR += 1
                GCR+=1
                correct = True
            else:
                GCR += len([a_set for a_set in answer_ls_set if a_set in correct_answer_ls_set[id]])*1.0/len(correct_answer_ls_set[id])


                # GCR += len(answer_ls_set-correct_answer_ls_set)*1.0/len(correct_answer_ls_set)

            # print(f"correct_num: {correct_num}")
            # print()
            finish_num += 1

            # print(f"Correct:{correct} GR:{GR/finish_num} SR:{SR/finish_num} A:{outputs_list[id]}, Q: {question}")
            # print("id=",id,"answer:", answer, " == correct_answer_list[id]:", correct_answer_list[id])
            print(f"A:  {outputs_list[id]}")
            print(f"CA: {correct_answer_list[id]}")
            GR_r = GR_ls/finish_num
            gr_s=0
            for i in range(len(GR_r)):
                gr_s+=GR_r[i]
                GR_r[i] = gr_s
            print(f"Correct:{correct} GR:{GR_r[0],GR_r[1],GR_r[-1]} SR:{SR/finish_num} GCR:{GCR/finish_num}")

            total_GR_ls.append(GR_ls)
            total_SR_ls.append(SR)
            total_GCR_ls.append(GCR)

    else:
        time.sleep(0.01)

llm.close()
# print(f"result: {result}")
# print(f"y: {y}")
# print(f"count: {count}")
# print()
#
# if result == y:
#     count += 1

# print("GR =:", round(np.mean(total_GR_ls), 4), "std=", round(np.std(total_GR_ls), 4))
# print("SR = ", round(np.mean(total_SR_ls), 3), "std=", round(np.std(total_SR_ls, ddof=1), 3))
# print("GCR = :", round(np.mean(total_GCR_ls), 3), "std=", round(np.std(total_GCR_ls, ddof=1), 3))

