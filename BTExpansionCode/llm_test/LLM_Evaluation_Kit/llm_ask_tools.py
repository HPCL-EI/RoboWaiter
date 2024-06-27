import re
from btpg.algos.llm_client.tools import goal_transfer_str, act_str_process
from btpg.utils import ROOT_PATH
# 导入向量数据库检索的相关函数
from btpg.algos.llm_client.vector_database_env_goal import search_nearest_examples
from ordered_set import OrderedSet


def parse_llm_output(answer,goals=True):
    goal_set = set()
    priority_act_ls, key_predicate, key_objects = [], [], []

    try:
        if goals:
            goal_str = answer.split("Optimal Actions:")[0].replace("Goals:", "").strip()
            goal_set = goal_transfer_str(goal_str)

        act_str = answer.split("Optimal Actions:")[1].split("Vital Action Predicates:")[0].strip()
        predicate_str = answer.split("Vital Action Predicates:")[1].split("Vital Objects:")[0].strip()
        objects_str = answer.split("Vital Objects:")[1].strip()
        priority_act_ls = act_str_process(act_str)

        # Remove all spaces, Split by comma to create a list
        key_predicate = predicate_str.replace(" ", "").split(",")
        key_objects = objects_str.replace(" ", "").split(",")

        priority_act_ls = list(OrderedSet(priority_act_ls))
        key_predicate = list(OrderedSet(key_predicate))
        key_objects = list(OrderedSet(key_objects))
    except Exception as e:
        goal_set, priority_act_ls, key_predicate, key_objects = None,None,None,None
        print(f"Failed to parse LLM output: {e}")


    if goals:
        return goal_set,priority_act_ls,key_predicate,key_objects
    else:
        return priority_act_ls, key_predicate, key_objects



def format_example(metadata):
    """格式化向量数据库的示例数据为所需的格式"""
    example_value = metadata['value']
    return (
        # f"Instruction: {example_value['Instruction']}\n"
            f"Goals: {example_value['Goals']}\n"
            f"Optimal Actions: {example_value['Optimal Actions']}\n"
            f"Vital Action Predicates: {example_value.get('Vital Action Predicates', '')}\n"
            f"Vital Objects: {example_value['Vital Objects']}\n")

def extract_llm_from_instr_goal(llm,default_prompt_file,environment,goals,instruction=None,cur_cond_set=None,\
                                choose_database=False,\
                                database_index_path=f"{ROOT_PATH}/../test/dataset/env_instruction_vectors.index",verbose=False):
    with open(default_prompt_file, 'r', encoding="utf-8") as f:
        prompt = f.read().strip()

    distances=None
    parsed_output =None
    parsed_fail=-1
    RED = "\033[31m"
    RESET = "\033[0m"

    while parsed_output==None:

        parsed_fail += 1 # 第一次是第0次。 0-1-2-3
        print(f"--- LLM: Goal={goals}  Parsed Fail={parsed_fail} --- ")
        if parsed_fail > 3:
            print(f"{RED}----LLM: Goal={goals}  Parsed Fail={parsed_fail} >3 break -----{RESET}")
            break

        if choose_database:

            # environment ?
            nearest_examples,distances = search_nearest_examples(database_index_path, llm, goals, top_n=5)
            # 使用自定义的格式函数将检索到的示例格式化为目标样式
            example_texts = '\n'.join([format_example(ex) for ex in nearest_examples])
            example_texts = "[Examples]\n" + example_texts

            # 输出最近的所有goal
            nearest_goals = [ex['value']['Goals'] for ex in nearest_examples]
            print("All Goals from nearest examples:")
            for g in nearest_goals:
                print(f"\033[93m{g}\033[0m") # 打印黄色 print(goal)

            # print("distances:",distances)
            # print("example_texts:\n",example_texts)
            # 替换 prompt 中的 [Examples] 部分
            example_marker = "[Examples]"
            if example_marker in prompt:
                prompt = prompt.replace(example_marker, example_texts)
            else:
                prompt = f"{prompt}\n{example_texts}"

        # 构建完整的 prompt，包括检索的 Examples 和当前的指令
        goals_str =' & '.join(goals)
        # question = f"{prompt}\nInstruction: {instruction}\nGoals: {goals_str}"
        question = f"{prompt}\nGoals: {goals_str}"
        if verbose:
            print("============ Question ================\n",question)
        messages = []
        messages.append({"role": "user", "content": question})
        answer = llm.request(message=messages)
        messages.append({"role": "assistant", "content": answer})
        # if verbose:
        # print("============ Answer ================\n",answer)
        parsed_output = parse_llm_output(answer, goals=False)
        # if parsed_output is None:
        #     print(f"\033[91mFailed to parse LLM output for goals: {goals_str}\033[0m")
        #     return None, None, None, messages, distances

    priority_act_ls, key_predicates, key_objects = parsed_output



    if priority_act_ls==None:
        print(f"\033[91mFailed to parse LLM output for goals: {goals_str}\033[0m")
    return priority_act_ls, key_predicates, key_objects, messages, distances,parsed_fail

