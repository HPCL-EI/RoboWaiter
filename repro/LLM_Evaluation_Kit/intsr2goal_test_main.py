import csv
import re
import numpy as np
import concurrent.futures
from itertools import chain

from LLM.llms.gpt3 import LLMGPT3
from LLM.dataset.data_process_check import format_check, goal_transfer_ls_set


def init_csv(filename, max_feedbacks=5):
    """Initialize a CSV file and write the header row, which includes multiple outputs and feedbacks."""
    headers = ['ID', 'Instruction', 'Correct Goal']
    for i in range(max_feedbacks + 1):
        headers.append(f'Model Output {i + 1}')
        if i < max_feedbacks:
            headers.append(f'Feedback Given {i + 1}')
    headers.extend(['Feedback Count', 'Grammar Correct', 'Content Correct'])
    print("headers:", headers)
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)


def append_to_csv(filename, data):
    """Append a row of data to the CSV file."""
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def print_colored(text,color):
    color_code = '\033[0m'
    if color=="grean":
        color_code = '\033[92m'
    elif color=="blue":
        color_code = '\033[94m'
    elif color=="yellow":
        color_code = '\033[93m'
    elif color=="orange":
        color_code = '\033[38;2;255;165;0m'
    elif color=="red":
        color_code = '\033[91m'
    reset_color_code = '\033[0m'  # ANSI escape sequence to reset color to default
    print(f"{color_code}{text}{reset_color_code}")


def print_status(grammar_correct, content_correct):
    """Prints 'Grammar_correct' and 'Content_correct' in green if true, red if false."""
    green_color = '\033[92m'
    red_color = '\033[91m'
    reset_color = '\033[0m'

    # Determine the color based on the boolean value for grammar_correct
    grammar_color = green_color if grammar_correct else red_color
    content_color = green_color if content_correct else red_color

    # Print with the appropriate colors
    print(f"{grammar_color}Grammar_correct: {grammar_correct}{reset_color} "
          f"{content_color}Content_correct: {content_correct}{reset_color}")


