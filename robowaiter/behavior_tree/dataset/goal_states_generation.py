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


generate_goal_states(30, 6, 6)
