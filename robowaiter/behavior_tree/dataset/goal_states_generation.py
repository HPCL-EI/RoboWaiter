# the empty string '' represents robot holds nothing
Object = ['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk',
          'VacuumCup', '']

Place = ['Bar', 'WaterTable', 'CoffeeTable', 'Bar2', 'Table1', 'Table2', 'Table3']

Entity = ['Robot', 'Customer']

Operable = ['AC', 'ACTemperature', 'HallLight', 'TubeLight', 'Curtain']

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
            pattern = f'At(%s, %s)'
        case 'is':
            pattern = f'Is(%s, %s)'
        case 'hold':
            pattern = f'Holding(%s)'
        case 'on':
            pattern = f'On(%s, %s)'
        case _:
            raise RuntimeError('Incorrect predict pattern!')

    for str_1 in oplist_1:
        if oplist_2:
            for str_2 in oplist_2:
                count += 1
                res.append({pattern % (str_1, str_2)})
        else:
            count += 1
            res.append({pattern % str_1})

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

    # print(res)
    # print(len(res))

    return res


def enumerate_goal_states():
    # goal states for VLN
    count_vln, list_vln = enumerate_predict(['Robot'], Place, 'at')
    print(f'VLN 任务的目标状态数：{count_vln}')

    # goal states for VLM
    count_vlm_1, list_vlm_1 = enumerate_predict(['Robot'], Place, 'at')
    count_vlm_2, list_vlm_2 = enumerate_predict(Operable, ['0', '1'], 'is')
    print(f'VLM 任务的目标状态数：{count_vlm_1 * count_vlm_2}')

    # goal states for open-task
    count_opentask_1, list_opentask_1 = enumerate_predict(['Robot'], Place, 'at')
    count_opentask_2, list_opentask_2 = enumerate_predict(Object, Place, 'on')
    print(f'Open-task-1 任务的目标状态数：{count_opentask_1 * count_opentask_2}')


# generate_goal_states(30, 6, 6)
enumerate_goal_states()
