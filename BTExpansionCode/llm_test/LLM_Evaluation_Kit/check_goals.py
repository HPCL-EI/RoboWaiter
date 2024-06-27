import time

from btpg.algos.llm_client.llms.ERNIE_Bot_4 import LLMERNIE
from sympy import to_dnf

import re

# 定义要拆分的多个字符
split_characters = r'[()&|]'  # 用正则表达式定义多个字符，包括逗号、句号、分号和感叹号等


predicate_list = ["Is","On"]
object_list = ["Chairs","Clean","Table1","Water"]


def format_check(result):
    try:
        goal_dnf = str(to_dnf(result, simplify=True))
    except:
        return False, None

    split_sentences = re.split(split_characters, result)
    split_sentences = [s.strip() for s in split_sentences if s.strip()]

    wrong_format_set = set()
    wrong_predicate_set = set()
    wrong_object_set = set()

    for sentence in split_sentences:
        if sentence == "": continue

        try:
            goal_dnf = str(to_dnf(sentence, simplify=True))
            # 格式正确
            word_list = sentence.split("_")
            if len(word_list) <=1:
                wrong_format_set.add(sentence)
                continue

            predicate = word_list[0]
            if predicate not in predicate_list:
                wrong_predicate_set.add(predicate)

            for object in word_list[1:]:
                if object not in object_list:
                    wrong_object_set.add(object)

        except:
            wrong_format_set.add(sentence)

    # print(wrong_format_set)
    # print(wrong_predicate_set)
    # print(wrong_object_set)
    if len(wrong_format_set) == 0  and \
            len(wrong_predicate_set) == 0 and\
            len(wrong_object_set) == 0:
        return True, None
    else:
        return False, [wrong_format_set,wrong_predicate_set,wrong_object_set]

def word_correct(sentence):
    try:
        goal_dnf = str(to_dnf(sentence, simplify=True))
        return True
    except:
        return False


def get_feedback_prompt(prompt,result,error_list):
    # wrong_format_set,wrong_predicate_set,wrong_object_set = error_list
    return prompt


# def get_feedback_prompt(prompt,result):
#     # split_sentences = re.split(split_characters, result)
#     # split_sentences = [s.strip() for s in split_sentences if s.strip()]
#     #
#     # wrong_format_set = set()
#     # wrong_predicate_set = set()
#     # wrong_object_set = set()
#     #
#     # for sentence in split_sentences:
#     #     if sentence == "": continue
#     #
#     #     try:
#     #         goal_dnf = str(to_dnf(sentence, simplify=True))
#     #         # 格式正确
#     #         word_list = sentence.split("_")
#     #         if len(word_list) <=1:
#     #             wrong_format_set.add(sentence)
#     #             continue
#     #
#     #         predicate = word_list[0]
#     #         if predicate not in predicate_list:
#     #             wrong_predicate_set.add(predicate)
#     #
#     #         for object in word_list[1:]:
#     #             if object not in object_list:
#     #                 wrong_object_set.add(object)
#     #
#     #     except:
#     #         wrong_format_set.add(sentence)
#     #
#     # print(wrong_format_set)
#     # print(wrong_predicate_set)
#     # print(wrong_object_set)


# a = "(On_S dfd oftdrink_Table3 & At_Chairs_Desk | & At_Chairs_Desk)"
# print(feedback(a))
#
#
#
# exit()



data_set_file = "easy.txt"
prompt_file = "prompt.txt"
test_num = 2


with open(data_set_file, 'r', encoding="utf-8") as f:
    data_set = f.read().strip()

with open(prompt_file, 'r', encoding="utf-8") as f:
    prompt = f.read().strip()

sections = re.split(r'\n\s*\n', data_set)
count = 0

llm = LLMERNIE()
question_list = []
correct_answer_list=  []
outputs_list = [[] for _ in range(len(sections))]

# 批量提交问题
for i,s in enumerate(sections[:test_num]) :
    x,y = s.strip().splitlines()
    x = x.strip()
    y = y.strip()
    # print(f"x: {x.strip()}, y: {y.strip()}")
    question_list.append(x)
    correct_answer_list.append(y)
    llm.ask(x,prompt=prompt,tag=i)



total_num = len(question_list)
finish_num = 0
SR = 0
GR = 0
while finish_num < total_num:
    result = llm.get_result()
    if result:
        # print(result)
        id,question,answer = result
        # print(correct_answer_list[id])
        outputs_list[id].append(answer)

        #如果不正确，且回答次数<5，则反馈

        format_correct,error_list = format_check(answer)

        if not format_correct:
            if len(outputs_list[id]) < 5:

                new_prompt = get_feedback_prompt(prompt,answer,error_list)
                llm.ask(question, prompt=prompt, tag=id)

                print(f"id: {id} Retry:{len(outputs_list[id])} A:{outputs_list[id]}, Q: {question}")
            else:
                finish_num += 1

        else:
            GR += 1

            correct = False
            if answer == correct_answer_list[id]:
                SR += 1
                correct = True
            # print(f"correct_num: {correct_num}")
            # print()
            finish_num += 1

            print(f"Correct:{correct} GR:{GR/finish_num} SR:{SR/finish_num} A:{outputs_list[id]}, Q: {question}")

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


