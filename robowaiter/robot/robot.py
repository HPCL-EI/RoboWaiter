import io
import contextlib

from robowaiter.utils.bt.load import load_bt_from_ptml, find_node_by_name, print_tree_from_root
from robowaiter.utils.bt.visitor import StatusVisitor

from robowaiter.behavior_tree.obtea.OptimalBTExpansionAlgorithm import Action  # 调用最优行为树扩展算法
from robowaiter.behavior_tree.obtea.opt_bt_exp_main import BTOptExpInterface

from robowaiter.behavior_lib.act.DelSubTree import DelSubTree
from robowaiter.behavior_lib._base.Sequence import Sequence


class Robot(object):
    scene = None
    response_frequency = 1

    def __init__(self, ptml_path, behavior_lib_path):
        self.ptml_path = ptml_path
        self.behavior_lib_path = behavior_lib_path

        self.next_response_time = self.response_frequency
        self.step_num = 0
        self.last_tick_output = ""
        self.action_list = None

    def set_scene(self, scene):
        self.scene = scene

    def load_BT(self):
        self.bt = load_bt_from_ptml(self.scene, self.ptml_path, self.behavior_lib_path)
        sub_task_place_holder = find_node_by_name(self.bt.root, "SubTaskPlaceHolder")
        if sub_task_place_holder:
            sub_task_seq = sub_task_place_holder.parent
            sub_task_seq.children.pop()
            self.scene.sub_task_seq = sub_task_seq

        self.bt_visitor = StatusVisitor()
        self.bt.visitors.append(self.bt_visitor)

    def expand_sub_task_tree(self, goal):
        if self.action_list is None:
            self.action_list = self.collect_action_nodes()
            print(f"首次运行行为树扩展算法，收集到{len(self.action_list)}个有效动作")

        algo = BTOptExpInterface(self.action_list)

        ptml_string = algo.process(goal)

        file_name = "sub_task"
        file_path = f'./{file_name}.ptml'
        with open(file_path, 'w') as file:
            file.write(ptml_string)

        sub_task_bt = load_bt_from_ptml(self.scene, file_path, self.behavior_lib_path)

        # 加入删除子树的节点
        seq = Sequence(name="Sequence", memory=False)
        seq.add_child(sub_task_bt.root)
        del_sub_tree = DelSubTree()
        del_sub_tree.set_scene(self.scene)
        seq.add_child(del_sub_tree)

        self.scene.sub_task_seq.add_child(seq)
        print("当前行为树为：")
        print_tree_from_root(self.bt.root)

    def collect_action_nodes(self):
        action_list = [
            Action(name='MakeCoffee()', pre={'At(Robot,CoffeeMachine)'},
                   add={'At(Coffee,Bar)'}, del_set=set(), cost=1),
            Action(name='MoveTo(Table)', pre={'At(Robot,Bar)'},
                   add={'At(Robot,Table)'}, del_set=set(), cost=1),
            Action(name='ExploreEnv()', pre={'At(Robot,Bar)'},
                   add={'EnvExplored()'}, del_set=set(), cost=1),
        ]
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


if __name__ == '__main__':
    pass
