

from sympy import symbols, Not, Or, And, to_dnf
from sympy import symbols, simplify_logic
import re



import re

def act_str_process(act_str, already_split=False):
    """
    Processes action strings in both underscore-separated and parentheses formats.

    Parameters:
    - act_str (str or list): The string or list of strings to be processed.
    - already_split (bool): Whether the input is already a list of action strings.

    Returns:
    - priority_act_ls (list): A list of formatted action strings in "Verb(Object)" format.
    """
    # Determine if the input is already a list or needs to be split
    if already_split:
        act_str_ls = act_str
    else:
        act_str_ls = act_str.replace(" ", "").split(",")

    priority_act_ls = []

    # Process each action string
    for literal in act_str_ls:
        # Remove only unwanted characters while keeping parentheses intact
        literal = re.sub(r"[\[\]\n]", "", literal)

        # Check for underscore-separated format (e.g., "Walk_pear")
        if '_' in literal and '(' not in literal:
            first_part, rest = literal.split('_', 1)
            literal = f"{first_part}({rest})"
            literal = literal.replace('_', ',')

        # Add parentheses if not already in that format
        elif '(' not in literal:
            literal = literal.replace('_', ',')
            literal = f"{literal}()"

        # Append processed literal to the list
        priority_act_ls.append(literal)

    return priority_act_ls

# Example usage:
# action_str = 'Walk_pear, RightGrab_pear, Walk_kitchentable'
# processed = act_str_process(action_str)
# print(processed)
#
# action_str_parentheses = 'Walk(pear), RightGrab(pear), Walk(kitchentable)'
# processed_parentheses = act_str_process(action_str_parentheses)
# print(processed_parentheses)







def goal_transfer_str(goal):
    goal_dnf = str(to_dnf(goal, simplify=True,force=True))
    # print(goal_dnf)
    goal_set = []
    if ('|' in goal or '&' in goal or 'Not' in goal) or not '(' in goal:
        goal_ls = goal_dnf.split("|")
        for g in goal_ls:
            g_set = set()
            g = g.replace(" ", "").replace("(", "").replace(")", "")
            g = g.split("&")
            for literal in g:
                if '_' in literal:
                    first_part, rest = literal.split('_', 1)
                    literal = first_part + '(' + rest
                    # 添加 ')' 到末尾
                    literal += ')'
                    # 替换剩余的 '_' 为 ','
                    literal = literal.replace('_', ',')
                g_set.add(literal)
            goal_set.append(g_set)

    else:
        g_set = set()
        w = goal.split(")")
        g_set.add(w[0] + ")")
        if len(w) > 1:
            for x in w[1:]:
                if x != "":
                    g_set.add(x[1:] + ")")
        goal_set.append(g_set)
    return goal_set



def act_format_records(act_record_list):
    # 初始化一个空列表来存储格式化后的结果
    formatted_records = []
    predicate = []
    objects_ls= []
    # 遍历列表中的每个记录
    for record in act_record_list:

        if "," not in record:
            # 找到括号的位置
            start = record.find('(')
            end = record.find(')')
            # 提取动作和对象
            action = record[:start]
            obj = record[start+1:end]
            # 格式化为新的字符串格式
            formatted_record = f"{action}_{obj}"
            # 将格式化后的字符串添加到结果列表中
            formatted_records.append(formatted_record)
            predicate.append(action)
            objects_ls.append(obj)
        else:
            # 有逗号，即涉及两个物体
            start = record.find('(')
            end = record.find(')')
            action = record[:start]
            objects = record[start + 1:end].split(',')
            obj1 = objects[0].strip()  # 去除可能的空白字符
            obj2 = objects[1].strip()
            formatted_record = f"{action}_{obj1}_{obj2}"
            # 将格式化后的字符串添加到结果列表中
            formatted_records.append(formatted_record)
            predicate.append(action)
            objects_ls.append(obj1)
            objects_ls.append(obj2)

    from collections import OrderedDict
    return list(formatted_records),list(OrderedDict.fromkeys(predicate)),list(OrderedDict.fromkeys(objects_ls))



def remove_duplicates_using_set(lst):
    return list(set(lst))


def update_objects_from_expressions(expressions, pattern, objects):
    for expr in expressions:
        match = pattern.search(expr)
        if match:
            # 将括号内的内容按逗号分割并加入到集合中
            objects.update(match.group(1).split(','))
