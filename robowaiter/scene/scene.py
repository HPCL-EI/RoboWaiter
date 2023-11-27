import io
import pickle
import sys
import time
import grpc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

from robowaiter.proto import camera
from robowaiter.proto import semantic_map
from robowaiter.algos.navigator.navigate import Navigator
import math
from robowaiter.proto import GrabSim_pb2
from robowaiter.proto import GrabSim_pb2_grpc
import copy
import os
from robowaiter.utils import get_root_path
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
from robowaiter.algos.navigator.dstar_lite import euclidean_distance
from PIL import Image
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

root_path = get_root_path()

channel = grpc.insecure_channel(
    "localhost:30001",
    options=[
        ("grpc.max_send_message_length", 1024 * 1024 * 1024),
        ("grpc.max_receive_message_length", 1024 * 1024 * 1024),
    ],
)
animation_step = [4, 5, 7, 3, 3]
loc_offset = [-700, -1400]



def show_image(camera_data):
    print('------------------show_image----------------------')
    # 获取第0张照片
    im = camera_data.images[0]
    # 使用numpy(np) 数值类型矩阵的frombuffer，将im.data以流的形式（向量的形式）读入，在变型reshape成三位矩阵的形式(长度，宽度，深度)即三阶张量
    d = np.frombuffer(im.data, dtype=im.dtype).reshape((im.height, im.width, im.channels))
    # matplotlib中的plt方法 对矩阵d 进行图形绘制，如果 深度相机拍摄的带深度的图片（图片名字中有depth信息），则转换成黑白图即灰度图
    plt.imshow(d, cmap="gray" if "depth" in im.name.lower() else None)
    # 图像展示在屏幕上
    # plt.show()

    return d


