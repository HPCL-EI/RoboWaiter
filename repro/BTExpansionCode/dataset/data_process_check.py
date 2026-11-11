
from sympy import symbols, Not, Or, And, to_dnf
from sympy import symbols, simplify_logic

import re

split_characters = r'[()&|~ ]'  # 用正则表达式定义多个字符，包括逗号、句号、分号和感叹号等

predicate_list = {"RobotNear","On","Holding","Exists","IsClean","Active","Closed","Low"}
object_list = {'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk','VacuumCup','Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater',
'Apple','Banana','Mangosteen','Orange','Glass','OrangeJuice','Tray','CoconutMilk','Kettle','PaperCup','Bread','Cake','LunchBox','Teacup','Tissue','Chocolate','Sandwiches','Mugs','Ice',
'Bar', 'Bar2', 'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3','WindowTable4','WindowTable5','WindowTable6','QuietTable1','QuietTable2','ReadingNook','Entrance','Exit','LoungeArea','HighSeats','VIPLounge','MerchZone',
'Table1','Floor','Chairs','AC','TubeLight','HallLight','Curtain','ACTemperature'
               }

dic_pred_obj={}
dic_pred_obj['RobotNear']=['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk', 'VacuumCup','Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater', 'Apple', 'Banana', 'Mangosteen', 'Orange','Kettle', 'PaperCup', 'Bread', 'LunchBox','Teacup', 'Chocolate', 'Sandwiches', 'Mugs','Watermelon', 'Tomato', 'CleansingFoam','CocountMilk','SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup','Tissue', 'YogurtDrink', 'Newspaper', 'Box','PaperCupStarbucks', 'CoffeeMachine', 'Straw', 'Cake','Tray', 'Bread','Glass', 'Door','Mug', 'Machine','PackagedCoffee', 'CubeSugar','Apple', 'Spoon','Drinks', 'Drink','Ice', 'Saucer','TrashBin', 'Knife','Cube']
dic_pred_obj['RobotNear']+=['Bar', 'Bar2', 'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3', 'WindowTable6','WindowTable4', 'WindowTable5','QuietTable1', 'QuietTable2', 'QuietTable3', 'ReadingNook', 'Entrance', 'Exit', 'LoungeArea', 'HighSeats','VIPLounge', 'MerchZone']
dic_pred_obj['IsClean']=['Table1','Floor','Chairs']
dic_pred_obj['Active']=['AC','TubeLight','HallLight']
dic_pred_obj['Closed']=['Curtain']
dic_pred_obj['Low']=['ACTemperature']

# object_list = {'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk',
#                'MilkDrink', 'Milk','VacuumCup','Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater',
#                 'Bar', 'Bar2', 'WaterTable', 'CoffeeTable', 'Table1', 'Table2', 'Table3','BrightTable6',
#                 'Table1','Floor','Chairs',
#                 'AC','TubeLight','HallLight',
#                 'Curtain','ACTemperature'
#                }
def format_check(result):
    try:
        goal_dnf = str(to_dnf(result, simplify=True))
    except Exception as e:
        # print("Caught an error:", e)
        return False, [str(e),None,None,None]

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
            word_list = re.split('_|~', sentence)
            word_list = [word for word in word_list if word]
            # word_list = sentence.split('_|~')
            if len(word_list) <=1:
                wrong_format_set.add(sentence)
                continue

            predicate = word_list[0]
            if predicate not in predicate_list:
                wrong_predicate_set.add(predicate)

            for object in word_list[1:]:
                if object not in object_list:
                    wrong_object_set.add(object)
                if predicate in dic_pred_obj \
                        and predicate not in wrong_predicate_set and object not in wrong_object_set \
                        and object not in dic_pred_obj[predicate]:
                    wrong_format_set.add(sentence)


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
        return False, [None,wrong_format_set,wrong_predicate_set,wrong_object_set]

def word_correct(sentence):
    try:
        goal_dnf = str(to_dnf(sentence, simplify=True))
        return True
    except:
        return False


# 检查 easy_instr_goal 的 goal 中的语法、谓词、obj


# data_set_file = "easy_instr_goal.txt"
# data_set_file = "medium_instr_goal.txt"
# data_set_file = "../dataset/hard_instr_goal.txt"

