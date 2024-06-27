import time

import numpy as np

from mabtpg.algo.llm_client.llms.ERNIE_Bot_4 import LLMERNIE
from mabtpg.algo.llm_client.llms.gpt3 import LLMGPT3
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, Not, Or, And, to_dnf
from sympy import symbols, simplify_logic
import re
from sympy.logic.boolalg import Implies
from sympy import sympify
from mabtpg.algo.llm_client.dataset.data_process_check import format_check,word_correct,goal_transfer_ls_set
def print_green(text):
    """
    Prints the provided text in green color in the terminal.
    """
    green_color_code = '\033[92m'  # ANSI escape sequence for green color
    reset_color_code = '\033[0m'   # ANSI escape sequence to reset color to default
    print(f"{green_color_code}{text}{reset_color_code}")

def print_blue(text):
    """
    Prints the provided text in blue color in the terminal.
    """
    blue_color_code = '\033[94m'  # ANSI escape sequence for blue color
    reset_color_code = '\033[0m'  # ANSI escape sequence to reset color to default
    print(f"{blue_color_code}{text}{reset_color_code}")


def generate_prompt1(num_examples,diffculty):
    # Basic prompt structure
    prompt1 = """
[Condition Predicates]
RobotNear_<items_place>, On_<items>_<place>, Holding_<items>, Exists_<items>, Dirty_<furniture>, Active_<appliance>, Closed_<furnishing>, Low_<control>

[Objects]
<items>=['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk', 'VacuumCup', 'Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater', 'Apple', 'Banana', 'Mangosteen', 'Orange', 'Kettle', 'PaperCup', 'Bread', 'LunchBox', 'Teacup', 'Chocolate', 'Sandwiches', 'Mugs', 'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk', 'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup', 'Tissue', 'YogurtDrink', 'Newspaper', 'Box', 'PaperCupStarbucks', 'CoffeeMachine', 'Straw', 'Cake', 'Tray', 'Bread', 'Glass', 'Door', 'Mug', 'Machine', 'PackagedCoffee', 'CubeSugar', 'Apple', 'Spoon', 'Drinks', 'Drink', 'Ice', 'Saucer', 'TrashBin', 'Knife', 'Cube']
<place>=['Bar', 'Bar2', 'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3', 'WindowTable6', 'WindowTable4', 'WindowTable5', 'QuietTable7', 'QuietTable8', 'QuietTable9', 'ReadingNook', 'Entrance', 'Exit', 'LoungeArea', 'HighSeats', 'VIPLounge', 'MerchZone']
<items_place>=<items>+<place>
<furniture>=['Table1', 'Floor', 'Chairs']
<appliance>=['AC', 'TubeLight', 'HallLight']
<furnishing>=['Curtain']
<control>=['ACTemperature']
"""

    if diffculty=="easy":
        # Define the examples
        examples = [
            "Instruction: Would you be able to provide some chips at the third table?\nOn_Chips_Table3",
            "Instruction: Please close the curtains.\nClosed_Curtain",
            "Instruction: Please lower the air conditioning temperature.\nLow_ACTemperature",
            "Instruction: Please ensure the water is ready for service.\nExists_Water",
            "Instruction: It's a bit messy here, could you rearrange the chairs?\n~Dirty_Chairs"
        ]
    elif diffculty=="medium":
        # Define the examples
        examples = [
            "Instruction: Would you be able to provide some chips at the third table?\nOn_Chips_Table3",
            "Instruction: If the curtains are already closed or the AC is running, could you please grab me a hot milk?\n( Closed_Curtain | Active_AC ) & Holding_Milk",
            "Instruction: Please turn up the air conditioning and come to the bar counter.\nRobotNear_Bar & ~Low_ACTemperature",
            "Instruction: Please ensure the water is ready for service, and deliver the yogurt to table number one.\nExists_Water & On_Yogurt_Table1",
            "Instruction: It's a bit messy here, could you rearrange the chairs? And, if possible, could you bring me an apple or a banana to the reading nook?\n~Dirty_Chairs & ( On_Apple_ReadingNook | On_Banana_ReadingNook )"
        ]
    else:
        # Define the examples
        examples = [
            "Instruction: Would you be able to provide some chips at the third table?\nOn_Chips_Table3",
            "Instruction: If the curtains are already closed or the AC is running, could you please grab me a hot milk?\n( Closed_Curtain | Active_AC ) & Holding_Milk",
            "Instruction: Please turn up the air conditioning and come to the bar counter.\nRobotNear_Bar & ~Low_ACTemperature",
            "Instruction: Please ensure the water is ready for service, and deliver the yogurt to table number one.\nExists_Water & On_Yogurt_Table1",
            "Instruction: It's a bit messy here, could you rearrange the chairs? And, if possible, could you bring me an apple or a banana to the reading nook?\n~Dirty_Chairs & ( On_Apple_ReadingNook | On_Banana_ReadingNook )"
        ]

    # Add the desired number of examples
    if num_examples > 0:
        prompt1 += "\n\n [Few-shot Demonstrations]\n"
        prompt1 += "\n".join(examples[:num_examples])

    prompt1 += "\n[System]\n[Condition Predicates] Lists all predicates representing conditions and their optional parameter sets.\n[Objects] Lists all parameter sets.\n[Few-shot Demonstrations] Provide several examples of Instruction to Goal mapping."
    return prompt1



