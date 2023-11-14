# the empty string '' represents robot holds nothing
import os
import re

Object = ['Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk', 'VacuumCup']

Cookable = ['Coffee', 'Water', 'Dessert']

Place = ['Bar', 'WaterTable', 'CoffeeTable', 'Bar2', 'Table1', 'Table2', 'Table3']

Entity = ['Robot', 'Customer']

Operable = ['AC', 'ACTemperature', 'HallLight', 'TubeLight', 'Curtain', 'Chairs', 'Floor', 'Table']

import random


def single_predict_generation(oplist_1, oplist_2, predict_pattern) -> str:
    index_1 = random.randint(0, len(oplist_1) - 1)
    if oplist_2:
        index_2 = random.randint(0, len(oplist_2) - 1)

    match predict_pattern:
        case 'at':
            return f'At({oplist_1[index_1]}, {oplist_2[index_2]})'
        case 'is':
            return f'Is({oplist_1[index_1]}, {oplist_2[index_2]})'
        case 'hold':
            return f'Holding({oplist_1[index_1]})'
        case 'on':
            return f'On({oplist_1[index_1]}, {oplist_2[index_2]})'
        case _:
            raise RuntimeError('Incorrect predict pattern!')


def enumerate_predict(oplist_1, oplist_2, predict_pattern) -> [int, list]:
    count = 0
    res = []

    match predict_pattern:
        case 'at':
            pattern = f'At(%s,%s)'
        case 'is':
            pattern = f'Is(%s,%s)'
        case 'hold':
            pattern = f'Holding(%s)'
        case 'on':
            pattern = f'On(%s,%s)'
        case _:
            raise RuntimeError('Incorrect predict pattern!')

    for str_1 in oplist_1:
        if oplist_2:
            for str_2 in oplist_2:
                count += 1
                res.append(pattern % (str_1, str_2))
        else:
            count += 1
            res.append(pattern % str_1)

    return count, res


def generate_goal_states(vln_num: int, vlm_num: int, opentask_num: int):
    # res stores lists of sets, while each state represent in set.
    res = []

    # goal states for VLN
    for i in range(vln_num):
        res.append({single_predict_generation(['Robot'], Place, 'at')})

    # goal states for VLM
    for i in range(int(vlm_num)):
        for j in range(int(vlm_num)):
            res.append(
                {
                    single_predict_generation(['Robot'], Place, 'at'),
                    single_predict_generation(Operable, ['0', '1'], 'is')
                }
            )

    # goal states for Open-task-1
    for i in range(int(opentask_num)):
        for j in range(int(opentask_num)):
            res.append(
                {
                    single_predict_generation(['Robot'], Place, 'at'),
                    single_predict_generation(Object, Place, 'on')
                }
            )

    print(res)
    print(len(res))

    return res


