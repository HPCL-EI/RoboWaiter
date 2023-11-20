import copy
import io
import contextlib
import os
import importlib.util

from robowaiter.utils.bt.load import load_bt_from_ptml,find_node_by_name,print_tree_from_root
from robowaiter.utils.bt.visitor import StatusVisitor

from robowaiter.behavior_tree.obtea.OptimalBTExpansionAlgorithm import Action  # 调用最优行为树扩展算法
from robowaiter.behavior_tree.obtea.opt_bt_exp_main import BTOptExpInterface

from robowaiter.behavior_lib.act.DelSubTree import DelSubTree
from robowaiter.behavior_lib._base.Sequence import Sequence
from robowaiter.utils.bt.load import load_behavior_tree_lib

from robowaiter.utils import get_root_path
root_path = get_root_path()
ptml_path = os.path.join(root_path, 'robowaiter/robot/Default.ptml')
behavior_lib_path = os.path.join(root_path, 'robowaiter/behavior_lib')



class Robot(object):
    scene = None
    response_frequency = 1

    def __init__(self,ptml_path=ptml_path,behavior_lib_path=behavior_lib_path):
        self.ptml_path = ptml_path
        self.behavior_lib_path = behavior_lib_path

        self.next_response_time = self.response_frequency
        self.step_num = 0
        self.last_tick_output = ""
        self.action_list = None


    def set_scene(self,scene=None):
        self.scene = scene


    def load_BT(self):
        self.bt = load_bt_from_ptml(self.scene, self.ptml_path,self.behavior_lib_path)
        sub_task_place_holder = find_node_by_name(self.bt.root,"SubTaskPlaceHolder()")
        if sub_task_place_holder:
            sub_task_seq = sub_task_place_holder.parent
            sub_task_seq.children.pop()
            self.scene.sub_task_seq = sub_task_seq

        self.bt_visitor = StatusVisitor()
        self.bt.visitors.append(self.bt_visitor)


    def expand_sub_task_tree(self,goal):
        if self.action_list is None:
            print("\n\n--------------------")
            print(f"首次运行行为树扩展算法")
            self.action_list = self.collect_action_nodes()
            print(f"共收集到{len(self.action_list)}个实例化动作:")
            # for a in self.action_list:
            #     if "Turn" in a.name:
            #         print(a.name)
            print("--------------------\n")

        # 如果目标是下班，规划的时候就直接快捷导入？
        end_goal = {"Is(Floor,Clean)","Is(Table1,Clean)","Is(Chairs,Clean)","Is(AC,Off)","Is(HallLight,Off)","Is(TubeLight,Off)","Is(Curtain,Off)"}
        if goal & end_goal == goal:
            tmp_list = copy.deepcopy(self.action_list)
            self.action_list=[]
            self.action_list = [action for action in tmp_list if "Turn" in action.name or "Clean" in action.name]

        algo = BTOptExpInterface(self.action_list,self.scene)

        ptml_string = algo.process(goal)

        file_name = "sub_task"
        file_path = f'./{file_name}.ptml'
        with open(file_path, 'w') as file:
            file.write(ptml_string)

        sub_task_bt = load_bt_from_ptml(self.scene, file_path,self.behavior_lib_path)

        # 加入删除子树的节点
        seq = Sequence(name="Sequence", memory=False)
        seq.add_child(sub_task_bt.root)
        del_sub_tree = DelSubTree()
        del_sub_tree.set_scene(self.scene)
        seq.add_child(del_sub_tree)

        if self.scene.sub_task_seq:
            self.scene.sub_task_seq.add_child(seq)
        else:
            print('Warning: have none sub task sequence')
            self.scene.sub_task_seq = seq
        # print("当前行为树为：")
        # print_tree_from_root(self.bt.root)
        print("行为树扩展完成！")

    # 获取所有action的pre,add,del列表
    def collect_action_nodes(self):
        action_list = []
        behavior_dict = load_behavior_tree_lib()
        for cls in behavior_dict["act"].values():
            if cls.can_be_expanded:
                print(f"可扩展动作：{cls.__name__}, 存在{len(cls.valid_args)}个有效论域组合")
                if cls.num_args == 0:
                    action_list.append(Action(name=cls.get_ins_name(),**cls.get_info()))
                if cls.num_args == 1:
                    for arg in cls.valid_args:
                        action_list.append(Action(name=cls.get_ins_name(arg), **cls.get_info(arg)))
                if cls.num_args > 1:
                    for args in cls.valid_args:
                        action_list.append(Action(name=cls.get_ins_name(*args),**cls.get_info(*args)))

        # print(action_list)
        # action_list = [
        #     Action(name='MakeCoffee', pre={'At(Robot,CoffeeMachine)'},
        #            add={'At(Coffee,Bar)'}, del_set=set(), cost=1),
        #     Action(name='MoveTo(Table)', pre={'At(Robot,Bar)'},
        #            add={'At(Robot,Table)'}, del_set=set(), cost=1),
        #     Action(name='ExploreEnv()', pre=set(),
        #            add={'EnvExplored()'}, del_set=set(), cost=1),
        # ]
        return action_list

    def step(self):
        if self.scene.time > self.next_response_time:
            self.next_response_time += self.response_frequency
            self.step_num += 1

            self.bt.tick()
            bt_output = self.bt_visitor.output_str

            if bt_output != self.last_tick_output:
                print(f"==== time:{self.scene.time:f}s ======")

                print(bt_output)

                print("\n")
                self.last_tick_output = bt_output
                return True
            else:
                return False

if __name__ == '__main__':
    pass