# with open(data_set_file, 'r', encoding="utf-8") as f:
#     for i,line in enumerate(f):
#         clean_line = line.strip()
#         if 'Goal' in clean_line:
#             answer = line.replace("Goal:","")
#             format_correct,error_list = format_check(answer)
#             if not format_correct:
#                 print(i," ",clean_line," ",error_list)



# # answer = '~On_Water_Bar & (On_Coffee_Table2 | On_Bernachon_Table2)'
# answer = 'On_Coffee_Table2 & ~(RobotNear_Table1 | RobotNear_Table3)'
# split_sentences = re.split(r'[()&|~ ]', answer)
# split_sentences = [s.strip() for s in split_sentences if s.strip()]
# print("split_sentences:",split_sentences)
# goal_dnf = str(to_dnf(answer, simplify=True))
# # print(goal_dnf)
# format_correct,error_list = format_check(answer)
# print(format_correct)
# print(error_list)

def goal_transfer_ls_set(goal):
    goal_dnf = str(to_dnf(goal, simplify=True))
    # print(goal_dnf)
    goal_set =[]
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
            literal=literal.replace('~', 'Not ')
            g_set.add(literal)
        goal_set.append(g_set)
    goal_set = [sorted(set(item)) for item in goal_set]
    return goal_set




def get_feedback_prompt(prompt,result,error_list):
    # wrong_format_set,wrong_predicate_set,wrong_object_set = error_list

    error_message=""

    if error_list[0]!=None:
        error_message += "Syntax or Format Error. "+ error_list[0] + ".The answer should consist only of ~, |, &, and the given [Condition] and  [Object].. "
    else:
        if error_list[1]!=set():
            error_strings = ", ".join(error_list[1])
            error_message += f"\"{error_strings}\" have format errors. They should consist only of ~, |, &, and the given [Condition] and  [Object].\n"
        if error_list[2]!=set():
            error_strings = ", ".join(error_list[2])
            error_message +=  f"\"{error_strings}\" are not in [Condition]. Please select the appropriate predicates from the [Condition] table to form the answer.\n"
        if error_list[3]!=set():
            error_strings = ", ".join(error_list[3])
            error_message +=  f"\"{error_strings}\" are not in [Object]. Please select the appropriate parameters from the [Object] table to form the answer.\n"

    # print("********** error_message: ",error_message,"\n********************")

    prompt += "\n"+"The last answer is "+result +".\n" + error_message
    return prompt



# answer = 'On_BottledDrink_Table3 | On_MilkDrink_Table3 |On_Softdrink_Bar' #'~On_Water_Bar & (On_Coffee_Table2 | On_Bernachon_Table2)'
# goal_dnf = str(to_dnf(answer, simplify=True))
# print(goal_dnf)
# print(goal_transfer_str(goal_dnf))

# answer = '~Holding_Chips & Is_Chairs_Clean'
# answer = 'On_Fries_Table6 & On_Yogurt_Table6 | (Active_HallLight & ~Low_ACTemperature) | (~Active_Curtain & Low_ACTemperature) | (Exists_Coffee & ~Holding_ADMilk)'
# answer="On_Fries_Table6 & On_Yogurt_Table6 | On_Coffee_Table6 & ~Holding_ADMilk | ~Low_ACTemperature | ~Closed_Curtain"
# answer="On_Fries_Table6 & (On_Yogurt_Table6 | On_Coffee_Table6) & ( OpenCurtain | ~Active_ACTemperature)"


# answer="On_Fries_Table6 & (On_Juice_Table6 | ~Exist_Juice => On_Coffee_Table6) & (OpenCurtain | ~Low_AC)"
# answer="On_Fries_Table6 & (On_Juice_Table6 | On_Coffee_Table6) & (Open_Curtain | ~Low_ACTemperature)"
#
answer="(On_Juice_Table6 | ~Exist_Juice=>On_Coffee_Table6 ) & ( ~Low_AC | Open_Curtain )"
format_correct,error_list = format_check(answer)
print(format_correct)
print(error_list)
print(get_feedback_prompt("",answer,error_list))