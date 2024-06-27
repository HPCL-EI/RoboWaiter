import time
import csv

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


def print_yellow(text):
    """
    Prints the provided text in yellow color in the terminal.
    """
    yellow_color_code = '\033[93m'  # ANSI escape sequence for yellow color
    reset_color_code = '\033[0m'   # ANSI escape sequence to reset color to default
    print(f"{yellow_color_code}{text}{reset_color_code}")

def print_status(grammar_correct, content_correct):
    """
    Prints 'Grammar_correct' and 'Content_correct' in green if true, red if false.
    """
    green_color = '\033[92m'
    red_color = '\033[91m'
    reset_color = '\033[0m'

    # Determine the color based on the boolean value for grammar_correct
    grammar_color = green_color if grammar_correct else red_color
    content_color = green_color if content_correct else red_color

    # Print with the appropriate colors
    print(f"{grammar_color}Grammar_correct: {grammar_correct}{reset_color} "
          f"{content_color}Content_correct: {content_correct}{reset_color}")

def print_orange(text):
    """
    Prints the provided text in orange color in the terminal.
    """
    orange_color_code = '\033[38;2;255;165;0m'  # RGB escape sequence for orange color
    reset_color_code = '\033[0m'  # ANSI escape sequence to reset color to default
    print(f"{orange_color_code}{text}{reset_color_code}")