def generate_prompt1(num_examples, diffculty):
    """Generate a prompt based on the number of examples and the difficulty level."""
    prompt1 = """
        [Condition Predicates]
        RobotNear_<items_place>, On_<items>_<place>, Holding_<items>, Exists_<makable>, IsClean_<furniture>, Active_<appliance>, Closed_<furnishing>, Low_<control>
        
        [Objects]
        <items>=['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk', 'VacuumCup', 'Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater', 'Apple', 'Banana', 'Mangosteen', 'Orange', 'Kettle', 'PaperCup', 'Bread', 'LunchBox', 'Teacup', 'Chocolate', 'Sandwiches', 'Mugs', 'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk', 'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup', 'Tissue', 'YogurtDrink', 'Newspaper', 'Box', 'PaperCupStarbucks', 'CoffeeMachine', 'Straw', 'Cake', 'Tray', 'Bread', 'Glass', 'Door', 'Mug', 'Machine', 'PackagedCoffee', 'CubeSugar', 'Apple', 'Spoon', 'Drinks', 'Drink', 'Ice', 'Saucer', 'TrashBin', 'Knife', 'Cube']
        <place>=['Bar', 'Bar2', 'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3', 'WindowTable6', 'WindowTable4', 'WindowTable5', 'QuietTable7', 'QuietTable8', 'QuietTable9', 'ReadingNook', 'Entrance', 'Exit', 'LoungeArea', 'HighSeats', 'VIPLounge', 'MerchZone']
        <makable>=['Coffee', 'Water', 'Dessert']
        <items_place>=<items>+<place>
        <furniture>=['Table1', 'Floor', 'Chairs']
        <appliance>=['AC', 'TubeLight', 'HallLight']
        <furnishing>=['Curtain']
        <control>=['ACTemperature']
        """
    if diffculty == "easy":
        # Define the examples
        examples = [
            "Instruction: Would you be able to provide some chips at the third table?\nOn_Chips_Table3",
            "Instruction: Please close the curtains.\nClosed_Curtain",
            "Instruction: Could you turn on the air conditioning, please?\nActive_AC",
            "Instruction: Please ensure the water is ready for service.\nExists_Water",
            "Instruction: It's a bit messy here, could you rearrange the chairs?\nIsClean_Chairs"
        ]
    elif diffculty == "medium":
        # Define the examples
        examples = [
            "Instruction: Could you bring some chips to table three, please? Also, it's quite warm here, so could you turn on the air conditioner? \nOn_Chips_Table3 & Active_AC",
            # "Instruction: Could you please bring some chips to either the third table or the second table?.\nOn_Chips_Table3 | On_Chips_Table2",
            "Instruction: If the curtains are already closed or the AC is running?\nClosed_Curtain | Active_AC",
            "Instruction: Please lower the air conditioning temperature and come to the bar counter.\nRobotNear_Bar & Low_ACTemperature",
            "Instruction: Please prepare some waters, and deliver the yogurt to table number one.\nExists_Water & On_Yogurt_Table1",
            "Instruction: It's a bit messy here, could you rearrange the chairs? And, if possible, could you bring me an apple to the reading nook?\nIsClean_Chairs & On_Apple_ReadingNook"
        ]
    else:
        # Define the examples
        examples = [
            "Instruction: Could you please bring some chips to either the third table or the second table? And also, don't forget to turn off the air conditioner, it's too cold.\n(On_Chips_Table3 | On_Chips_Table2)& ~Active_AC",
            "Instruction: If the curtains are already closed or the AC is running, can you also make sure the floor is clean?\n(Closed_Curtain | Active_AC) & IsClean_Floor",
            "Instruction: Please turn up the air conditioning, come to the bar counter, and check if there is any yogurt available.\nRobotNear_Bar & ~Low_ACTemperature & Exists_Yogurt",
            "Instruction: Please ensure the water is ready for service, deliver the yogurt to table number one, and turn on the tube light.\nExists_Water & On_Yogurt_Table1 & Active_TubeLight",
            "Instruction: It's a bit messy here, could you rearrange the chairs? And, if possible, could you deliver an apple or a banana to the bar?\nIsClean_Chairs & ( On_Apple_Bar | On_Banana_Bar )"
        ]
    # examples = [
    #     "Instruction: Would you be able to provide some chips at the third table?\nOn_Chips_Table3",
    #     "Instruction: If the curtains are already closed or the AC is running?\nClosed_Curtain | Active_AC",
    #     "Instruction: Please ensure the water is ready for service, and deliver the yogurt to table number one.\nExists_Water & On_Yogurt_Table1",
    #     "Instruction: Please turn up the air conditioning, come to the bar counter, and check if there is any yogurt available.\nRobotNear_Bar & ~Low_ACTemperature & Exists_Yogurt",
    #     "Instruction: It's a bit messy here, could you rearrange the chairs? And, if possible, could you deliver an apple or a banana to the bar?\nIsClean_Chairs & ( On_Apple_Bar | On_Banana_Bar )"
    # ]

    # Add the desired number of examples
    if num_examples > 0:
        prompt1 += "\n\n [Few-shot Demonstrations]\n"
        prompt1 += "\n".join(examples[:num_examples])

    prompt1 += "\n[System]\n[Condition Predicates] Lists all predicates representing conditions and their optional parameter sets.\n[Objects] Lists all parameter sets.\n[Few-shot Demonstrations] Provide several examples of Instruction to Goal mapping."
    return prompt1


