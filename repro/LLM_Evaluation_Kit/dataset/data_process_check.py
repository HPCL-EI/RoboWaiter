from sympy import symbols, Not, Or, And, to_dnf
from sympy import symbols, simplify_logic

import re

split_characters = r'[()&|~ ]'

predicate_list = {"RobotNear", "On", "Holding", "Exists", "IsClean", "Active", "Closed", "Low"}
object_list = {'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk',
               'VacuumCup', 'Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater',
               'Apple', 'Banana', 'Mangosteen', 'Orange', 'Glass', 'OrangeJuice', 'Tray', 'CoconutMilk', 'Kettle',
               'PaperCup', 'Bread', 'Cake', 'LunchBox', 'Teacup', 'Tissue', 'Chocolate', 'Sandwiches', 'Mugs', 'Ice',
               'Bar', 'Bar2', 'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3', 'WindowTable4',
               'WindowTable5', 'WindowTable6', 'QuietTable1', 'QuietTable2', 'ReadingNook', 'Entrance', 'Exit',
               'LoungeArea', 'HighSeats', 'VIPLounge', 'MerchZone',
               'Table1', 'Floor', 'Chairs', 'AC', 'TubeLight', 'HallLight', 'Curtain', 'ACTemperature'
               }

dic_pred_obj = {}
dic_pred_obj['RobotNear'] = ['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink',
                             'Milk', 'VacuumCup', 'Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater', 'Apple',
                             'Banana', 'Mangosteen', 'Orange', 'Kettle', 'PaperCup', 'Bread', 'LunchBox', 'Teacup',
                             'Chocolate', 'Sandwiches', 'Mugs', 'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk',
                             'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup', 'Tissue',
                             'YogurtDrink', 'Newspaper', 'Box', 'PaperCupStarbucks', 'CoffeeMachine', 'Straw', 'Cake',
                             'Tray', 'Bread', 'Glass', 'Door', 'Mug', 'Machine', 'PackagedCoffee', 'CubeSugar', 'Apple',
                             'Spoon', 'Drinks', 'Drink', 'Ice', 'Saucer', 'TrashBin', 'Knife', 'Cube']
dic_pred_obj['RobotNear'] += ['Bar', 'Bar2', 'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3',
                              'WindowTable6', 'WindowTable4', 'WindowTable5', 'QuietTable1', 'QuietTable2',
                              'QuietTable3', 'ReadingNook', 'Entrance', 'Exit', 'LoungeArea', 'HighSeats', 'VIPLounge',
                              'MerchZone']
dic_pred_obj['IsClean'] = ['Table1', 'Floor', 'Chairs']
dic_pred_obj['Active'] = ['AC', 'TubeLight', 'HallLight']
dic_pred_obj['Closed'] = ['Curtain']
dic_pred_obj['Low'] = ['ACTemperature']


def format_check(result):
    try:
        goal_dnf = str(to_dnf(result, simplify=True))
    except Exception as e:
        # print("Caught an error:", e)
        return False, [str(e), None, None, None]

    split_sentences = re.split(split_characters, result)
    split_sentences = [s.strip() for s in split_sentences if s.strip()]

    wrong_format_set = set()
    wrong_predicate_set = set()
    wrong_object_set = set()

    for sentence in split_sentences:
        if sentence == "": continue
        try:
            goal_dnf = str(to_dnf(sentence, simplify=True))
            word_list = re.split('_|~', sentence)
            word_list = [word for word in word_list if word]
            if len(word_list) <= 1:
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

    if len(wrong_format_set) == 0 and \
            len(wrong_predicate_set) == 0 and \
            len(wrong_object_set) == 0:
        return True, None
    else:
        return False, [None, wrong_format_set, wrong_predicate_set, wrong_object_set]


def goal_transfer_ls_set(goal):
    goal_dnf = str(to_dnf(goal, simplify=True))
    goal_set = []
    goal_ls = goal_dnf.split("|")
    for g in goal_ls:
        g_set = set()
        g = g.replace(" ", "").replace("(", "").replace(")", "")
        g = g.split("&")
        for literal in g:
            if '_' in literal:
                first_part, rest = literal.split('_', 1)
                literal = first_part + '(' + rest
                literal += ')'
                literal = literal.replace('_', ',')
            literal = literal.replace('~', 'Not ')
            g_set.add(literal)
        goal_set.append(g_set)
    goal_set = [sorted(set(item)) for item in goal_set]
    return goal_set