def extract_llm_from_instr(llm,default_prompt_file,instruction,cur_cond_set,\
                                choose_database=False,\
                                index_path=f"{ROOT_PATH}/../test/dataset/env_instruction_vectors.index"):
    """从向量数据库检索并生成初始 prompt"""

    with open(default_prompt_file, 'r', encoding="utf-8") as f:
        prompt = f.read().strip()

    if choose_database:
        # 补充：向量数据库检索，拼接上最相近的 Example cur_cond_set
        # cur_env_state = ', '.join(map(str, cur_cond_set))
        # cur_data = instuction + "\n[current environmental condition]\n" + cur_env_state  # 可能还要再调整
        # cur_emb = llm.embedding(question=cur_data)
        # 导入向量数据库，找到最近的前5条。
        # 准备好的 30条数据 作为 向量数据库
        # example = ""
        # 将例子拼在后面
        # question+=example
        # 检索向量数据库以获取最近的 Examples
        nearest_examples,distances = search_nearest_examples(index_path, llm, instruction,top_n=3)
        # 使用自定义的格式函数将检索到的示例格式化为目标样式
        example_texts = '\n'.join([format_example(ex) for ex in nearest_examples])
        example_texts = "[Examples]\n" + example_texts
        print("distances:",distances)
        # print("example_texts:\n",example_texts)
        # 替换 prompt 中的 [Examples] 部分
        example_marker = "[Examples]"
        if example_marker in prompt:
            prompt = prompt.replace(example_marker, example_texts)
        else:
            prompt = f"{prompt}\n{example_texts}"


    # 构建完整的 prompt，包括检索的 Examples 和当前的指令
    question = f"{prompt}\n{instruction}"
    print("question:",question)
    messages = []
    messages.append({"role": "user", "content": question})
    answer = llm.request(message=messages)
    messages.append({"role": "assistant", "content": answer})
    print(answer)

    goal_set, priority_act_ls, key_predicates, key_objects = parse_llm_output(answer)

    print("goal",goal_set)
    print("act:",priority_act_ls)
    print("key_predicate",key_predicates)
    print("Vital Objects:",key_objects)


    # 提取目标中的所有物体
    objects = set()
    # 正则表达式用于找到括号中的内容
    pattern = re.compile(r'\((.*?)\)')
    # 遍历所有表达式，提取物体名称
    for expr in goal_set[0]:
        # 找到括号内的内容
        match = pattern.search(expr)
        if match:
            # 将括号内的内容按逗号分割并加入到集合中
            objects.update(match.group(1).split(','))
    key_objects += list(objects)
    key_objects = list(set(key_objects))

    return goal_set, priority_act_ls, key_predicates, key_objects, messages

def act_tree_verbose(llm, messages, reflect_prompt):
    messages.append({"role": "user", "content": reflect_prompt})
    answer = llm.request(message=messages)
    messages.append({"role": "assistant", "content": answer})

    print("============ Answer ================\n",answer)

    goal_set, priority_act_ls, key_predicates, key_objects = parse_llm_output(answer)

    print("goal",goal_set)
    print("act:",priority_act_ls)
    print("key_predicate",key_predicates)
    print("Vital Objects:",key_objects)

    return goal_set, priority_act_ls, key_predicates, key_objects, messages


def convert_conditions(conditions_set):
    # Initialize an empty list to store the formatted strings
    formatted_conditions = []

    # Loop over each condition in the set
    for condition in conditions_set:
        # Remove the parentheses and split the condition into parts based on the first opening parenthesis
        base, args = condition.split("(")
        # Remove the closing parenthesis and replace commas with underscores in the arguments
        args = args.strip(")").replace(",", "_")
        # Concatenate the base and the arguments with an underscore and add to the list
        formatted_conditions.append(f"{base.strip()}_{args}")

    formatted_conditions_str = " & ".join(formatted_conditions)
    return formatted_conditions_str


def extract_llm_from_reflect(llm,messages,nearest_examples=None):

    answer = llm.request(message=messages)
    messages.append({"role": "assistant", "content": answer})
    priority_act_ls, key_predicates, key_objects = parse_llm_output(answer,goals=False) # 返回的都是list

    cyan = "\033[36m"
    reset = "\033[0m"
    print(f"{cyan}--- Reflect Just LLM ---{reset}")
    print(f"{cyan}priority_act_ls: {', '.join(priority_act_ls)}{reset}")
    print(f"{cyan}key_predicates: {', '.join(key_predicates)}{reset}")
    print(f"{cyan}key_objects: {', '.join(key_objects)}{reset}")

    # 如果这里面把例子中的pred和obj也加进去
    if nearest_examples!=None:
        ex_preds=set()
        ex_objs=set()
        for ex in nearest_examples:
            ex_preds |= set(ex['value']['Vital Action Predicates'].replace(" ", "").split(","))
            ex_objs |= set(ex['value']['Vital Objects'].replace(" ", "").split(","))
        key_predicates = list(set(key_predicates) | ex_preds)
        key_objects = list(set(key_objects) | ex_objs)

        pass

    cyan = "\033[36m"
    reset = "\033[0m"
    print(f"{cyan}--- Reflect Answers ---{reset}")
    print(f"{cyan}priority_act_ls: {', '.join(priority_act_ls)}{reset}")
    print(f"{cyan}key_predicates: {', '.join(key_predicates)}{reset}")
    print(f"{cyan}key_objects: {', '.join(key_objects)}{reset}")

    return priority_act_ls, key_predicates, key_objects, messages