def get_feedback_prompt(error_list, error_black_set):
    error_message = ""

    if error_list[0] != None:
        error_message += "It contains syntax errors or illegal characters."
    else:

        if error_list[1] != set():
            error_black_set[0] |= set(error_list[1])

        if error_list[2] != set():
            error_black_set[1] |= set(error_list[2])

        if error_list[3] != set():
            error_black_set[2] |= set(error_list[3])

        er_word0 = ", ".join(list(error_black_set[0]))
        er_word1 = ", ".join(list(error_black_set[1]))
        er_word2 = ", ".join(list(error_black_set[2]))

        error_message += f"\n[Syntax Blacklist] {er_word0}\n[]Condition Predicate Blacklist] {er_word1}\n[Object Blacklist] {er_word2}\n"

        error_message += "\n[Additional Promot]\n" + \
                         "1. Outputs including texts in the three blacklists are forbidden.\n" + \
                         "2. If a word from [Object Blacklist] is encountered, choose the closest parameter from the [Objects] table to formulate the outputs.\n" + \
                         "3. If a word from [Condition Predicate Blacklist] is encountered, choose the closest parameter from the [Condition Predicates] table to formulate the outputs.\n" + \
                         "4. Please generate directly interpretable predicate formulas without any additional explanations."
    print("error_message:", error_message)

    return error_message


def evaluate_answer(correct_answer, user_answer):
    """Evaluate if the `correct_answer` is logically implied by the `user_answer`."""
    correct_answer_set = set(list(chain.from_iterable(goal_transfer_ls_set(correct_answer))))
    user_answer_set = set(list(chain.from_iterable(goal_transfer_ls_set(user_answer))))

    if correct_answer_set <= user_answer_set:
        return True
    else:
        return False


def evaluate_section(prompt, section, csv_filename, id):
    """ Process a single section of the dataset and return detailed results for further processing. """
    results = {f'GA-{f}F': [] for f in range(6)}
    results.update({f'IA-{f}F': [] for f in range(6)})

    x, y = section.strip().splitlines()
    question = x.strip()
    correct_answer = y.strip().replace("Goal: ", "")
    print_colored(f"id:{id}  correct_answer: {correct_answer} Q:{question}","orange")
    error_black_set = [set(), set(), set()]
    feedback_time = 0

    # record
    data_record = [id, question, correct_answer]

    grammar_correct = False
    content_correct = False

    # Modified evaluate_responses logic here, focusing on single section
    while feedback_time <= 5:

        messages = [{"role": "user", "content": prompt + "\n" + question}]
        answer = llm.request(message=messages)
        messages.append({"role": "assistant", "content": answer})
        print_colored(f"id:{id}  {feedback_time}th Answer: {answer}  Q:{question}","yellow")

        # record
        data_record += [answer]

        grammar_correct, error_list = format_check(answer)
        content_correct = False

        if grammar_correct:
            content_correct = evaluate_answer(correct_answer, answer)
            for f in range(feedback_time, 6):
                results[f'GA-{f}F'].append(1)  # Mark grammar as correct
                results[f'IA-{f}F'].append(1 if content_correct else 0)
            break
        else:
            results[f'GA-{feedback_time}F'].append(0)
            results[f'IA-{feedback_time}F'].append(0)
            error_message = get_feedback_prompt(error_list, error_black_set)
            feedback_prompt = error_message
            messages.append({"role": "user", "content": feedback_prompt})

            # record
            if feedback_time != 5:
                data_record += [feedback_prompt]
            feedback_time += 1

    # record
    data_record.extend(["", ""] * (5 - feedback_time))
    data_record.extend([feedback_time, grammar_correct, content_correct])

    print_status(grammar_correct, content_correct)

    return results, data_record