def get_feedback_prompt(error_list,error_black_set):

    error_message=""


    if error_list[0]!=None:
        error_message += "It contains syntax errors or illegal characters."
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

        error_message += f"\n[Syntax Blacklist] [{er_word0}]\n<Condition Predicate Blacklist> [{er_word1}]\n<Object Blacklist> [{er_word2}]\n"

        error_message += "\n[Additional Promot]\n"+\
    "1. Outputs including texts in the three blacklists are forbidden.\n"+\
    "2. If a word from [Object Blacklist] is encountered, choose the closest parameter from the [Objects] table to formulate the outputs.\n"+\
    "3. If a word from [Condition Predicate Blacklist] is encountered, choose the closest parameter from the [Condition Predicates] table to formulate the outputs.\n"+\
    "4. Please generate directly interpretable predicate formulas without any additional explanations."
    print("error_message:",error_message)

    return error_message


def evaluate_answer(correct_answer, user_answer):
    """
    Evaluate if the `correct_answer` is logically implied by the `user_answer`.
    This means that whenever the user_answer is true, the correct_answer must also be true.
    """
    # 将字符串表达式转换为 Sympy 可处理的逻辑表达式
    try:
        correct_expr = sympify(correct_answer)
        user_expr = sympify(user_answer)

        # 使用蕴含来判断，如果 user_expr 为真则 correct_expr 也应为真
        # Implies(a, b) 表示 a -> b。 如果 a -> b 总是真的，返回True
        is_implied = Implies(user_expr, correct_expr).simplify()

        # 如果蕴含关系总是为真，则表示 user_answer 包含了 correct_answer
        return is_implied
    except Exception as e:
        print(f"Error parsing expressions: {e}")
        return False
    # 你可以根据需要调整这个函数来评估答案的正确性
    # return correct_answer == user_answer


easy_data_set_file = "../dataset/easy_instr_goal.txt"
medium_data_set_file = "../dataset/medium_instr_goal.txt"
hard_data_set_file = "../dataset/hard_instr_goal.txt"

test_data_set_file = "../dataset/test.txt"

data_set_file = "../dataset/data100.txt"
prompt_file1 = "../dataset/prompt_test1.txt"
prompt_file2 = "../dataset/prompt_test2.txt"
test_num = 1


with open(easy_data_set_file, 'r', encoding="utf-8") as f:
    easy_data_set = f.read().strip()
with open(medium_data_set_file, 'r', encoding="utf-8") as f:
    medium_data_set = f.read().strip()
with open(hard_data_set_file, 'r', encoding="utf-8") as f:
    hard_data_set = f.read().strip()

data_set = easy_data_set
# data_set =hard_data_set
# data_set = easy_data_set + medium_data_set + hard_data_set

with open(prompt_file1, 'r', encoding="utf-8") as f:
    prompt1 = f.read().strip()
with open(prompt_file2, 'r', encoding="utf-8") as f:
    prompt2 = f.read().strip()


sections = re.split(r'\n\s*\n', data_set)
count = 0



# llm = LLMERNIE()
llm = LLMGPT3()


def evaluate_responses(prompt, sections):
    # 初始化结果字典，记录不同反馈次数下的语法和内容正确率
    results = {f'GA-{f}F': [] for f in range(6)}
    results.update({f'IA-{f}F': [] for f in range(6)})

    for i, s in enumerate(sections):
        x, y = s.strip().splitlines()
        question = x.strip()
        correct_answer = y.strip().replace("Goal: ", "")

        # 在主循环中维护错误黑名单的状态：
        error_black_set = [set(), set(), set()]
        feedback_time = 0

        while feedback_time <= 5:
            if feedback_time == 0:
                messages = [{"role": "user", "content": prompt + "\n" + question}]
            answer = llm.request(message=messages)
            messages.append({"role": "assistant", "content": answer})
            print_green(f"{feedback_time}th Answer: {answer}")

            grammar_correct, error_list = format_check(answer)
            if grammar_correct:
                content_correct = evaluate_answer(correct_answer, answer)
                # 一旦语法正确，标记所有后续反馈级别为正确
                for f in range(feedback_time, 6):
                    results[f'GA-{f}F'].append(1)  # 标记语法正确
                    results[f'IA-{f}F'].append(1 if content_correct else 0)
                break  # 退出循环，因为语法正确
            else:
                results[f'GA-{feedback_time}F'].append(0)
                results[f'IA-{feedback_time}F'].append(0)
                feedback_prompt = get_feedback_prompt(error_list, error_black_set)
                messages.append({"role": "user", "content": feedback_prompt})

            feedback_time += 1

    return results

# 假设 data_set 已经被定义并加载
sections = re.split(r'\n\s*\n', data_set)[:]

# 示例评估循环
num_examples = [0, 1, 5]
results_table = []

for num in num_examples:
    feedback_type = "Zero-shot" if num == 0 else f"Few-shot {num}"
    print_blue(f'=============== Feedback Level {feedback_type} ==============')

    prompt = generate_prompt1(num) + prompt2  # 假设这个函数根据 num_examples 生成合适的提示
    evaluation_results = evaluate_responses(prompt, sections)

    # 筛选并计算特定反馈级别下的平均正确率
    filtered_keys = ['GA-0F', 'GA-1F', 'GA-5F', 'IA-0F', 'IA-1F', 'IA-5F']
    row = {key: f'{key}: {np.mean(evaluation_results[key]):.2%}' for key in filtered_keys if key in evaluation_results}
    results_table.append(row)

# 输出结果表
for index, row in enumerate(results_table):
    feedback_type = "Zero-shot" if num_examples[index] == 0 else f"Few-shot {num_examples[index]}"
    print(f'{feedback_type}:', ', '.join(row.values()))
    print("\n")