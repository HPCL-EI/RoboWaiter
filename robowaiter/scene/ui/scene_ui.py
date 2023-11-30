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

from robowaiter.scene.scene import Scene

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

from robowaiter.utils import get_root_path
root_path = get_root_path()


from robowaiter.utils.bt.draw import render_dot_tree


class SceneUI(Scene):
    scene_queue = None
    ui_queue = None
    scene_flag=2
    walker_followed = False
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
        self.gen_obj()
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
            cur_obstacle_world_points, cur_objs_id, obj_detect_count = self.navigation_move(self, cur_objs, cur_obstacle_world_points,
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


            semantic_info_str = ""
            # semantic_info_str += f'检测行人数量：{walker_detect_count}' + "\n\n"
            semantic_info_str += f'检测物体数量：{obj_detect_count}' + "\n\n"
            semantic_info_str += f'更新语义信息：{new_add_info}' + "\n\n"
            semantic_info_str += f'已存语义信息：{self.infoCount}' + "\n"

            self.infoCount = added_info

            # print("======semantic_info_str===========")

            self.ui_func(("get_semantic_info", semantic_info_str))
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
            (13, self.customer_say, (0, "我想坐高脚凳子。")),
            (3, self.customer_say, (0, "你带我去吧。")),
            (60, self.control_walker, (0, False, 100, -250, 480, -90)), #45
            (-1, self.customer_say, (0, "谢谢你！这儿还不错！")),
        ]

    def run_VLM(self):
        # 场景一  拿放物品
        self.gen_obj()
        self.state["condition_set"]={'At(Robot,Bar)', 'Is(AC,Off)',
                          'Holding(Nothing)', 'Exist(Yogurt)', 'Exist(BottledDrink)',
                          'Exist(Softdrink)',
                          'Exist(Chips)', 'Exist(NFCJuice)', 'Exist(Bernachon)', 'Exist(ADMilk)', 'Exist(SpringWater)'
                          'Exist(VacuumCup)', 'On(VacuumCup,Table2)',
                          'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
                          'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}

        self.add_walkers([[4,1, 880], [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
        # self.control_walkers(walker_loc=[[-55, 750], [70, -200], [250, 1200], [0, 880]],is_autowalk = True)
        self.control_walkers(walker_loc=[[-55, 750]], is_autowalk=True)
        self.signal_event_list = [
            (3, self.add_walker,  (20,0,700)),
            (1, self.control_walker, (6, False,100, 60, 520,0)),
            (1, self.customer_say, (6, "给我来份薯片和果汁，我坐在对面的水杯桌那儿。")), #给我来份薯片和果汁，我坐在对面的桌子那儿。
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


    def run_VLM_AC(self):
        # 开关空调
        # 场景二  开和调节空调温度
        self.gen_obj()
        self.add_walkers([[4,1, 880], [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
        self.control_walkers(walker_loc=[[-55, 750]],is_autowalk = True)
        self.signal_event_list = [
            (3, self.add_walker,  (0,0,700)),
            (1, self.control_walker, (6, False,100, 60, 520,0)), #[walkerID,autowalk,speed,X,Y,Yaw]
            (2, self.customer_say, (6, "好热呀，想开空调，想要温度调低点！")),
            (6, self.control_walker, (6, False, 200, 60, 80, 0)),
            (-1, self.customer_say, (6, "谢谢！这下凉快了！")),  #(-100,600)
        ]
        pass

    def run_CafeDaily(self):
        # self.run_AEM()
        self.walker_followed = False
        self.gen_obj()
        self.scene_flag = 1
        self.st1 = 3
        # self.st2 = self.st1 + 30
        # self.st3 = self.st2 + 65
        self.st2 = 3
        self.st3 = 3
        self.st4 = 3

        self.signal_event_list = [

            # 场景1：带小女孩找阳光下的空位
            (3, self.add_walker, (5, 230, 1200)),  # 0号"Girl02_C_3"
            (1, self.control_walker, (0, False, 200, 60, 520, 0)),
            (9, self.customer_say, (0, "早上好呀，我想找个能晒太阳的地方。")),
            (1, self.customer_say, (0, "你可以带我过去嘛？")),#可以带我过去嘛？
            (13, self.control_walker, (0, False, 50, 140, 1200, 180)),  # 小女孩站在了 BrightTable1 旁边就餐啦
            #
            # # # 场景2：有个胖胖男人点单交流并要咖啡，帮他送去角落的桌子
            # (3, self.add_walker, (5, 230, 1200)), # 小女孩
            # # # 上述准备
            (10, self.add_walker, (26, -28, -150, 90)),
            (0, self.add_walker, (10, -70, -200, -45)),
            (9, self.customer_say, (1, "嘿，RoboWaiter，过来一下！")),
            (10, self.control_walkers_and_say, ([[[1, False, 100, -18, -200, -90, "你们这有什么饮料嘛？"]]])), #6
            # 20 胖胖男到了 BrightTable6
            (2, self.customer_say, (1, "咖啡有哪些呢？")),  # 10
            (2, self.customer_say, (1, "来杯卡布奇诺吧。")),  # 15

            # # 场景3：有位女士要杯水和冰红茶
            # (0, self.add_walker, (5, 230, 1200)),
            # (0, self.add_walker, (26, -30, -200, -90)),
            # (0, self.add_walker, (10, -80, -180, -45)),
            #############
            (3, self.add_walkers,
             ([[[21, 65, 1000, -90], [32, -80, 850, 135], [1, 60, 420, 135], [29, -290, 400, 180]]])),
            (0, self.control_walker, (5, True, 50, 250, 1200, 180)),  # 设置id=4 的2小男孩随机游走红随机游走
            (0, self.add_walker, (48, 60, 520, 0)),  # 生成他妈妈
            (0, self.add_walkers, ([[[48, 60, 520, 0], [31, 60, 600, -90], [20, 60, 680, -90], [9, 60, 760, -90]]])),
            (50, self.customer_say, (7, "哎呦，今天这么多人，还有空位吗？")),  # 女士问 50
            (10, self.customer_say, (7, "我带着孩子呢，想要宽敞亮堂的地方。")),  # 女士问
            (8, self.customer_say, (7, "大厅的桌子好啊，快带我去呀！")),
            (15, self.control_walker, (7, False, 50, -250, 480, 0)),  # #290, 400
            (3, self.customer_say, (7, "我想来杯水，帮我孩子拿个酸奶吧。")),
            # # ### 9号灰色男 排队排着排着，不排了
            (0, self.control_walker, (10, False, 100, 100, 760, 180)),
            (0, self.control_walker, (10, True, 100, 0, 0, 180)),
            (110, self.customer_say, (7, "谢谢你的水和酸奶！")),  # 倒水+取放酸奶 90s 这次是110

            # # # 场景4：三人排队点单，女士要保温杯
            # (0, self.add_walker, (5, 230, 1200)),
            # (0, self.add_walker, (26, -30, -200, -90)),
            # (0, self.add_walker, (10, -80, -180, -45)),
            # (0, self.add_walker, (21, 65, 1000, -90)),  # 男 'BrightTable2': (65, 1000, 135),
            # (0, self.add_walker, (32, -80, 850, 135)),
            # (0, self.add_walker, (1, 60, 220, 135)),
            # (0, self.add_walker, (48, 60, 320, 0)),
            # (0, self.add_walker, (31, 60, 600, -90)), # 女红色排队 7号找保温杯的顾客
            # (0, self.add_walker, (20, 60, 680, -90)),  # 大胖男排队
            # (0, self.add_walker, (9, 60, 760, -90)), # 男灰黑色排队
            # (0, self.add_walker, (29, -290, 400, 180)), # # 青色女人占了位置 BrightTable5
            # # # # # # 上述准备 10开始
            (10, self.control_walkers_and_say, ([[[8, False, 100, 60, 520, 180, "我昨天保温杯好像落在你们咖啡厅了，你看到了吗？"]]])),
            (9, self.customer_say, (8,"你可以帮我拿来吗，我在前门的桌子前等你。")),
            (1, self.control_walker,(8, False, 80, -10, 520, 90)),# 红女士在吧台前后退一步
            (1, self.control_walker, (8, False, 80, 240, 1000, -45)), # 红女士走到Table1前
            (1, self.control_walker, (9, False, 100, 60, 600, -90)), # 大胖男排队往前走一步
            (2, self.control_walker, (10, False, 100, 60, 680, -90)), # 男灰黑色排队往前走一步
            (15, self.customer_say, (8,"就是这个杯子！找到啦，好开心！")), # 红女士在Table1前
            (5, self.customer_say, (8, "不用了。")),  # 红女士在Table1前


            (8, self.remove_walkers, ([[0, 7, 8]])),
            (3, self.control_walker, (6, False, 100, 60, 520, 0)), # 10号变7号 男灰黑色排队往前,轮到他
            (8, self.customer_say, (6, "还有酸奶吗")),
            (8, self.customer_say, (6, "那好吧，那就先把窗帘给我关上，再开个空调")),
            (35, self.control_walkers_and_say, ([[[6, True, 100, 60, 520, 0, "谢谢，这下凉快了"]]])),


            # # 场景8 结束了，删除所有顾客。此处增加自主探索发现空间比较暗，打开大厅灯
            (28, self.clean_walkers,()),
            (1, self.add_walker, (17, 60, 1000)),# 增加警察，提醒下班啦
            (3, self.control_walkers_and_say, ([[[0, False, 150, 60, 520, 0, "下班啦！别忘了打扫卫生。"]]])),
            (10, self.control_walker, (0, False, 100, 60, 1000, 0)),
            (4, self.clean_walkers, ())

        ]


        pass


    def run_reset(self):
        self.gen_obj()
        pass

    def init_robot(self):
        # init robot

        if self.robot:
            self.robot.set_scene(self)
            self.robot.load_BT()
            self.draw_current_bt()

    def draw_current_bt(self):
        render_dot_tree(self.robot.bt.root,target_directory=self.output_path,name="current_bt",png_only=True)
        self.ui_queue.put(('draw_from_file',"img_view_bt", f"{self.output_path}/current_bt.png"))
        # self.ui_queue.put(('draw_from_file', "img_view_bt", f"{self.output_path}/current_bt.svg"))

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
        if self.scene_flag == 1:
            # 如果机器人不在 吧台
            if self.walker_followed:
                return
            end = [self.status.location.X, self.status.location.Y]
            if end[1] >= 600 or end[1] <= 450 or end[0] >= 250:
                # if int(self.status.location.X)!=247 or  int(self.status.location.X)!=520:
                self.walker_followed = True
                self.control_walkers_and_say([[0, False, 150, end[0], end[1], 90, "谢谢！"]])
                self.scene_flag += 1


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

