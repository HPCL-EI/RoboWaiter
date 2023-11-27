"""
UI场景
"""
import sys
import json
import math
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
import pickle
import time
import os

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

from robowaiter.utils import get_root_path
root_path = get_root_path()

from robowaiter.scene.scene import Scene
from robowaiter.utils.bt.draw import render_dot_tree


class SceneUI(Scene):
    scene_queue = None
    ui_queue = None
    # camera_interval = 4
    def __init__(self, robot,scene_queue,ui_queue):
        self.scene_queue = scene_queue
        self.ui_queue = ui_queue

        super().__init__(robot)
        # 在这里加入场景中发生的事件
        self.show_ui = True

        # while True:
        #     if not self.scene_queue.empty():
        #         param = self.scene_queue.get()
        #         # 处理参数...

        # self.ui_queue.put(('say',"test"))
        self.stoped = False

    def run(self):
        # 基类run
        self._run()
        # 运行并由robot打印每步信息
        while not self.stoped:
            self.step()

    def _run(self):
        pass

    def run_AEM(self):
        print(len(self.status.objects))
        # 创建一个从白色（1）到灰色（0）的 colormap
        objs = self.status.objects
        cur_objs = []
        cur_obstacle_world_points = []
        visited_obstacle = set()
        obj_json_data = []
        obj_count = 0
        added_info = 0
        map_ratio = self.map_ratio
        db = DBSCAN(eps=map_ratio, min_samples=int(map_ratio / 2))
        file_name = os.path.join(root_path, 'robowaiter/proto/map_1.pkl')
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                map = pickle.load(file)
        print('------------ 自主探索 ------------')
        while True:
            walker_count = 0
            fig = plt.figure()
            goal = self.explore(map, 120)
            if goal is None:
                break
            # cur_obstacle_world_points, cur_objs_id = self.navigation_move(plt, cur_objs, cur_obstacle_world_points,
            #                                                               [[goal[0], goal[1]]], map_ratio, db, 0, 11)
            cur_obstacle_world_points, cur_objs_id = self.navigation_move(self, cur_objs, cur_obstacle_world_points,
                                                                          [[goal[0], goal[1]]], map_ratio, db, 0, 11)
            for point in cur_obstacle_world_points:
                if point[0] < -350 or point[0] > 600 or point[1] < -400 or point[1] > 1450:
                    continue
                self.map_map[math.floor((point[0] + 350) / map_ratio), math.floor((point[1] + 400) / map_ratio)] = 1
                visited_obstacle.add(
                    (math.floor((point[0] + 350) / map_ratio), math.floor((point[1] + 400) / map_ratio)))
            for i in range(len(cur_objs_id)):
                if cur_objs_id[i] == "walker":
                    walker_count += 1
                for obj in objs:
                    if obj.name == cur_objs_id[i] and obj not in cur_objs:
                        cur_objs.append(obj)
                        break
            # plt.subplot(2, 1, 2)  # 这里的2,1表示总共2行，1列，2表示这个位置是第2个子图
            # plt.imshow(self.map_map, cmap='binary', alpha=0.5, origin='lower',
            #            extent=(-400 / map_ratio, 1450 / map_ratio,
            #                    -350 / map_ratio, 600 / map_ratio))
            # new_map = self.updateMap(cur_obstacle_world_points)
            self.draw_map(plt, self.map_map)
            plt.axis("off")
            self.send_img("img_label_map")
            # plt.title("地图构建过程")
            # self.send_img("img_label_map")
            # plt.subplot(2, 7, 14)  # 这里的2,1表示总共2行，1列，2表示这个位置是第2个子图

            # walker_count 新增行人信息

            # 新增语义信息
            new_add_info = len(cur_objs) - added_info + walker_count
            # plt.text(0, 0.5, f'新增语义信息：{new_add_info}', fontsize=10)  # 在图中添加文字，x和y坐标是在这个图片大小内的相对位置，fontsize是字体大小

            # 已存语义信息
            added_info += new_add_info
            # plt.text(0, 0.3, f'已存语义信息：{added_info}', fontsize=10)  # 在图中添加文字，x和y坐标是在这个图片大小内的相对位置，fontsize是字体大小
            self.infoCount = added_info
            plt.axis("off")
            # plt.show()
            print("------------当前检测到的物品信息--------------")
            print(cur_objs)
            time.sleep(1)

        for i in range(len(cur_objs)):
            if cur_objs[i].name == "Desk" or cur_objs[i].name == "Chair":
                obj_json_data.append(
                    {"id": f"{i}", "name": f"{cur_objs[i].name}", "location": f"{cur_objs[i].location}",
                     "height": f"{cur_objs[i].location.Z * 2}"})

            else:
                obj_json_data.append(
                    {"id": f"{i}", "name": f"{cur_objs[i].name}", "location": f"{cur_objs[i].location}",
                     "height": f"{cur_objs[i].location.Z}"})
        file_json_name = os.path.join(root_path, 'robowaiter/proto/objs.json')
        with open(file_json_name, 'w') as file:
            json.dump(obj_json_data, file)


        print("已绘制完成地图！！！")
        print("------------检测到的所有物品信息--------------")
        print(obj_json_data)

    def run_VLN(self):
        self.gen_obj()
        self.add_walkers([
            [29, 60, 520],  # 顾客 0
            [23, 0, 220],  # 秃头老头子  1
            [0, -55, 150],  # 小男孩d走来走去 2
            [10, -55, 750],  # 3
            [19, 70, -200],  # 后门站着不动的 4
            [21, 65, 1000, -90],  # 大胖男占了一号桌 5
            [5, 230, 1200],  # 小女孩 6
            [26, -28, -10, 90],
            # [26, 60, 0, 90],
            # [26, -28, 0, 90] , #在设置一个在后门随机游走的 7
            # 设置为 26, 60, 0, 90]
            [31, 280, 1200, -45]  # 8
        ])
        self.control_walker(2, True, 200, -55, 155, 90)  # 飞速奔跑的小男孩
        # self.control_walker(7, True, 80, -25, -150, 90)
        self.control_walker(5, True, 65, 995, 520, 90)
        self.control_walker(4, True, 65, 70, -200, 90)

        self.new_event_list = [
            (5, self.customer_say, (0, "请问哪里有空位啊？")),
            (13, self.customer_say, (0, "我想坐高凳子。")),
            (3, self.customer_say, (0, "你带我去吧。")),
            (45, self.control_walker, (0, False, 100, -250, 480, -90)),
            (-1, self.customer_say, (0, "谢谢你！这儿还不错！")),
        ]

    def run_VLM(self):
        self.gen_obj()
        self.add_walkers([[4,1, 880], [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
        self. control_walkers(walker_loc=[[-55, 750], [70, -200], [250, 1200], [0, 880]],is_autowalk = True)
        self.signal_event_list = [
            (3, self.add_walker,  (20,0,700)),
            (1, self.control_walker, (6, False,100, 60, 520,0)),
            (1, self.customer_say, (6, "给我来份薯片和果汁，我坐在对面的桌子那儿。")),
            (5, self.control_walker, (6, False, 100, -250, 480, 0)),
        ]
        pass

    def run_GQA(self):
        self.gen_obj()
        self.add_walkers([ [16,250, 1200],[6,-55, 750],[10,70, -200],[47,-290, 400, 180],[26, 60,-320,90]])
        self.control_walker(1, True, 100, 60, 720, 0)
        self.control_walker(4, True, 100, 60, -120, 0)
        self.add_walkers([[31, 60,500,0], [15,60,550,0]])
        self.signal_event_list = [
            (5, self.customer_say, (6, "你好呀，你们这有啥好吃的？")), # 男
            (8, self.customer_say, (6, "听起来都好甜呀，我女朋友爱吃水果。")),
            (15, self.customer_say, (6, "你们这人可真多。")),
            (15, self.customer_say, (6, "我女朋友怕晒，有空余的阴凉位置嘛？")),
            (20, self.customer_say, (6, "那还不错。")),
            (15, self.customer_say, (5, "请问洗手间在哪呢？")),
            (20, self.customer_say, (5, "我们还想一起下下棋,切磋切磋。")),
            (20, self.customer_say, (6, "太棒啦，亲爱的。")),
            (15, self.customer_say, (5, "那你知道附近最近的电影院在哪吗?")),
            (20, self.customer_say, (6, "谢啦，那我们先去阴凉位置下个棋，等电影开始了就去看呢!")),
        ]
        pass

    def run_OT(self):
        self.gen_obj()
        self.add_walkers([ [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
        self.control_walker(1, True, 100, 60, 720, 0)
        self.control_walker(4, True, 100, 60, -120, 0)
        self.add_walkers([[16,60, 520], [47,-40, 520]])
        self.signal_event_list = [
            (8, self.customer_say, (5, "给我来杯咖啡，哦对，再倒一杯水。")),
            (1, self.control_walker_ls,([[[5, False, 100, -250, 480, 0],[6, False, 100, 60, 520, 0]]])),
            (-1, self.customer_say, (5, "感谢，这些够啦，你去忙吧。")),
            (10, self.customer_say, (6, "我想来份点心和酸奶。")),
            (-1, self.customer_say, (6, "真美味啊！")),
        ]
        pass

    def run_AT(self):
        self.add_walker(23, 60, 520, 0)
        self.signal_event_list = [
            (2, self.customer_say, (0,"可以关筒灯和关窗帘吗？")),
        ]
        pass

    def run_reset(self):
        pass

    def init_robot(self):
        # init robot

        if self.robot:
            self.robot.set_scene(self)
            self.robot.load_BT()
            self.draw_current_bt()

    def draw_current_bt(self):
        render_dot_tree(self.robot.bt.root,target_directory=self.output_path,name="current_bt")
        self.ui_queue.put(('draw_from_file',"img_view_bt", f"{self.output_path}/current_bt.png"))

    def ui_func(self,args):
        # _,_,output_path = args
        # plt.savefig(output_path)

        self.ui_queue.put(args)

    def _reset(self):
        pass

    def _step(self):
        # print("已运行")
        self.handle_queue_messages()
        # if len(self.sub_task_seq.children) == 0:
        #     question = input("请输入指令：")
        #     if question[-1] == ")":
        #         print(f"设置目标:{question}")
        #         self.new_set_goal(question)
        #     else:
        #         self.customer_say("System",question)


    def handle_queue_messages(self):
        while not self.scene_queue.empty():
            message = self.scene_queue.get()
            function_name = message[0]
            function = getattr(self, function_name, None)

            args = []
            if len(message)>1:
                args = message[1:]

            result = function(*args)

    def stop(self):
        self.stoped = True

if __name__ == '__main__':
    from robowaiter.robot.robot import Robot

    robot = Robot()
    ui = UI(Robot)

    # create task
    # task = SceneUI(robot,ui)