def generate_prompt1(num_examples,diffculty):
    # Basic prompt structure
    prompt1 = """
[Condition Predicates]
RobotNear_<items_place>, On_<items>_<place>, Holding_<items>, Exists_<items>, IsClean_<furniture>, Active_<appliance>, Closed_<furnishing>, Low_<control>

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
            "Instruction: It's a bit messy here, could you rearrange the chairs?\nIsClean_Chairs"
        ]
    elif diffculty=="medium":
        # Define the examples
        examples = [
            "Instruction: Would you be able to provide some chips at the third table?\nOn_Chips_Table3",
            "Instruction: If the curtains are already closed or the AC is running?\nClosed_Curtain | Active_AC",
            "Instruction: Please lower the air conditioning temperature and come to the bar counter.\nRobotNear_Bar & Low_ACTemperature",
            "Instruction: Please ensure the water is ready for service, and deliver the yogurt to table number one.\nExists_Water & On_Yogurt_Table1",
            "Instruction: It's a bit messy here, could you rearrange the chairs? And, if possible, could you bring me an apple to the reading nook?\nIsClean_Chairs & On_Apple_ReadingNook"
        ]
    else:
        # Define the examples
        examples = [
            "Instruction: Would you be able to provide some chips at the third table?\nOn_Chips_Table3",
            "Instruction: If the curtains are already closed or the AC is running, could you please grab me a hot milk?\n( Closed_Curtain | Active_AC ) & Holding_Milk",
            "Instruction: Please turn up the air conditioning and come to the bar counter.\nRobotNear_Bar & ~Low_ACTemperature",
            "Instruction: Please ensure the water is ready for service, and deliver the yogurt to table number one.\nExists_Water & On_Yogurt_Table1",
            "Instruction: It's a bit messy here, could you rearrange the chairs? And, if possible, could you bring me an apple or a banana to the reading nook?\nIsClean_Chairs & ( On_Apple_ReadingNook | On_Banana_ReadingNook )"
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

        error_message += f"\n[Syntax Blacklist] {er_word0}\n[]Condition Predicate Blacklist] {er_word1}\n[Object Blacklist] {er_word2}\n"

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

    if correct_answer==user_answer:
        return True

    # 将字符串表达式转换为 Sympy 可处理的逻辑表达式
    try:
        # 将字符串表达式转换为 Sympy 可处理的逻辑表达式
        correct_expr = sympify(correct_answer)
        user_expr = sympify(user_answer)
        # Simplify both expressions to their logical forms
        correct_dnf = simplify_logic(correct_expr, form='dnf')
        user_dnf = simplify_logic(user_expr, form='dnf')

        # Check if user answer implies correct answer
        is_contained = Implies(user_dnf, correct_dnf).simplify()  # Should be user implies correct

        # Check if the implication is always true
        return is_contained

    except Exception as e:
        print(f"Error parsing expressions: {e}")
        return False
    # 你可以根据需要调整这个函数来评估答案的正确性
    # return correct_answer == user_answer




def evaluate_responses_and_save_to_csv(prompt, sections, csv_filename):
    results = {f'GA-{f}F': [] for f in range(6)}
    results.update({f'IA-{f}F': [] for f in range(6)})

    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 初始化CSV文件，写入标题行。因为列数是动态的，可以省略列标题或仅写入固定的标题
        writer.writerow(['Instruction', 'Goal', 'Feedback Details'])

        for i, s in enumerate(sections):
            x, y = s.strip().splitlines()
            question = x.strip()
            correct_answer = y.strip().replace("Goal: ", "")
            print_orange(f"correct_answer: {correct_answer}")

            error_black_set = [set(), set(), set()]
            feedback_details = []

            for feedback_time in range(6):
                messages = [{"role": "user", "content": prompt + "\n" + question}]
                answer = llm.request(message=messages)
                messages.append({"role": "assistant", "content": answer})
                print_yellow(f"{feedback_time}th Answer: {answer} question:{question}")

                grammar_correct, error_list = format_check(answer)
                content_correct = False
                error_message = ""

                if grammar_correct:
                    content_correct = evaluate_answer(correct_answer, answer)
                    # 一旦语法正确，标记所有后续反馈级别为正确
                    for f in range(feedback_time, 6):
                        results[f'GA-{f}F'].append(1)  # 标记语法正确
                        results[f'IA-{f}F'].append(1 if content_correct else 0)
                    break  # 退出循环，因为语法正确
                else:
                    error_message = get_feedback_prompt(error_list, error_black_set)
                    feedback_prompt = error_message
                    messages.append({"role": "user", "content": feedback_prompt})

                # 累积每次反馈的结果到一个列表
                feedback_details.append(f"{feedback_time}F: {answer} (Error: {error_message})")

                # 更新结果
                content_correct = evaluate_answer(correct_answer, answer)
                results[f'GA-{feedback_time}F'].append(1 if grammar_correct else 0)
                results[f'IA-{feedback_time}F'].append(1 if content_correct else 0)

                if grammar_correct and content_correct:
                    break  # 如果答案正确，不需要更多反馈

            # 一次性将问题、答案及所有反馈写入一行
            writer.writerow([question, correct_answer, '; '.join(feedback_details)])
            print_status(grammar_correct, content_correct)

    return results



easy_data_set_file = "../dataset/easy_instr_goal.txt"
medium_data_set_file = "../dataset/medium_instr_goal.txt"
hard_data_set_file = "../dataset/hard_instr_goal.txt"

test_data_set_file = "../dataset/test.txt"

data_set_file = "../dataset/data100.txt"
prompt_file1 = "../dataset/prompt_test1.txt"
prompt_file2 = "../dataset/prompt_test2.txt"

with open(easy_data_set_file, 'r', encoding="utf-8") as f:
    easy_data_set = f.read().strip()
with open(medium_data_set_file, 'r', encoding="utf-8") as f:
    medium_data_set = f.read().strip()
with open(hard_data_set_file, 'r', encoding="utf-8") as f:
    hard_data_set = f.read().strip()

# data_set =hard_data_set
# data_set = easy_data_set + medium_data_set + hard_data_set

with open(prompt_file1, 'r', encoding="utf-8") as f:
    prompt1 = f.read().strip()
with open(prompt_file2, 'r', encoding="utf-8") as f:
    prompt2 = f.read().strip()





# llm = LLMERNIE()
llm = LLMGPT3()
# for diffculty in ["easy", "medium", "hard"]:
for diffculty in ["hard"]:
    print_blue(f"-----------------------{diffculty}-------------------------")

    # 使用示例
    csv_filename = f"evaluation_results_{diffculty}.csv"

    if diffculty == "easy":
        data_set = easy_data_set
    elif diffculty == "medium":
        data_set = medium_data_set
    elif diffculty == "hard":
        data_set = hard_data_set

    sections = re.split(r'\n\s*\n', data_set)[:3]
    num_examples = [0, 1, 5]
    results_table = []

    for num in num_examples:
        feedback_type = "Zero-shot" if num == 0 else f"Few-shot {num}"
        print_blue(f'=============== Feedback Level {feedback_type} ===============')

        prompt = generate_prompt1(num,diffculty) + prompt2
        evaluation_results = evaluate_responses_and_save_to_csv(prompt, sections, csv_filename)

        filtered_keys = ['GA-0F', 'GA-1F', 'GA-5F', 'IA-0F', 'IA-1F', 'IA-5F']
        row = {key: f'{key}: {np.mean(evaluation_results[key]):.2%}' for key in filtered_keys if key in evaluation_results}
        results_table.append(row)

    for index, row in enumerate(results_table):
        feedback_type = "Zero-shot" if num_examples[index] == 0 else f"Few-shot {num_examples[index]}"
        print(f'{feedback_type}:', ', '.join(row.values()))
        print("\n")