# the empty string '' represents robot holds nothing
import os
import re

Object = ['Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk', 'VacuumCup']

Cookable = ['Coffee', 'Water', 'Dessert']

Place = ['Bar', 'WaterTable', 'CoffeeTable', 'Bar2', 'Table1', 'Table2', 'Table3']

Entity = ['Robot', 'Customer']

Operable = ['AC', 'ACTemperature', 'HallLight', 'TubeLight', 'Curtain', 'Chairs', 'Floor', 'Table1']

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
                i = re.sub(',0', ',Up', i)
                i = re.sub(',1', ',Down', i)
            elif 'Is' in i and ('AC' in i or 'HallLight' in i or 'TubeLight' in i or 'Curtain' in i):
                i = re.sub(',0', ',Off', i)
                i = re.sub(',1', ',On', i)
            elif 'Is' in i and ('Chairs' in i or 'Floor' in i or 'Table' in i):
                i = re.sub(',0', ',Dirty', i)
                i = re.sub(',1', ',Clean', i)

            file.write(i + '\n')


def translate_zero_one(i: str) -> str:
    if 'ACTemperature' in i:
        i = re.sub('0\)', '调高', i)
        i = re.sub('1\)', '调低', i)
    elif 'AC' in i or 'HallLight' in i or 'TubeLight' in i or 'Curtain' in i:
        i = re.sub('0\)', '关闭', i)
        i = re.sub('1\)', '打开', i)
    elif 'Chairs' in i or 'Floor' in i or 'Table' in i:
        i = re.sub('0\)', '脏', i)
        i = re.sub('1\)', '打扫干净', i)

    return i


def enumerate_goal_states_with_describe() -> str:
    with open(os.path.join('./goal_states_with_description.txt'), 'w', encoding='utf-8') as file:
        # vln
        count, res = enumerate_predict(['Robot'], Place, 'at')
        print(count)
        for i in range(count):
            tmp = '#' + res[i].split(',')[-1][:-1]
            file.write(f'{res[i]}\t请你来一下{tmp}。\n')
            file.write(f'{res[i]}\t请你去一下{tmp}。\n')
            file.write(f'{res[i]}\t你能去{tmp}那个位置吗？\n')

        # vlm, on
        count, res = enumerate_predict(Object, Place, 'on')
        print(count)
        for i in range(count):
            tmp = res[i].split(',')
            obj = '#' + tmp[0][3:]
            pla = '#' + tmp[-1][:-1]
            file.write(f'{res[i]}\t请你把{obj}放到{pla}那个位置。\n')
            file.write(f'{res[i]}\t请你拿一下{obj}到{pla}位置。\n')

        # vlm, is
        count, res = enumerate_predict(Operable, ['0', '1'], 'is')
        print(count)
        for i in res:
            tmp = i.split(',')
            thing, op = '#' + tmp[0][3:], '#' + tmp[-1]
            file.write('%s\t%s\n' % (i, translate_zero_one(f'你能把{thing}{op}一下吗？')))

        # vlm, holding
        count, res = enumerate_predict(Object + ['Nothing'], None, 'hold')
        print(count)
        for i in res:
            tmp = '#' + i.split('(')[-1][:-1]
            if tmp == 'Nothing':
                file.write(f'{i}\t你手里是没有东西的吗？\n')
                continue
            file.write(f'{i}\t你能把{tmp}抓在手里吗？\n')
            file.write(f'{i}\t你能一直拿着{tmp}吗？\n')

        count, res = enumerate_predict(Cookable, Place, 'on')
        print(count)
        for i in res:
            tmp = i.split(',')
            thing, pla = '#' + tmp[0][3:], '#' + tmp[-1][:-1]

            file.write(f'{i}\t你能制作{thing}并把它端到{pla}这里来吗？\n')
            file.write(f'{i}\t给我来点{thing}，并把它端到{pla}这里来。\n')
    return './goal_states_with_description.txt'


from copy import deepcopy
def mutex(path: str):
    with open(os.path.join(path), 'r', encoding='utf-8') as file:
        lines = "".join(file.readlines())
        new_line = deepcopy(lines)

    check = ['#Bar2', '#WaterTable', '#CoffeeTable', '#Bar', '#Table1', '#Table2', '#Table3', '#Coffee', '#Water',
             '#Dessert', '#Softdrink', '#BottledDrink', '#Yogurt', '#ADMilk', '#MilkDrink', '#Milk', '#VacuumCup', '#AC',
             '#ACTemperature', '#HallLight', '#TubeLight', '#Curtain', '#Chairs', '#Floor', '#Table1']
    repla = ['#另一个吧台', '#茶水桌', '#咖啡桌', '#吧台', '#第一张桌子', '#第二张桌子', '#第三张桌子', '#咖啡', '#水',
             '#点心或者甜品', '#软饮料', '#瓶装饮料', '#酸奶', '#AD钙奶', '#牛奶饮料', '#牛奶', '#保温杯', '#空调',
             '#空调温度', '#大厅灯', '#筒灯', '#窗帘', '#椅子', '#地板', '#第一张桌子']

    for i, j in zip(check, repla):
        new_line = re.sub(i, j, new_line)
    new_line = re.sub('#', '', new_line)
    lines = re.sub('#', '', lines)

    with open(os.path.join(path), 'a', encoding='utf-8') as file:
        file.write(new_line*13 + lines * 13)


# generate_goal_states(30, 6, 6)
# enumerate_goal_states(5000)
mutex(enumerate_goal_states_with_describe())
