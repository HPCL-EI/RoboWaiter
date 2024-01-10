
from EXP.exp_tools import collect_action_nodes,get_start,BTTest,goal_transfer_str,collect_cond_nodes
import copy
import random
seed = 1
random.seed(seed)

action_list = collect_action_nodes(random)
# for act in action_list:
#     print(act.name,act.cost)

start_robowaiter = get_start()

# 计算state总数
num = collect_cond_nodes()
print("states num: ",num)

goal_states = []
with open('easy.txt', 'r') as file:
    for line in file:
        clean_line = line.strip()
        goal_states.append(clean_line)
print(goal_states)

# goal_set_ls=[]
# for count, goal_str in enumerate(goal_states):
#     goal = copy.deepcopy(goal_transfer_str(goal_str))
#     goal_set_ls.append(goal)
# print(goal_set_ls)

# goal_states={"On_Dessert_Bar"}
# goal_states={"On_MilkDrink_Bar2"}
# goal_states={"Is_TubeLight_On"}
# goal_states = goal_set_ls
# goal_states = {'On(VacuumCup,WaterTable)'}
# goal_states = {'At(Robot,WaterTable)'}
# goal_states = {'Is(Table1,Clean)'}

# todo: 行为树鲁棒性测试，随机生成规划问题
# # 设置生成规划问题集的超参数：文字数、解深度、迭代次数

BTTest(bt_algo_opt=True, goal_states=goal_states,action_list=action_list,start_robowaiter=start_robowaiter)
print("\n")
# 对比
BTTest(bt_algo_opt=False, goal_states=goal_states,action_list=action_list,start_robowaiter=start_robowaiter)