class Scene:
    robot = None
    event_list = []
    new_event_list = []
    signal_event_list = []
    # show_bubble = True
    event_signal = "None"
    # step_interval = 1
    # camera_interval = 1.5
    output_path = os.path.join(os.path.dirname(__file__), "outputs")

    default_state = {
        "map": {
            "2d": None,
            "obj_pos": {}
        },
        "chat_list": [],  # 未处理的顾客的对话, (顾客的位置,顾客对话的内容)
        "sub_goal_list": [],  # 子目标列表
        "status": None,  # 仿真器中的观测信息，见下方详细解释
        "condition_set": {'At(Robot,Bar)', 'Is(AC,Off)',
                          'Holding(Nothing)', 'Exist(Yogurt)', 'Exist(BottledDrink)',
                          'Exist(Softdrink)',
                          # 'On(Yogurt,Bar)','On(BottledDrink,Bar)',
                          # 'Exist(Softdrink)', 'On(Softdrink,Table1)',
                          'Exist(Chips)', 'Exist(NFCJuice)', 'Exist(Bernachon)', 'Exist(ADMilk)', 'Exist(SpringWater)'
                          
                          'Exist(VacuumCup)', 'On(VacuumCup,Table2)',
                          'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
                          'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'},
        "obj_mem": {},
        "customer_mem": {},
        "served_mem": {},
        "greeted_customers": set(),
        "attention": {},
        "serve_state": {},
        "chat_history": {},
        "wait_history": set(),
        "anomaly": None
    }
    """
    status:
        location: Dict[X: float, Y: float]
        rotation: Dict[Yaw: float]
        joints: List[Dict[name: str, location: Dict[X: float, Y: float, Z: float]]]
        fingers: List[Dict[name: str, location: List[3 * Dict[X: float, Y: float, Z: float]]]]
        objects[:-1]: List[Dict[name: str, location: Dict[X: float, Y: float, Z: float]]]
        objects[-1]: Dict[name: "Hand", boxes: List[Dict[diagonals: List[4 * Dict[X0: float, Y0: float, Z0: float, X1: float, Y1: float, Z1: float]]]]]
        walkers: List[name: str, pose: Dict[X: float, Y: float, Yaw: float], speed: float, target: Dict[X: float, Y: float, Yaw: float]]
        timestamp: int, timestep: int
        collision: str, info: str
    """

    def __init__(self, robot=None, sceneID=0):
        self.stub = GrabSim_pb2_grpc.GrabSimStub(channel)


        self.robot = robot

        self.sceneID = sceneID
        self.use_offset = False
        self.start_time = time.time()
        self.time = 0
        self.sub_task_seq = None
        os.makedirs(self.output_path,exist_ok=True)

        self.show_bubble = True
        # 是否展示UI
        self.show_ui = False
        # 图像分割
        self.take_picture = False
        self.map_ratio = 5
        self.map_map = np.zeros((math.ceil(950 / self.map_ratio), math.ceil(1850 / self.map_ratio)))
        self.db = DBSCAN(eps=self.map_ratio, min_samples=int(self.map_ratio / 2))
        self.infoCount = 0

        self.is_nav_walk = False

        file_name = os.path.join(root_path,'robowaiter/algos/navigator/map_5.pkl')
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                self.map_map_real = pickle.load(file)



        self.robot_changed = False
        self.last_event_time = 0
        self.last_camera_time = -99999
        self.last_step_time = -99999

        self.img_cache = {
            "img_label_canvas":None,
            "img_label_seg":None,
            "img_label_obj":None,
            "img_label_map":None,
        }

        # 1-7 正常执行, 8-10 控灯操作移动到6, 11-12窗帘操作不需要移动,
        self.op_dialog = ["", "制作咖啡", "倒水", "夹点心", "拖地", "擦桌子", "开筒灯", "搬椅子",  # 1-7
                          "关筒灯", "开大厅灯", "关大厅灯", "关闭窗帘", "打开窗帘",  # 8-12
                          "调整空调开关", "调高空调温度", "调低空调温度",  # 13-15
                          "抓握物体", "放置物体"]  # 16-17
        # 动画控制的执行步骤数
        self.op_act_num = [0, 3, 4, 6, 3, 2, 0, 1,
                           0, 0, 0, 0, 0,
                           0, 0, 0,
                           0, 0]
        # 动画控制的执行区域坐标
        self.op_v_list = [[0.0, 0.0], [250.0, 310.0], [-70.0, 480.0], [250.0, 630.0], [-70.0, 740.0], [260.0, 1120.0],
                          [300.0, -220.0],
                          [0.0, -70.0]]
        self.op_typeToAct = {8: [6, 2], 9: [6, 3], 10: [6, 4], 11: [8, 1], 12: [8, 2]}  # 任务类型到行动的映射
        self.obj_loc = [300.5, -140.0, 114]  # 空调面板位置

        # AEM
        self.visited = set()
        self.all_frontier_list = set()
        self.semantic_map = semantic_map
        self.auto_map = np.ones((800, 1550))
        self.filename = os.path.join(root_path, 'robowaiter/proto/map_1.pkl')
        with open(self.filename, 'rb') as file:
            self.map_file = pickle.load(file)

        self.colors = [
            'red',
            'pink',
            'purple',
            'blue',
            'cyan',
            'green',
            'yellow',
            'orange',
            'brown',
            'gold',
        ]

        # tool register
        self.all_loc_en = ['bar', 'Table', 'sofa', 'stove', 'Gate', 'light switch', 'airconditioner switch', 'cabinet',
                           'bathroom', 'window', 'audio',
                           'lounge area', 'workstation', 'service counter', 'cashier counter', 'corner', 'cake display',
                           'ChargingStations',
                           'refrigerator', 'bookshelf']

        self.loc_map_en = {'bar': {'工作台', '服务台', '收银台', '蛋糕柜'}, 'Table': {'大门', '休闲区', '墙角'},
                           'sofa': {'餐桌', '窗户', '音响', '休闲区', '墙角', '书架'},
                           'stove': {'吧台', '橱柜', '工作台', '服务台', '收银台', '蛋糕柜', '冰箱'},
                           'Gate': {'吧台', '灯开关', '空调开关', '卫生间', '墙角'},
                           'light switch': {'大门', '空调开关', '卫生间', '墙角'},
                           'airconditioner switch': {'大门', '灯开关', '卫生间', '墙角'},
                           'cabinet': {'灶台', '吧台', '工作台', '服务台', '收银台', '蛋糕柜', '充电处', '冰箱'},
                           'bathroom': {'大门', '墙角'},
                           'window': {'餐桌', '沙发', '休闲区'}, 'audio': {'餐桌', '沙发', '休闲区', '墙角', '书架'},
                           'lounge area': {'沙发', '餐桌', '墙角', '书架', '音响'},
                           'workstation': {'吧台', '服务台', '收银台'},
                           'service counter': {'吧台', '工作台', '收银台'},
                           'cashier counter': {'吧台', '工作台', '服务台'},
                           'corner': {'卫生间', '沙发', '灯开关', '空调开关', '音响', '休闲区', '书架'},
                           'cake display': {'吧台', '橱柜', '服务台', '收银台', '冰箱'},
                           'ChargingStations': {'吧台', '餐桌', '沙发', '休闲区', '工作台', '服务台', '收银台', '墙角',
                                                '书架'},
                           'refrigerator': {'吧台', '服务台', '蛋糕柜'},
                           'bookshelf': {'餐桌', '沙发', '窗户', '休闲区', '墙角'}}

        self.obstacle_objs_id = [114, 115, 122, 96, 102, 83, 121, 105, 108, 89, 100, 90,
                            111, 103, 95, 92, 76, 113, 101, 29, 112, 87, 109, 98,
                            106, 120, 97, 86, 104, 78, 85, 81, 82, 84, 91, 93, 94,
                            99, 107, 116, 117, 118, 119, 255, 251]
        self.not_key_objs_id = {255, 254, 253, 107, 81}

        self.init_algos()  # 初始化各种算法类


    def init_world(self,scene_num=1, mapID=11):
        self.stub.SetWorld(GrabSim_pb2.BatchMap(count=scene_num, mapID=mapID))
        time.sleep(3)  # wait for the map to load

    def get_camera(self,part, scene_id=0):
        # print('------------------get_camera----------------------')
        action = GrabSim_pb2.CameraList(cameras=part, scene=scene_id)
        return self.stub.Capture(action)

    def init_robot(self):
        # init robot

        if self.robot:
            self.robot.set_scene(self)
            self.robot.load_BT()

    def init_algos(self):
        '''
            初始化各种各种算法
        '''
        # map_file = os.path.join(root_path, 'robowaiter/algos/navigator/map_5.pkl')
        # with open(map_file, 'rb') as file:
        #     map = pickle.load(file)

        # 初始化探索、导航、操作
        self.navigator = Navigator(scene=self, area_range=[-350, 600, -400, 1450], map=copy.deepcopy(self.map_map_real), scale_ratio=5)
        # self.explorer
        # self.manipulator


    def reset(self):
        # 基类reset，默认执行仿真器初始化操作
        self.reset_sim()
        self.init_robot()
        self.init_algos()

        # reset state
        self.state = copy.deepcopy(self.default_state)

        self._reset()
        print("场景初始化完成")

        self.running = True

    def run(self):
        # 基类run
        self._run()
        # 运行并由robot打印每步信息
        while True:
            self.step()

    def step(self):
        # 基类step，默认执行行为树tick操作
        self.time = time.time() - self.start_time

        # if self.time - self.last_step_time > self.step_interval:
        self.deal_event()
        self.deal_new_event()
        self.deal_signal_event()
        self._step()
        self.robot_changed = self.robot.step()
        self.last_step_time = self.time

    def deal_new_event(self):
        if len(self.new_event_list) > 0:
            next_event = self.new_event_list[0]
            t, func, args = next_event
            if self.time >= t:
                print(f'event: {t}, {func.__name__}')
                self.new_event_list.pop(0)
                func(*args)

    def deal_signal_event(self):
        if len(self.signal_event_list) > 0:
            next_event = self.signal_event_list[0]
            t, func, args = next_event
            if t < 0:  # 一直等待机器人行动，直到机器人无行动
                if self.robot_changed:
                    return
            if (t >= 0) and (self.time - self.last_event_time < t):
                return

            print(f'event: {t}, {func.__name__}')
            self.signal_event_list.pop(0)
            self.last_event_time = self.time
            func(*args)

    def deal_event(self):
        if len(self.event_list) > 0:
            next_event = self.event_list[0]
            t, func = next_event
            if self.time >= t:
                print(f'event: {t}, {func.__name__}')
                self.event_list.pop(0)
                func()

    def create_chat_event(self, sentence):
        def customer_say():
            print(f'{sentence}')
            if self.show_bubble:
                self.chat_bubble(f'{sentence}')
            self.state['chat_list'].append(f'{sentence}')

        return customer_say

    def set_goal(self, goal):
        g = eval("{'" + goal + "'}")

        def set_sub_task():
            self.state['chat_list'].append(("Goal", g))

        return set_sub_task


    def new_set_goal(self,goal):
        self.state['chat_list'].append(("Goal",goal))


    @property
    def status(self):
        return self.stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))

    def reset_sim(self):
        # reset world
        self.stub.CleanWalkers(GrabSim_pb2.SceneID(value=self.sceneID))
        self.init_world()
        self.stub.Reset(GrabSim_pb2.ResetParams(scene=self.sceneID))

    def _reset(self):
        # 场景自定义的reset
        pass

    def _run(self):
        # 场景自定义的run
        pass

    def _step(self):
        # 场景自定义的step
        pass

    def walker_control_generator(self, walkerID, autowalk, speed, X, Y, Yaw):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        return GrabSim_pb2.WalkerControls.WControl(
            id=walkerID,
            autowalk=autowalk,
            speed=speed,
            pose=GrabSim_pb2.Pose(X=X, Y=Y, Yaw=Yaw),
        )

    def walk_to(self, X, Y, Yaw=100, velocity=200, dis_limit=0):
        walk_v = [X, Y, Yaw, velocity, dis_limit]
        action = GrabSim_pb2.Action(
            scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v
        )
        scene = self.stub.Do(action)

        return scene

    def walker_walk_to(self, walkerID, X, Y, speed=50, Yaw=0):
        self.control_walker(
            [self.walker_control_generator(walkerID=walkerID, autowalk=False, speed=speed, X=X, Y=Y, Yaw=Yaw)])

    def reachable_check(self, X, Y, Yaw):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        navigation_info = self.stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.WalkTo,
                values=[X, Y, Yaw],
            )
        ).info
        if navigation_info == "Unreachable":
            return False
        else:
            return True

    def add_walker(self, id, x, y, yaw=0, v=0, scope=100):
        loc = [x, y, yaw, v, scope]
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=loc)
        scene = self.stub.Do(action)
        # print(scene.info)
        walker_list = []
        if (str(scene.info).find('unreachable') > -1):
            print('当前位置不可达,无法初始化NPC')
        else:
            walker_list.append(
                GrabSim_pb2.WalkerList.Walker(id=id, pose=GrabSim_pb2.Pose(X=loc[0], Y=loc[1], Yaw=loc[2])))
        self.stub.AddWalker(GrabSim_pb2.WalkerList(walkers=walker_list, scene=self.sceneID))

        w = self.status.walkers
        num_customer = len(w)
        name = w[-1].name
        self.state["customer_mem"][name] = num_customer - 1

        self.ui_func(("add_walker",name))


    def walker_index2mem(self, index):
        for mem, i in self.state["customer_mem"].items():
            if index == i:
                return mem

    def add_walkers(self, walker_loc=[[0, 880], [250, 1200], [-55, 750], [70, -200]]):
        print('------------------add_walkers----------------------')
        for i, walker in enumerate(walker_loc):
            if len(walker) == 2:
                self.add_walker(i, walker[0], walker[1])
            elif len(walker) == 3:
                self.add_walker(walker[0], walker[1], walker[2])
            elif len(walker) == 4:
                self.add_walker(walker[0], walker[1], walker[2], walker[3])
            elif len(walker) == 5:
                self.add_walker(walker[0], walker[1], walker[2], walker[3], walker[4])

    def remove_walker(self, *args):  # take single walkerID or a list of walkerIDs
        remove_list = []
        if isinstance(args[0], list):
            remove_list = args[0]
        else:
            for walkerID in args:
                # walkerID is the index of the walker in status.walkers.
                # Since status.walkers is a list, some walkerIDs would change after removing a walker.
                remove_list.append(walkerID)

        self.stub.RemoveWalkers(GrabSim_pb2.RemoveList(IDs=remove_list, scene=self.sceneID))
        self.state["customer_mem"] = {}
        w = self.status.walkers
        for i in range(len(w)):
            self.state["customer_mem"][w[i].name] = i

    def remove_walkers(self, IDs=[0]):
        s = self.stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))
        scene = self.stub.RemoveWalkers(GrabSim_pb2.RemoveList(IDs=IDs, scene=self.sceneID))
        time.sleep(2)
        self.state["customer_mem"] = {}
        w = self.status.walkers
        for i in range(len(w)):
            self.state["customer_mem"][w[i].name] = i
        return

    def clean_walkers(self):
        scene = self.stub.CleanWalkers(GrabSim_pb2.SceneID(value=self.sceneID))
        self.state["customer_mem"] = {}
        return scene

    def control_walker(self, walkerID, autowalk, speed, X, Y, Yaw=0):

        if not isinstance(walkerID, int):
            walkerID = self.walker_index2mem(walkerID)

        pose = GrabSim_pb2.Pose(X=X, Y=Y, Yaw=Yaw)
        scene = self.stub.ControlWalkers(
            GrabSim_pb2.WalkerControls(
                controls=[GrabSim_pb2.WalkerControls.WControl(id=walkerID, autowalk=autowalk, speed=speed, pose=pose)],
                scene=self.sceneID)
        )
        return scene
        # self.stub.ControlWalkers(
        #     GrabSim_pb2.WalkerControls(controls=control_list, scene=self.sceneID)
        # )

    def control_walkers_and_say(self, control_list_ls):
        """ 同时处理行人的行走和对话
        control_list_ls =[walkerID,autowalk,speed,X,Y,Yaw,cont]
        """
        control_list = []
        for control in control_list_ls:
            if control[-1] != None:
                walkerID = control[0]

                if not isinstance(walkerID, int):
                    walkerID = self.walker_index2mem(walkerID)

                # cont = self.status.walkers[walkerID].name + ":"+control[-1]
                # self.control_robot_action(control[walkerID], 3, cont)
                self.customer_say(walkerID, control[-1])
            control_list.append(
                self.walker_control_generator(walkerID=control[0], autowalk=control[1], speed=control[2], X=control[3],
                                              Y=control[4], Yaw=control[5]))
        # 收集没有对话的统一控制
        scene = self.stub.ControlWalkers(
            GrabSim_pb2.WalkerControls(controls=control_list, scene=self.sceneID)
        )
        return scene

    def control_walkers(self, walker_loc=[[-55, 750], [70, -200], [250, 1200], [0, 880]], is_autowalk=True):
        """pose:表示行人的终止位置姿态"""
        scene = self.status
        walker_loc = walker_loc
        controls = []
        for i in range(len(walker_loc)):
            loc = walker_loc[i]
            is_autowalk = is_autowalk
            pose = GrabSim_pb2.Pose(X=loc[0], Y=loc[1], Yaw=180)
            controls.append(GrabSim_pb2.WalkerControls.WControl(id=i, autowalk=is_autowalk, speed=80, pose=pose))
        scene = self.stub.ControlWalkers(GrabSim_pb2.WalkerControls(controls=controls, scene=self.sceneID))
        return scene

    def control_walker_ls(self, walker_loc=[[-55, 750], [70, -200], [250, 1200], [0, 880]]):
        """pose:表示行人的终止位置姿态"""
        scene = self.status
        walker_loc = walker_loc
        controls = []
        for walker in walker_loc:
            if len(walker) == 2:
                self.control_walker(walker[0], walker[1])
            elif len(walker) == 3:
                self.control_walker(walker[0], walker[1], walker[2])
            elif len(walker) == 4:
                self.control_walker(walker[0], walker[1], walker[2], walker[3])
            elif len(walker) == 5:
                self.control_walker(walker[0], walker[1], walker[2], walker[3], walker[4])
            elif len(walker) == 6:
                self.control_walker(walker[0], walker[1], walker[2], walker[3], walker[4], walker[5])
        #     self.control_walker()
        # scene = self.stub.ControlWalkers(GrabSim_pb2.WalkerControls(controls=controls, scene=self.sceneID))
        # return scene
        return

    def control_joints(self, angles):
        self.stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.RotateJoints,
                values=angles,
            )
        )

    def add_object(self, type, X, Y, Z, Yaw=0):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        self.stub.AddObjects(
            GrabSim_pb2.ObjectList(
                objects=[
                    GrabSim_pb2.ObjectList.Object(x=X, y=Y, yaw=Yaw, z=Z, type=type)
                ],
                scene=self.sceneID,
            )
        )

    def remove_object(self, *args):  # refer to remove_walker
        remove_list = []
        if isinstance(args[0], list):
            remove_list = args[0]
        else:
            for objectID in args:
                remove_list.append(objectID)
        self.stub.RemoveObjects(GrabSim_pb2.RemoveList(IDs=remove_list, scene=self.sceneID))

    def clean_object(self):
        self.stub.CleanObjects(GrabSim_pb2.SceneID(value=self.sceneID))

    def grasp(self, handID, objectID):
        self.stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.Grasp,
                values=[handID, objectID],
            )
        )

    def release(self, handID):
        self.stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.Release,
                values=[handID],
            )
        )

    def get_camera_color(self, image_only=True):
        camera_data = self.stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Color], scene=self.sceneID
            )
        )
        if image_only:
            return show_image(camera_data)
        else:
            return camera_data

    def get_camera_depth(self, image_only=True):
        camera_data = self.stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Depth], scene=self.sceneID
            )
        )
        if image_only:
            return show_image(camera_data)
        else:
            return camera_data

    def get_camera_segment(self, show=True):
        camera_data = self.stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Segment], scene=self.sceneID
            )
        )
        if show:
            show_image(camera_data)

        return camera_data

    def chat_bubble(self, message):
        self.stub.ControlRobot(
            GrabSim_pb2.ControlInfo(
                scene=self.sceneID, type=0, action=1, content=message.strip()
            )
        )

    def walker_bubble(self, name, message):
        talk_content = name + ":" + message
        self.control_robot_action(0, 3, talk_content)

    def customer_say(self, name, sentence, show_bubble=True):
        if isinstance(name, int):
            name = self.walker_index2mem(name)

        # if not isinstance(walkerID, int):
        #     name = self.walker_index2mem(walkerID)

        print(f'{name} say: {sentence}')
        if self.show_bubble and show_bubble:
            self.walker_bubble(name, sentence)
        self.state['chat_list'].append((name, sentence))

    # def control_robot_action(self, scene_id=0, type=0, action=0, message="你好"):
    #     print('------------------control_robot_action----------------------')
    #     scene = self.stub.ControlRobot(
    #         GrabSim_pb2.ControlInfo(scene=scene_id, type=type, action=action, content=message))
    #     if (str(scene.info).find("Action Success") > -1):
    #         print(scene.info)
    #         return True
    #     else:
    #         print(scene.info)
    #         return False

    def animation_control(self, animation_type):
        # animation_type: 1:make coffee 2: pour water 3: grab food 4: mop floor 5: clean table
        scene = self.stub.ControlRobot(
            GrabSim_pb2.ControlInfo(scene=self.sceneID, type=animation_type, action=1)
        )
        if scene.info == "action success":
            for i in range(2, animation_step[animation_type - 1] + 1):
                self.stub.ControlRobot(
                    GrabSim_pb2.ControlInfo(
                        scene=self.sceneID, type=animation_type, action=i
                    )
                )

    def animation_reset(self):
        self.stub.ControlRobot(GrabSim_pb2.ControlInfo(scene=self.sceneID, type=0, action=0))

    # 手指移动到指定位置
    def ik_control_joints(self, handNum=2, x=30, y=40, z=80):
        # print('------------------ik_control_joints----------------------')
        # IK控制,双手, 1左手, 2右手; 暂时只动右手
        HandPostureObject = [
            GrabSim_pb2.HandPostureInfos.HandPostureObject(handNum=handNum, x=x, y=y, z=z, roll=0, pitch=0, yaw=0),
            # GrabSim_pb2.HandPostureInfos.HandPostureObject(handNum=1, x=0, y=0, z=0, roll=0, pitch=0, yaw=0),
        ]
        temp = self.stub.GetIKControlInfos(
            GrabSim_pb2.HandPostureInfos(scene=self.sceneID, handPostureObjects=HandPostureObject))

    def move_to_obj(self, obj_id):

        scene = self.status
        # 抬头
        # value = [0]*21
        # for i in range(21):
        #     value[i] = self.status.joints[i].angle
        # value[5] = 0
        # action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.RotateJoints, values=value)
        # scene = self.stub.Do(action)
        # time.sleep(1.0)

        obj_info = scene.objects[obj_id]
        # Robot
        obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
        walk_v = [obj_x + 50, obj_y] + [180, 180, 0]
        if obj_y >= 820 and obj_y <= 1200 and obj_x >= 240 and obj_x <= 500:  # 物品位于斜的抹布桌上 ([240,500],[820,1200])
            walk_v = [obj_x + 40, obj_y - 35, 130, 180, 0]
            obj_x += 3
            obj_y += 2.5
        walk_v[0] += 1
        print("walk:", walk_v)
        if self.is_nav_walk:
            self.navigator.navigate(goal=(walk_v[0], walk_v[1]), animation=False)
        else:
            action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
            scene = self.stub.Do(action)
        print("After Walk Position:", [scene.location.X, scene.location.Y, scene.rotation.Yaw])

    # 移动到进行操作任务的指定地点
    def move_task_area(self, op_type, obj_id=0, release_pos=[247.0, 520.0, 100.0]):
        scene = self.status

        # 抬头
        # value = [0]*21
        # for i in range(21):
        #     value[i] = self.status.joints[i].angle
        # value[5] = 0
        # action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.RotateJoints, values=value)
        # scene = self.stub.Do(action)
        # time.sleep(1.0)

        cur_pos = [scene.location.X, scene.location.Y, scene.rotation.Yaw]
        print("Current Position:", cur_pos, "开始任务:", self.op_dialog[op_type])
        if op_type == 11 or op_type == 12:  # 开关窗帘不需要移动
            return
        print('------------------moveTo_Area----------------------')
        if op_type < 8:  # 动画控制相关任务的移动目标
            if self.show_ui:
                self.get_obstacle_point(self.db, self.status, map_ratio=self.map_ratio)
            walk_v = self.op_v_list[op_type] + [scene.rotation.Yaw, 180, 0]
        if 8 <= op_type <= 10:  # 控灯相关任务的移动目标
            if self.show_ui:
                self.get_obstacle_point(self.db, self.status, map_ratio=self.map_ratio)
            walk_v = self.op_v_list[6] + [scene.rotation.Yaw, 180, 0]
        if op_type in [13, 14, 15]:  # 空调相关任务的移动目标
            if self.show_ui:
                self.get_obstacle_point(self.db, self.status, map_ratio=self.map_ratio)
            walk_v = [240, -140.0] + [0, 180, 0]
        if op_type == 16:  # 抓握物体，移动到物体周围的可达区域
            scene = self.status
            obj_info = scene.objects[obj_id]
            obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
            walk_v = [obj_x + 50, obj_y] + [180, 180, 0]
            if obj_info.name == 'Plate':
                walk_v = [obj_x + 51, obj_y] + [180, 180, 0]
            if 820 <= obj_y <= 1200 and 240 <= obj_x <= 500:  # 物品位于斜的抹布桌上 ([240,500],[820,1200])
                walk_v = [obj_x + 40, obj_y - 35, 130, 180, 0]
        if op_type == 17:  # 放置物体，移动到物体周围的可达区域
            walk_v = release_pos[:-1] + [180, 180, 0]
            if release_pos == [340.0, 900.0, 99.0]:
                walk_v[2] = 130
        # 移动到目标位置
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
        scene = self.stub.Do(action)
        print("After Walk Position:", [scene.location.X, scene.location.Y, scene.rotation.Yaw])

    # 相应的行动，由主办方封装
    def control_robot_action(self, type=0, action=0, message="你好"):
        scene = self.stub.ControlRobot(
            GrabSim_pb2.ControlInfo(
                scene=self.sceneID, type=type, action=action, content=message
            )
        )
        if str(scene.info).find("Action Success") > -1:
            print(scene.info)
            return True
        else:
            print(scene.info)
            return False

    # 调整空调开关、温度
    def adjust_kongtiao(self, op_type):
        # 低头
        value = [0] * 21
        for i in range(21):
            value[i] = self.status.joints[i].angle
        value[5] = 30
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.RotateJoints, values=value)
        scene = self.stub.Do(action)
        time.sleep(1.0)

        if self.show_ui:
            self.get_obstacle_point(self.db, self.status, map_ratio=self.map_ratio,update_info_count=1)


        obj_loc = self.obj_loc[:]
        obj_loc[2] -= 5
        if op_type == 13: obj_loc[1] -= 2
        if op_type == 14: obj_loc[1] -= 0
        if op_type == 15: obj_loc[1] += 2
        self.ik_control_joints(2, obj_loc[0], obj_loc[1], obj_loc[2])
        time.sleep(3.0)
        self.robo_recover()  # 恢复肢体关节
        return True

    def gen_obj(self, h=100):
        # 4;冰红(盒) 5;酸奶  7:保温杯 9;冰红(瓶) 13:代语词典  14:cake 61:甜牛奶
        scene = self.status
        ginger_loc = [scene.location.X, scene.location.Y, scene.location.Z]
        obj_list = [

            GrabSim_pb2.ObjectList.Object(x=190, y=40, z=87, roll=0, pitch=0, yaw=0,
                                          type=38), #矿泉水


            GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 75, z=95, roll=0, pitch=0, yaw=0,
                                          type=48),  # 48是薯片
            # GrabSim_pb2.ObjectList.Object(x=190, y=40, z=87, roll=0, pitch=0, yaw=0,
            #                               type=48), #48是薯片
            GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 65, z=95, roll=0, pitch=0, yaw=0,
                                          type=37), #37是NFC果汁
            GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 55, z=95, roll=0, pitch=0, yaw=0,
                                          type=8), #8是贝尔纳松
            GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 45, z=95, roll=0, pitch=0, yaw=0,
                                          type=6), #6是AD钙奶
            GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 35, z=95, roll=0, pitch=0, yaw=0,
                                          type=9), #9是冰红(瓶)
            GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 25, z=95, roll=0, pitch=0, yaw=0,
                                          type=5),  # 5是酸奶

            # GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 30, z=95, roll=0, pitch=0, yaw=0,
            #                               type=13),
            # GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 40, z=95, roll=0, pitch=0, yaw=0,
            #                               type=48),
            # GrabSim_pb2.ObjectList.Object(x=340, y=960, z=88, roll=0, pitch=0, yaw=90, type=7),
            # GrabSim_pb2.ObjectList.Object(x=340, y=960, z = 88, roll=0, pitch=0, yaw=90, type=9),

            GrabSim_pb2.ObjectList.Object(x=320, y=400, z=95, roll=0, pitch=0, yaw=0,
                                          type=20),

            # 斜桌三瓶冰红茶
            GrabSim_pb2.ObjectList.Object(x=340, y=965, z=88, roll=0, pitch=0, yaw=90, type=4),
            GrabSim_pb2.ObjectList.Object(x=320, y=940, z=88, roll=0, pitch=0, yaw=90, type=4),
            GrabSim_pb2.ObjectList.Object(x=300, y=930, z=88, roll=0, pitch=0, yaw=90, type=4),
            # GrabSim_pb2.ObjectList.Object(x=300, y=930, z=88, roll=0, pitch=0, yaw=90, type=38), #矿泉水

            GrabSim_pb2.ObjectList.Object(x=370, y=1000, z=88, roll=0, pitch=0, yaw=90, type=1), #香蕉
            GrabSim_pb2.ObjectList.Object(x=380, y=1000, z=88, roll=0, pitch=0, yaw=90, type=65),  # 番茄
            GrabSim_pb2.ObjectList.Object(x=380, y=1020, z=88, roll=0, pitch=0, yaw=90, type=42),  # 山竹
            GrabSim_pb2.ObjectList.Object(x=360, y=1020, z=88, roll=0, pitch=0, yaw=90, type=27),  # 橙子

            # BrightTable2
            # GrabSim_pb2.ObjectList.Object(x=-30, y=1000, z=35, roll=0, pitch=0, yaw=90, type=64), #西瓜
            GrabSim_pb2.ObjectList.Object(x=-15, y=1050, z=40, roll=0, pitch=0, yaw=90, type=17), #a午餐盒

            # 保温杯
            GrabSim_pb2.ObjectList.Object(x=-102, y=10, z=90, roll=0, pitch=0, yaw=90, type=7),
            # GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 70, z=95, roll=0, pitch=0, yaw=0,
            #                               type=9),

            # Table3上由两套军旗，一个模仿
            GrabSim_pb2.ObjectList.Object(x=-115, y=200, z=85, roll=0, pitch=0, yaw=90, type=26), # Chess
            GrabSim_pb2.ObjectList.Object(x=-130, y=225, z=85, roll=0, pitch=0, yaw=90, type=55), # 玩具狗
            GrabSim_pb2.ObjectList.Object(x=-110, y=225, z=85, roll=0, pitch=0, yaw=90, type=56), #玩具熊
            GrabSim_pb2.ObjectList.Object(x=-115, y=250, z=85, roll=0, pitch=0, yaw=90, type=26),  # Chess
            GrabSim_pb2.ObjectList.Object(x=-115, y=280, z=85, roll=0, pitch=0, yaw=90, type=35),  # 魔方

            # 靠窗边的桌子上
            GrabSim_pb2.ObjectList.Object(x=-400, y=520, z=70, roll=0, pitch=0, yaw=0, type=63),  # 小说
            GrabSim_pb2.ObjectList.Object(x=-410, y=550, z=70, roll=0, pitch=0, yaw=0, type=59),  # 围巾
            GrabSim_pb2.ObjectList.Object(x=-395, y=570, z=70, roll=0, pitch=0, yaw=0, type=18), # 手镯


        ]
        scene = self.stub.AddObjects(GrabSim_pb2.ObjectList(objects=obj_list, scene=self.sceneID))
        time.sleep(1.0)

    # 实现抓握操作
    def grasp_obj(self, obj_id, hand_id=1):
        print('------------------adjust_joints----------------------')
        scene = self.status

        # 低头
        value = [0] * 21
        for i in range(21):
            value[i] = self.status.joints[i].angle
        value[5] = 30
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.RotateJoints, values=value)
        scene = self.stub.Do(action)
        time.sleep(1.0)

        if self.show_ui:
            self.get_obstacle_point(self.db, self.status, map_ratio=self.map_ratio)

        obj_info = scene.objects[obj_id]
        obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
        if 820 <= obj_y <= 1200 and 240 <= obj_x <= 500: # 物品位于斜的抹布桌上 ([240,500],[820,1200])
            obj_x += 3
            obj_y += 2.5
        if obj_info.name == "CoffeeCup":
            # obj_x += 2.5
            # obj_y -= 0.7  # 1.7
            # obj_z -= 6
            # values= [0, 0, 0, 0, 0, 15, -6, -6, -6, -6]  # 后5位右手 [-6,45]
            # stub.Do(GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Finger, values=values))
            pass
        if obj_info.name == "Glass":
            pass
        # Finger
        self.ik_control_joints(2, obj_x - 9, obj_y, obj_z)  # -10, 0, 0
        time.sleep(3.0)
        # Grasp Obj
        print('------------------grasp_obj----------------------')
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Grasp,
                                    values=[hand_id, obj_id])
        scene = self.stub.Do(action)
        time.sleep(3.0)
        return True

    # robot的肢体恢复原位
    def robo_recover(self):
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.RotateJoints,  # 恢复原位
                                    values=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        scene = self.stub.Do(action)

    # 恢复手指关节
    def standard_finger(self):
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.stub.Do(GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Finger, values=values))
        time.sleep(1.0)

    # 弯腰以及手掌与放置面平齐
    def robo_stoop_parallel(self):
        # 0-3是躯干，4-6是脖子和头，7-13是左胳膊，14-20是右胳膊
        scene = self.status
        angle = [scene.joints[i].angle for i in range(21)]
        angle[0] = 15  # 15
        angle[19] = -15
        angle[20] = -30
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.RotateJoints,  # 弯腰
                                    values=angle)
        scene = self.stub.Do(action)
        time.sleep(1.0)

    # 实现放置操作
    def release_obj(self, release_pos):
        print("------------------adjust_joints----------------------")
        # 低头
        value = [0] * 21
        for i in range(21):
            value[i] = self.status.joints[i].angle
        value[5] = 30
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.RotateJoints, values=value)
        scene = self.stub.Do(action)
        time.sleep(1.0)

        if self.show_ui:
            self.get_obstacle_point(self.db, self.status, map_ratio=self.map_ratio)

        if release_pos == [340.0, 900.0, 99.0]:
            self.ik_control_joints(2, release_pos[0] - 40, release_pos[1] + 35, release_pos[2])
            time.sleep(2.0)
        else:
            self.ik_control_joints(2, release_pos[0] - 80, release_pos[1], release_pos[2])
            time.sleep(2.0)
            self.robo_stoop_parallel()
        print("------------------release_obj----------------------")
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Release, values=[1])
        scene = self.stub.Do(action)
        time.sleep(2.0)
        self.robo_recover()  # 恢复肢体关节
        self.standard_finger()  # 恢复手指关节
        return True

    # 执行过程: Robot输出"开始(任务名)" -> 按步骤数执行任务 -> Robot输出成功或失败的对话
    def op_task_execute(self, op_type, obj_id=0, release_pos=[247.0, 520.0, 100.0]):
        #id = 196  # Glass = 188+x, Plate = 150+x
        self.control_robot_action(0, 1, "开始" + self.op_dialog[op_type])  # 输出正在执行的任务
        if op_type < 8:
            if self.show_ui:
                self.get_obstacle_point(self.db, self.status, map_ratio=self.map_ratio)
            result = self.control_robot_action(op_type, 1)
        if 8 <= op_type <= 12:
            if self.show_ui:
                self.get_obstacle_point(self.db, self.status, map_ratio=self.map_ratio)
            result = self.control_robot_action(self.op_typeToAct[op_type][0], self.op_typeToAct[op_type][1])
        if op_type in [13, 14, 15]:  # 调整空调:13代表按开关,14升温,15降温
            result = self.adjust_kongtiao(op_type)
        if op_type == 16:  # 抓握物体, 需要传入物品id
            result = self.grasp_obj(obj_id)
        if op_type == 17:  # 放置物体, 放置物品, 需要传入放置地点
            result = self.release_obj(release_pos)
        self.control_robot_action(0, 2)
        if result:
            if self.op_act_num[op_type] > 0:
                for i in range(2, 2 + self.op_act_num[op_type]):
                    self.control_robot_action(op_type, i)
                    self.control_robot_action(0, 2)
            # self.control_robot_action(0, 1, "成功"+self.op_dialog[op_type])
        # else:
        #     self.control_robot_action(0, 1, self.op_dialog[op_type]+"失败")

    def find_obj(self, name):
        for id, item in enumerate(self.status.objects):
            if item.name == name:
                print("name:", name, "id:", id, "X:", item.location.X, "Y:", item.location.Y, "Z:", item.location.Z, )

    def test_move(self):
        v_list = [[0, 880], [250, 1200], [-55, 750], [70, -200]]
        scene = self.status
        for walk_v in v_list:
            walk_v = walk_v + [scene.rotation.Yaw - 90, 600, 100]
            print("walk_v", walk_v)
            action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
            scene = self.stub.Do(action)
            print(scene.info)

    def navigation_move(self, plt, cur_objs, cur_obstacle_world_points, v_list, map_ratio, db, scene_id=0, map_id=11):
        print('------------------navigation_move----------------------')
        scene = self.stub.Observe(GrabSim_pb2.SceneID(value=scene_id))
        walk_value = [scene.location.X, scene.location.Y]
        print("position:", walk_value)

        if not cur_objs:
            walk_v = [scene.location.X, scene.location.Y + 1]
            yaw = Navigator.get_yaw(walk_value, walk_v)
            yaw =  math.degrees(yaw)
            walk_v = walk_value + [yaw, 250, 10]
            print("walk_v", walk_v)
            action = GrabSim_pb2.Action(scene=scene_id, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
            scene = self.stub.Do(action)
            # cur_objs, objs_name_set = camera.get_semantic_map(GrabSim_pb2.CameraName.Head_Segment, cur_objs,
            #                                                   objs_name_set)

            # cur_obstacle_world_points, cur_objs_id = camera.get_obstacle_point(plt, db, scene,
            #                                                                    cur_obstacle_world_points, map_ratio)
            cur_obstacle_world_points, cur_objs_id = camera.get_obstacle_point(self, db, scene,
                                                                               cur_obstacle_world_points, map_ratio)
            # cur_obstacle_world_points, cur_objs_id = self.get_obstacle_point(db, scene, map_ratio)
            # # self.get_obstacle_point(db, scene, cur_obstacle_world_points, map_ratio)


            # if scene.info == "Unreachable":
            print(scene.info)

        # if map_id == 11:  # coffee
        #     v_list = [[0, 880], [250, 1200], [-55, 750], [70, -200]]
        # else:
        #     v_list = [[0.0, 0.0]]

        else:
            for walk_v in v_list:
                yaw = Navigator.get_yaw(walk_value, walk_v)
                yaw =  math.degrees(yaw)
                walk_v = walk_v + [yaw, 250, 10]
                print("walk_v", walk_v)
                action = GrabSim_pb2.Action(scene=scene_id, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
                scene = self.stub.Do(action)

                # cur_objs, objs_name_set = camera.get_semantic_map(GrabSim_pb2.CameraName.Head_Segment, cur_objs,
                #                                                   objs_name_set)

                cur_obstacle_world_points, cur_objs_id = camera.get_obstacle_point(self, db, scene,
                                                                                   cur_obstacle_world_points, map_ratio)

                # if scene.info == "Unreachable":
                print(scene.info)
        return cur_obstacle_world_points, cur_objs_id

    def isOutMap(self, pos, min_x=-200, max_x=600, min_y=-250, max_y=1300):
        if pos[0] <= min_x or pos[0] >= max_x or pos[1] <= min_y or pos[1] >= max_y:
            return True
        return False

    def real2map(self, x, y):
        '''
            实际坐标->地图坐标 (向下取整)
        '''
        # x = round((x - self.min_x) / self.scale_ratio)
        # y = round((y - self.min_y) / self.scale_ratio)
        x = math.floor((x + 200))
        y = math.floor((y + 250))
        return x, y

    def explore(self, map, explore_range):
        scene = self.stub.Observe(GrabSim_pb2.SceneID(value=0))
        cur_pos = [int(scene.location.X), int(scene.location.Y)]
        for i in range(cur_pos[0] - explore_range, cur_pos[0] + explore_range + 1):
            for j in range(cur_pos[1] - explore_range, cur_pos[1] + explore_range + 1):
                if self.isOutMap((i, j)):
                    continue
                x, y = self.real2map(i, j)
                if map[x, y] == 0:
                    self.visited.add((i, j))
                    self.auto_map[x][y] = 0
        for i in range(cur_pos[0] - explore_range, cur_pos[0] + explore_range + 1):
            for j in range(cur_pos[1] - explore_range, cur_pos[1] + explore_range + 1):
                if self.isOutMap((i, j)):
                    continue
                x, y = self.real2map(i, j)
                if map[x, y] == 0:
                    if self.isNewFrontier((i, j), map):
                        self.all_frontier_list.add((i, j))
        if len(self.all_frontier_list) == 0:
            free_list = list(self.visited)
            free_array = np.array(free_list)
            print(f"主动探索完成！保存了二维地图与环境中重点物品语义信息！")

            # # 画地图: X行Y列，第一行在下面
            # plt.clf()
            # plt.imshow(self.auto_map, cmap='binary', alpha=0.5, origin='lower',
            #            extent=(-250, 1300,
            #                    -200, 600))
            # plt.show()
            # print("已绘制完成地图！！！")

            return None
        # # 画地图: X行Y列，第一行在下面
        # plt.imshow(self.auto_map, cmap='binary', alpha=0.5, origin='lower',
        #            extent=(-250, 1300,
        #                    -200, 600))
        # plt.show()
        # print("已绘制部分地图！")
        return self.getNearestFrontier(cur_pos, self.all_frontier_list)

    def isNewFrontier(self, pos, map):
        around_nodes = [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]

        for node in around_nodes:
            x, y = self.real2map(node[0], node[1])
            if not self.isOutMap((node[0], node[1])) and node not in self.visited and map[x, y] == 0:
                return True
        if (pos[0], pos[1]) in self.all_frontier_list:
            self.all_frontier_list.remove((pos[0], pos[1]))
        return False

    def getDistance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def getNearestFrontier(self, cur_pos, frontiers):
        dis_min = sys.maxsize
        frontier_best = None
        for frontier in frontiers:
            dis = self.getDistance(frontier, cur_pos)
            if dis <= dis_min:
                dis_min = dis
                frontier_best = frontier
        return frontier_best

    def cal_distance_to_robot(self, objx, objy, objz):
        scene = self.status
        ginger_x, ginger_y, ginger_z = [int(scene.location.X), int(scene.location.Y), 100]
        return math.sqrt((ginger_x - objx) ** 2 + (ginger_y - objy) ** 2 + (ginger_z - objz) ** 2)

    # 根据map文件判断是否可达
    def reachable(self, pos):
        x, y = self.real2map(pos[0], pos[1])
        if self.map_file[x, y] == 0:
            return True
        else:
            return False


    def transform_co(self,img_data, pixel_x_, pixel_y_, depth_, id=0, label=0):
        im = img_data.images[0]

        # 相机外参矩阵
        out_matrix = np.array(im.parameters.matrix).reshape((4, 4))

        d = np.frombuffer(im.data, dtype=im.dtype).reshape((im.height, im.width, im.channels))
        depth = depth_

        # 将像素坐标转换为归一化设备坐标
        normalized_x = (pixel_x_ - im.parameters.cx) / im.parameters.fx
        normalized_y = (pixel_y_ - im.parameters.cy) / im.parameters.fy

        # 将归一化设备坐标和深度值转换为相机坐标
        camera_x = normalized_x * depth
        camera_y = normalized_y * depth
        camera_z = depth

        # 构建相机坐标向量
        camera_coordinates = np.array([camera_x, camera_y, camera_z, 1])
        # print("物体相对相机坐标的齐次坐标: ", camera_coordinates)

        # 将相机坐标转换为机器人底盘坐标
        robot_coordinates = np.dot(out_matrix, camera_coordinates)[:3]
        # print("物体的相对底盘坐标为:", robot_coordinates)

        # 将物体相对机器人底盘坐标转为齐次坐标
        robot_homogeneous_coordinates = np.array([robot_coordinates[0], -robot_coordinates[1], robot_coordinates[2], 1])
        # print("物体的相对底盘的齐次坐标为:", robot_homogeneous_coordinates)

        # 机器人坐标
        X = self.status.location.X
        Y = self.status.location.Y
        Z = 0.0

        # 机器人旋转信息
        Roll = 0.0
        Pitch = 0.0
        Yaw = self.status.rotation.Yaw

        # 构建平移矩阵
        T = np.array([[1, 0, 0, X],
                      [0, 1, 0, Y],
                      [0, 0, 1, Z],
                      [0, 0, 0, 1]])

        # 构建旋转矩阵
        Rx = np.array([[1, 0, 0, 0],
                       [0, np.cos(Roll), -np.sin(Roll), 0],
                       [0, np.sin(Roll), np.cos(Roll), 0],
                       [0, 0, 0, 1]])

        Ry = np.array([[np.cos(Pitch), 0, np.sin(Pitch), 0],
                       [0, 1, 0, 0],
                       [-np.sin(Pitch), 0, np.cos(Pitch), 0],
                       [0, 0, 0, 1]])

        Rz = np.array([[np.cos(np.radians(Yaw)), -np.sin(np.radians(Yaw)), 0, 0],
                       [np.sin(np.radians(Yaw)), np.cos(np.radians(Yaw)), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

        R = np.dot(Rz, np.dot(Ry, Rx))

        # 构建机器人的变换矩阵
        T_robot = np.dot(T, R)
        # print(T_robot)

        # 将物体的坐标从机器人底盘坐标系转换到世界坐标系
        world_coordinates = np.dot(T_robot, robot_homogeneous_coordinates)[:3]

        # if world_coordinates[0] < 200 and world_coordinates[1] <= 1050:
        #     world_coordinates[0] += 400
        #     world_coordinates[1] += 400
        # elif world_coordinates[0] >= 200 and world_coordinates[1] <= 1050:
        #     world_coordinates[0] -= 550
        #     world_coordinates[1] += 400
        # elif world_coordinates[0] >= 200 and world_coordinates[1] > 1050:
        #     world_coordinates[0] -= 550
        #     world_coordinates[1] -= 1450
        # elif world_coordinates[0] < 200 and world_coordinates[1] > 1050:
        #     world_coordinates[0] += 400
        #     world_coordinates[1] -= 1450
        # print("物体的世界坐标：", world_coordinates)

        # 世界偏移后的坐标
        world_offest_coordinates = [world_coordinates[0] + 700, world_coordinates[1] + 1400, world_coordinates[2]]
        # print("物体世界偏移的坐标: ", world_offest_coordinates)
        return world_coordinates

    def ui_func(self,args):
        plt.show()

    def draw_current_bt(self):
        pass

    def get_obstacle_point(self, db, scene, map_ratio, update_info_count=0):

        # if abs(self.last_take_pic_tim - self.time)<

        # db = DBSCAN(eps=4, min_samples=2)
        cur_obstacle_pixel_points = []
        cur_obstacle_world_points = []
        obj_detect_count = 0
        walker_detect_count = 0
        object_pixels = {}

        not_key_objs_id = {255, 254, 253, 107, 81}


        img_data_segment,img_data_depth,img_data_color = self.get_cameras()
        if len(img_data_segment.images) <1:
            return
        im_segment = img_data_segment.images[0]
        im_depth = img_data_depth.images[0]
        im_color = img_data_color.images[0]

        d_segment = np.frombuffer(im_segment.data, dtype=im_segment.dtype).reshape(
            (im_segment.height, im_segment.width, im_segment.channels))
        d_depth = np.frombuffer(im_depth.data, dtype=im_depth.dtype).reshape(
            (im_depth.height, im_depth.width, im_depth.channels))
        d_color = np.frombuffer(im_color.data, dtype=im_color.dtype).reshape(
            (im_color.height, im_color.width, im_color.channels))


        items = img_data_segment.info.split(";")
        objs_id = {}
        for item in items:
            key, value = item.split(":")
            objs_id[int(key)] = value
        objs_id[251] = "walker"
        # plt.imshow(d_depth, cmap="gray" if "depth" in im_depth.name.lower() else None)
        # plt.show()
        img_segment = d_segment


        d_depth = np.transpose(d_depth, (1, 0, 2))
        d_segment = np.transpose(d_segment, (1, 0, 2))

        for i in range(0, d_segment.shape[0], map_ratio):
            for j in range(0, d_segment.shape[1], map_ratio):
                if d_depth[i][j][0] == 600:
                    continue

                # if d_segment[i][j] == 96:
                #     print(f"apple的像素坐标：({i},{j})")
                #     print(f"apple的深度：{d_depth[i][j][0]}")
                #     print(f"apple的世界坐标: {transform_co(img_data_depth, i, j, d_depth[i][j][0], scene)}")
                # if d_segment[i][j] == 113:
                #     print(f"kettle的像素坐标：({i},{j})")
                #     print(f"kettle的深度：{d_depth[i][j][0]}")
                #     print(f"kettle的世界坐标: {transform_co(img_data_depth, i, j, d_depth[i][j][0], scene)}")
                if d_segment[i][j][0] in [251]:
                    cur_obstacle_pixel_points.append([i, j])
                if d_segment[i][j][0] not in not_key_objs_id:
                    # 首先检查键是否存在
                    if d_segment[i][j][0] in object_pixels:
                        # 如果键存在，那么添加元组(i, j)到对应的值中
                        object_pixels[d_segment[i][j][0]].append([i, j])
                    else:
                        # 如果键不存在，那么创建一个新的键值对，其中键是d_segment[i][j][0]，值是一个包含元组(i, j)的列表
                        object_pixels[d_segment[i][j][0]] = [[i, j]]

        for i in range(0, d_segment.shape[0], map_ratio):
            for j in range(0, d_segment.shape[1], map_ratio):
                if d_depth[i][j][0] == 600:
                    continue

                # if d_segment[i][j] == 96:
                #     print(f"apple的像素坐标：({i},{j})")
                #     print(f"apple的深度：{d_depth[i][j][0]}")
                #     print(f"apple的世界坐标: {transform_co(img_data_depth, i, j, d_depth[i][j][0], scene)}")
                # if d_segment[i][j] == 113:
                #     print(f"kettle的像素坐标：({i},{j})")
                #     print(f"kettle的深度：{d_depth[i][j][0]}")
                #     print(f"kettle的世界坐标: {transform_co(img_data_depth, i, j, d_depth[i][j][0], scene)}")
                # if d_segment[i][j][0] in [251]:
                #     cur_obstacle_pixel_points.append([i, j])
                if d_segment[i][j][0] not in not_key_objs_id:
                    # 首先检查键是否存在
                    if d_segment[i][j][0] in object_pixels:
                        # 如果键存在，那么添加元组(i, j)到对应的值中
                        object_pixels[d_segment[i][j][0]].append([i, j])
                    else:
                        # 如果键不存在，那么创建一个新的键值对，其中键是d_segment[i][j][0]，值是一个包含元组(i, j)的列表
                        object_pixels[d_segment[i][j][0]] = [[i, j]]


        # print(cur_obstacle_pixel_points)
        # for pixel in cur_obstacle_pixel_points:
        #     world_point = self.transform_co(img_data_depth, pixel[0], pixel[1], d_depth[pixel[0]][pixel[1]][0], scene)
        #     cur_obstacle_world_points.append([world_point[0], world_point[1]])
        # print(f"{pixel}：{[world_point[0], world_point[1]]}")
        img_obj = d_color

        # self.ui_func(("draw_img","img_label_obj",d_color))

        # 画分隔图
        # plt.subplot(2, 2, 1)
        plt.figure()
        plt.imshow(img_segment, cmap="gray" if "depth" in im_segment.name.lower() else None)
        plt.axis("off")
        # plt.title("相机分割")
        self.send_img("img_label_seg")

        # 画目标检测图
        # plt.subplot(2, 2, 2)
        plt.figure()
        plt.imshow(img_obj, cmap="gray" if "depth" in im_depth.name.lower() else None)
        plt.axis('off')
        # plt.title("目标检测")

        for key, value in object_pixels.items():
            if key == 0:
                continue
            if key not in objs_id.keys():
                continue
            if key in [91, 84, 96, 87, 102, 106, 120, 85, 113, 101, 83, 251]:
                X = np.array(value)
                db.fit(X)
                labels = db.labels_
                # 将数据按照聚类标签分组，并打印每个分组的数据
                for i in range(max(labels) + 1):  # 从0到最大聚类标签的值
                    group_data = X[labels == i]  # 获取当前标签的数据
                    x_max = max(p[0] for p in group_data)
                    y_max = max(p[1] for p in group_data)
                    x_min = min(p[0] for p in group_data)
                    y_min = min(p[1] for p in group_data)
                    if x_max - x_min < 10 or y_max - y_min < 10:
                        continue
                    if key != 251:
                        obj_detect_count += 1
                    else:
                        center_point = [int((x_max - x_min) / 2) + x_min, int((y_max-y_min) / 2) + y_min]
                        world_point = self.transform_co(img_data_depth, center_point[0],center_point[1] , d_depth[center_point[0]][center_point[1]][0], scene)
                        cur_obstacle_world_points.append([world_point[0], world_point[1]])
                        walker_detect_count += 1
                    # 在指定的位置绘制方框
                    # 创建矩形框
                    rect = patches.Rectangle((x_min, y_min), (x_max - x_min), (y_max - y_min), linewidth=1,
                                             edgecolor=self.colors[key % 10],
                                             facecolor='none')
                    plt.text(x_min, y_min, f'{objs_id[key]}',
                             fontdict={'family': 'serif', 'size': 10, 'color': 'green'}, ha='center',
                             va='center')
                    plt.gca().add_patch(rect)
            else:
                if key != 251:
                    obj_detect_count += 1
                else:
                    center_point = [int((x_max - x_min) / 2), int(y_max - y_min) / 2]
                    cur_obstacle_world_points.append(self.transform_co(img_data_depth, center_point[0], center_point[1],
                                                                       d_depth[center_point[0]][center_point[1]][0],
                                                                       scene))
                    walker_detect_count += 1
                x_max = max(p[0] for p in value)
                y_max = max(p[1] for p in value)
                x_min = min(p[0] for p in value)
                y_min = min(p[1] for p in value)
                # 在指定的位置绘制方框
                # 创建矩形框
                rect = patches.Rectangle((x_min, y_min), (x_max - x_min), (y_max - y_min), linewidth=1,
                                         edgecolor=self.colors[key % 10],
                                         facecolor='none')

                plt.text(x_min, y_min, f'{objs_id[key]}',
                         fontdict={'family': 'serif', 'size': 10, 'color': 'green'},
                         ha='center',
                         va='center')
                plt.gca().add_patch(rect)

        self.send_img("img_label_obj")


        new_map = self.updateMap(cur_obstacle_world_points)
        self.draw_map(plt,new_map)

        plt.axis("off")
        self.send_img("img_label_map")



        # plt.subplot(2, 7, 14)
        # plt.text(0, 0.9, f'检测行人数量：{walker_detect_count}', fontsize=10)
        # plt.text(0, 0.7, f'检测物体数量：{obj_detect_count}', fontsize=10)
        # plt.text(0, 0.5, f'新增语义信息：{walker_detect_count}', fontsize=10)
        # plt.text(0, 0.3, f'更新语义信息：{update_info_count}', fontsize=10)
        # plt.text(0, 0.1, f'已存语义信息：{self.infoCount}', fontsize=10)


        # draw figures

        # output_path = os.path.join(self.output_path,"vision.png")




        # # 转换为numpy数组
        # image_np = np.asarray(image_pil)
        # self.ui_func(("draw_from_file","img_label_canvas",output_path))
        # plt.close()
        # plt.show()
        # return cur_obstacle_world_points

    def send_img(self,name):
        # 将图像保存到内存
        buffer = io.BytesIO()
        plt.savefig(buffer, bbox_inches='tight', pad_inches=0,format='png')
        image_data = buffer.getvalue()

        # 关闭当前图像
        plt.close()

        if not self.img_cache[name] == image_data:
            self.img_cache[name] = image_data
            self.ui_func(("draw_img",name,image_data))





    def updateMap(self, points):
        # map = copy.deepcopy(self.map_map)
        map = copy.deepcopy(self.map_map_real)
        for point in points:
            if point[0] < -350 or point[0] > 600 or point[1] < -400 or point[1] > 1450:
                continue
            map[math.floor((point[0] + 350) / self.map_ratio), math.floor((point[1] + 400) / self.map_ratio)] = 1
        for obs in points:
            obs = self.navigator.planner.real2map(obs)
            (x, y) = obs
            occupy_radius = self.navigator.planner.dyna_obs_radius  # 避免robot被dyna_obs的占用区域包裹住
            # 圆形区域
            occupy_pos = [(i, j) for i in range(x - occupy_radius, x + occupy_radius + 1)
                          for j in range(y - occupy_radius, y + occupy_radius + 1)
                          if euclidean_distance((i, j), obs) < occupy_radius]

            for pos in occupy_pos:
                map[pos] = 1
        return map

    def draw_map(self,plt, map):
        # plt.subplot(2, 1, 2)  # 这里的2,1表示总共2行，1列，2表示这个位置是第2个子图
        plt.imshow(map, cmap='binary', alpha=0.5, origin='lower',
                   extent=(-400 / self.map_ratio, 1450 / self.map_ratio,
                           -350 / self.map_ratio, 600 / self.map_ratio))
        # plt.title('可达性地图')

    def get_id_object_world(self, id, scene):
        pixels = []
        world_points = []

        img_data_segment,img_data_depth,_ = self.get_cameras()
        # img_data_segment = get_camera([GrabSim_pb2.CameraName.Head_Segment])
        im_segment = img_data_segment.images[0]

        # img_data_depth = get_camera([GrabSim_pb2.CameraName.Head_Depth])
        im_depth = img_data_depth.images[0]

        d_segment = np.frombuffer(im_segment.data, dtype=im_segment.dtype).reshape(
            (im_segment.height, im_segment.width, im_segment.channels))
        d_depth = np.frombuffer(im_depth.data, dtype=im_depth.dtype).reshape(
            (im_depth.height, im_depth.width, im_depth.channels))

        d_segment = np.transpose(d_segment, (1, 0, 2))
        d_depth = np.transpose(d_depth, (1, 0, 2))

        for i in range(0, d_segment.shape[0], 5):
            for j in range(0, d_segment.shape[1], 5):
                if d_segment[i][j][0] == id:
                    pixels.append([i, j])
        for pixel in pixels:
            world_points.append(self.transform_co(img_data_depth, pixel[0], pixel[1], d_depth[pixel[0]][pixel[1]][0]))
        return world_points

    def get_cameras(self):
        # if self.time - self.last_camera_time > self.camera_interval:
        self.img_data_segment = self.get_camera([GrabSim_pb2.CameraName.Head_Segment])
        time.sleep(0.2)
        self.img_data_depth = self.get_camera([GrabSim_pb2.CameraName.Head_Depth])
        time.sleep(0.2)
        self.img_data_color = self.get_camera([GrabSim_pb2.CameraName.Head_Color])
        # self.last_camera_time = self.time

        return self.img_data_segment,self.img_data_depth,self.img_data_color