def enumerate_goal_states(total: int):
    res = []

    point_15 = int(total * .15)
    point_10 = int(total * .10)

    # goal states for VLN, .15
    count_vln, list_vln = enumerate_predict(['Robot'], Place, 'at')
    list_vln = ['{%s}' % i for i in list_vln]
    if count_vln < point_15:
        list_vln *= point_15 // count_vln
        for i in range(0, point_15 - len(list_vln)):
            list_vln.append('{%s}' % single_predict_generation(['Robot'], Place, 'at'))
    # print(f'VLN 任务的目标状态数：{count_vln}')
    res += list_vln

    # goal states for VLM-1, 0.15
    count_vlm_1, list_vlm_1 = enumerate_predict(Object, Place, 'on')
    list_vlm_1 = ['{%s}' % i for i in list_vlm_1]
    if count_vlm_1 < point_15:
        list_vlm_1 *= point_15 // count_vlm_1
        for i in range(0, point_15 - len(list_vlm_1)):
            list_vlm_1.append('{%s}' % (single_predict_generation(Object, Place, 'on')))
    res += list_vlm_1

    # goal states for VLM-2, 0.15
    count_vlm_2, list_vlm_2 = enumerate_predict(Operable, ['0', '1'], 'is')
    list_vlm_2 = ['{%s}' % i for i in list_vlm_2]
    if count_vlm_2 < point_15:
        list_vlm_2 *= point_15 // count_vlm_2
        for i in range(0, point_15 - len(list_vlm_2)):
            list_vlm_2.append('{%s}' % single_predict_generation(Operable, ['0', '1'], 'is'))
    res += list_vlm_2

    # goal states for VLM-3, 0.1
    count_vlm_3, list_vlm_3 = enumerate_predict(Object + ['Nothing'], None, 'hold')
    list_vlm_3 = ['{%s}' % i for i in list_vlm_3]
    if count_vlm_3 < point_10:
        list_vlm_3 *= point_10 // count_vlm_3
        for i in range(0, point_10 - len(list_vlm_3)):
            list_vlm_3.append('{%s}' % single_predict_generation(Object, None, 'hold'))
    res += list_vlm_3

    # goal states for OT, 0.15
    count_ot, list_ot = enumerate_predict(Cookable, Place, 'on')
    list_ot = ['{%s}' % i for i in list_ot]
    if count_ot < point_15:
        list_ot *= point_15 // count_ot
        for i in range(0, point_15 - len(list_ot)):
            list_ot.append('{%s}' % single_predict_generation(Cookable, Place, 'on'))
    res += list_ot

    # goal states for compound-1, 0.1
    count_1, list_1 = enumerate_predict(['Robot'], Place, 'at')
    count_2, list_2 = enumerate_predict(Object, Place, 'on')
    list_tmp = []
    for i in list_1:
        for j in list_2:
            list_tmp.append('{%s,%s}' % (i, j))
    if len(list_tmp) < point_10:
        list_tmp *= point_10 // len(list_tmp)
        list_tmp += list_tmp[0:point_10 - len(list_tmp)]
    else:
        list_tmp = list_tmp[:point_10]
    res += list_tmp

    # goal states for compound-2, 0.1
    count_1, list_1 = enumerate_predict(['Robot'], Place, 'at')
    count_2, list_2 = enumerate_predict(Operable, ['0', '1'], 'is')
    list_tmp = []
    for i in list_1:
        for j in list_2:
            list_tmp.append('{%s,%s}' % (i, j))
    if len(list_tmp) < point_10:
        list_tmp *= point_10 // len(list_tmp)
        list_tmp += list_tmp[0:point_10 - len(list_tmp)]
    else:
        list_tmp = list_tmp[:point_10]
    res += list_tmp

    # goal states for compound-3, 0.1
    count_1, list_1 = enumerate_predict(Cookable, Place, 'on')
    count_2, list_2 = enumerate_predict(Operable, ['0', '1'], 'is')
    list_tmp = []
    for i in list_1:
        for j in list_2:
            list_tmp.append('{%s,%s}' % (i, j))
    if len(list_tmp) < point_10:
        list_tmp *= point_10 // len(list_tmp)
        list_tmp += list_tmp[0:point_10 - len(list_tmp)]
    else:
        list_tmp = list_tmp[:point_10]
    res += list_tmp

    # # goal states for VLM-1, 0.15
    # count_vlm_1, list_vlm_1 = enumerate_predict(['Robot'], Place, 'at')
    # count_vlm_2, list_vlm_2 = enumerate_predict(Operable, ['0', '1'], 'is')
    # print(f'VLM 任务的目标状态数：{count_vlm_1 * count_vlm_2}')
    #
    # # goal states for open-task
    # count_opentask_1, list_opentask_1 = enumerate_predict(['Robot'], Place, 'at')
    # count_opentask_2, list_opentask_2 = enumerate_predict(Object, Place, 'on')
    # print(f'Open-task-1 任务的目标状态数：{count_opentask_1 * count_opentask_2}')

    with open(os.path.join('./goal_states.txt'), 'w+') as file:
        for i in res:
            if 'Is' in i and 'ACTemperature' in i:
                i = re.sub('0', 'Up', i)
                i = re.sub('1', 'Down', i)
            elif 'Is' in i and ('AC' in i or 'HallLight' in i or 'TubeLight' in i or 'Curtain' in i):
                i = re.sub('0', 'Off', i)
                i = re.sub('1', 'On', i)
            elif 'Is' in i and ('Chairs' in i or 'Floor' in i or 'Table' in i):
                i = re.sub('0', 'Dirty', i)
                i = re.sub('1', 'Clean', i)

            file.write(i + '\n')


# generate_goal_states(30, 6, 6)
enumerate_goal_states(5000)