# Main execution flow setup
if __name__ == "__main__":
    # Define file paths and read datasets
    easy_data_set_file = "dataset/easy_instr_goal.txt"
    medium_data_set_file = "dataset/medium_instr_goal.txt"
    hard_data_set_file = "dataset/hard_instr_goal.txt"

    test_data_set_file = "dataset/test.txt"

    data_set_file = "dataset/data100.txt"
    prompt_file1 = "dataset/prompt_test1.txt"
    prompt_file2 = "dataset/prompt_test2.txt"

    with open(easy_data_set_file, 'r', encoding="utf-8") as f:
        easy_data_set = f.read().strip()
    with open(medium_data_set_file, 'r', encoding="utf-8") as f:
        medium_data_set = f.read().strip()
    with open(hard_data_set_file, 'r', encoding="utf-8") as f:
        hard_data_set = f.read().strip()
    with open(prompt_file1, 'r', encoding="utf-8") as f:
        prompt1 = f.read().strip()
    with open(prompt_file2, 'r', encoding="utf-8") as f:
        prompt2 = f.read().strip()

    # Initialize data structures and loop through experiment iterations
    llm = LLMGPT3()
    max_try_time = 5
    difficulties = ["medium"]  # Can be expanded to ["easy", "medium", "hard"]
    num_examples = [0, 1, 5]

    all_results = {}
    for try_time in range(max_try_time):
        print_colored(f'=============== Time {try_time} ===============',"blue")
        for difficulty in difficulties:
            print_colored(f"-----------------------{difficulty}-------------------------","blue")

            for diff in difficulties:
                if diff not in all_results:
                    all_results[diff] = {num: [] for num in num_examples}

            data_set = easy_data_set
            if difficulty == "medium":
                data_set = medium_data_set
            elif difficulty == "hard":
                data_set = hard_data_set

            sections = re.split(r'\n\s*\n', data_set)[:]
            results_table = []

            for num in num_examples:
                feedback_type = "Zero-shot" if num == 0 else f"Few-shot {num}"
                print_colored(f'=============== Feedback Level {feedback_type} ===============',"blue")

                # record
                csv_filename = f"details_{difficulty}_shot={num}_t={try_time}.csv"
                init_csv(csv_filename)

                prompt = generate_prompt1(num, difficulty) + prompt2

                all_data_records = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = {executor.submit(evaluate_section, prompt, section, csv_filename, id): section for id, section
                               in
                               enumerate(sections)}
                    results = {f'GA-{f}F': [] for f in range(6)}
                    results.update({f'IA-{f}F': [] for f in range(6)})

                    for future in concurrent.futures.as_completed(futures):
                        evaluation_results, data_record = future.result()
                        for key in results:
                            results[key].extend(evaluation_results[key])
                        all_data_records.append(data_record)

                # Bulk write to CSV
                for data_record in all_data_records:
                    append_to_csv(csv_filename, data_record)

                filtered_keys = ['GA-0F', 'GA-1F', 'GA-5F', 'IA-0F', 'IA-1F', 'IA-5F']
                row = {key: f'{key}: {np.mean(results[key]):.2%}' for key in filtered_keys if key in results}
                results_table.append(row)

                all_results[difficulty][num].append(results)

            # Print results at the end of each difficulty level
            print("Feedback Level\t" + "\t".join(['GA-0F', 'GA-1F', 'GA-5F', 'IA-0F', 'IA-1F', 'IA-5F']))
            for index, row in enumerate(results_table):
                feedback_type = "Zero-shot" if num_examples[index] == 0 else f"Few-shot {num_examples[index]}"
                row_data = "\t".join(
                    value.split(': ')[1] if ':' in value else value
                    for key, value in row.items() if
                    key in ['GA-0F', 'GA-1F', 'GA-5F', 'IA-0F', 'IA-1F', 'IA-5F'])
                print(f"{feedback_type}\t{row_data}")

    print("\n--------------------------------------------\n")
    # Print average results for each difficulty and feedback level
    for difficulty in difficulties:
        print(f"--------- {difficulty} Average Results ---------")
        for num in num_examples:
            average_results = {}
            for key in ['GA-0F', 'GA-1F', 'GA-5F', 'IA-0F', 'IA-1F', 'IA-5F']:
                all_scores = [results[key] for results in all_results[difficulty][num]]
                average_score = np.mean([np.mean(scores) for scores in all_scores])
                average_results[key] = f'{average_score:.2%}'

            row_data = "\t".join(value for value in average_results.values())
            if num == 0:
                print(f"Zero-shot\t{row_data}")
            else:
                print(f"Few-shot-{num}\t{row_data}")
