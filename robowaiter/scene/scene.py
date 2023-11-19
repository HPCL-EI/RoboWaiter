import pickle
import sys
import time
import grpc
import numpy as np
import matplotlib.pyplot as plt
from robowaiter.proto import camera
from robowaiter.proto import semantic_map
from robowaiter.algos.navigator.navigate import Navigator
import math
from robowaiter.proto import GrabSim_pb2
from robowaiter.proto import GrabSim_pb2_grpc
import copy
import os
from robowaiter.utils import get_root_path
root_path = get_root_path()

channel = grpc.insecure_channel(
    "localhost:30001",
    options=[
        ("grpc.max_send_message_length", 1024 * 1024 * 1024),
        ("grpc.max_receive_message_length", 1024 * 1024 * 1024),
    ],
)
stub = GrabSim_pb2_grpc.GrabSimStub(channel)

animation_step = [4, 5, 7, 3, 3]
loc_offset = [-700, -1400]


def init_world(scene_num=1, mapID=11):
    stub.SetWorld(GrabSim_pb2.BatchMap(count=scene_num, mapID=mapID))
    time.sleep(3)  # wait for the map to load


def show_image(camera_data):
    print('------------------show_image----------------------')
    #获取第0张照片
    im = camera_data.images[0]
    #使用numpy(np) 数值类型矩阵的frombuffer，将im.data以流的形式（向量的形式）读入，在变型reshape成三位矩阵的形式(长度，宽度，深度)即三阶张量
    d = np.frombuffer(im.data, dtype=im.dtype).reshape((im.height, im.width, im.channels))
    #matplotlib中的plt方法 对矩阵d 进行图形绘制，如果 深度相机拍摄的带深度的图片（图片名字中有depth信息），则转换成黑白图即灰度图
    plt.imshow(d, cmap="gray" if "depth" in im.name.lower() else None)
    #图像展示在屏幕上
    plt.show()

    return d


class Scene:
    robot = None
    event_list = []
    new_event_list = []
    signal_event_list = []
    # show_bubble = True
    event_signal = "None"

    default_state = {
        "map": {
            "2d": None,
            "obj_pos": {}
        },
        "chat_list": [],  # 未处理的顾客的对话, (顾客的位置,顾客对话的内容)
        "sub_goal_list": [],  # 子目标列表
        "status": None,  # 仿真器中的观测信息，见下方详细解释
        "condition_set": {'At(Robot,Bar)', 'Is(AC,Off)',
         'Holding(Nothing)','Exist(Yogurt)','Exist(BottledDrink)','On(Yogurt,Bar)','On(BottledDrink,Bar)',
         #'Exist(Softdrink)', 'On(Softdrink,Table1)',
        'Exist(VacuumCup)', 'On(VacuumCup,Table2)',
         'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
         'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'},
        "obj_mem":{},
        "customer_mem":{},
        "served_mem":{},
        "greeted_customers":set(),
        "attention":{},
        "serve_state":{},
        "chat_history":{}
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

    def __init__(self,robot=None, sceneID=0):
        self.sceneID = sceneID
        self.use_offset = False
        self.start_time = time.time()
        self.time = 0
        self.sub_task_seq = None

        self.show_bubble = True

        # init robot
        if robot:
            robot.set_scene(self)
            robot.load_BT()
        self.robot = robot

        self.robot_changed = False

        # 1-7 正常执行, 8-10 控灯操作移动到6, 11-12窗帘操作不需要移动,
        self.op_dialog = ["","制作咖啡","倒水","夹点心","拖地","擦桌子","开筒灯","搬椅子",    # 1-7
                          "关筒灯","开大厅灯","关大厅灯","关闭窗帘","打开窗帘",              # 8-12
                          "调整空调开关","调高空调温度","调低空调温度",                      # 13-15
                          "抓握物体","放置物体"]                                         # 16-17
        # 动画控制的执行步骤数
        self.op_act_num = [0,3,4,6,3,2,0,1,
                           0,0,0,0,0,
                           0,0,0,
                           0,0]
        # 动画控制的执行区域坐标
        self.op_v_list = [[0.0,0.0],[250.0, 310.0],[-70.0, 480.0],[250.0, 630.0],[-70.0, 740.0],[260.0, 1120.0],[300.0, -220.0],
                          [0.0, -70.0]]
        self.op_typeToAct = {8:[6,2],9:[6,3],10:[6,4],11:[8,1],12:[8,2]}   # 任务类型到行动的映射
        self.obj_loc = [300.5, -140.0,114]   # 空调面板位置

        # AEM
        self.visited = set()
        self.all_frontier_list = set()
        self.semantic_map = semantic_map
        self.auto_map = np.ones((800, 1550))
        self.filename = os.path.join(root_path, 'robowaiter/proto/map_1.pkl')
        with open(self.filename, 'rb') as file:
            self.map_file = pickle.load(file)


    def reset(self):
        # 基类reset，默认执行仿真器初始化操作
        self.reset_sim()

        # reset state
        self.state = copy.deepcopy(self.default_state)



        print("场景初始化完成")
        self._reset()

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

        self.deal_event()
        self.deal_new_event()
        self.deal_signal_event()
        self._step()
        self.robot_changed = self.robot.step()

    def deal_new_event(self):
        if len(self.new_event_list)>0:
            next_event = self.new_event_list[0]
            t,func,args = next_event
            if self.time >= t:
                print(f'event: {t}, {func.__name__}')
                self.new_event_list.pop(0)
                func(*args)

    def deal_signal_event(self):
        if len(self.signal_event_list)>0:
            next_event = self.signal_event_list[0]
            t, func,args = next_event
            if t < 0: #一直等待机器人行动，直到机器人无行动
                if self.robot_changed:
                    return
            if t > 0:
                time.sleep(t)

            print(f'event: {t}, {func.__name__}')
            self.signal_event_list.pop(0)
            func(*args)

    def deal_event(self):
        if len(self.event_list)>0:
            next_event = self.event_list[0]
            t,func = next_event
            if self.time >= t:
                print(f'event: {t}, {func.__name__}')
                self.event_list.pop(0)
                func()

    def create_chat_event(self,sentence):
        def customer_say():
            print(f'{sentence}')
            if self.show_bubble:
                self.chat_bubble(f'{sentence}')
            self.state['chat_list'].append(f'{sentence}')

        return customer_say



    def set_goal(self,goal):
        g = eval("{'" + goal + "'}")
        def set_sub_task():
            self.state['chat_list'].append(("Goal",g))

        return set_sub_task

    def new_set_goal(self,goal):
        g = eval("{'" + goal + "'}")
        self.state['chat_list'].append(("Goal",g))


    @property
    def status(self):
        return stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))

    def reset_sim(self):
        # reset world
        stub.CleanWalkers(GrabSim_pb2.SceneID(value=self.sceneID))
        init_world()
        stub.Reset(GrabSim_pb2.ResetParams(scene=self.sceneID))


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
        walk_v = [X,Y,Yaw,velocity,dis_limit]
        action = GrabSim_pb2.Action(
            scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v
        )
        scene = stub.Do(action)

        return scene

    def walker_walk_to(self,walkerID,X,Y,speed=50,Yaw=0):
        self.control_walker(
            [self.walker_control_generator(walkerID=walkerID, autowalk=False, speed=speed, X=X, Y=Y, Yaw=Yaw)])


    def reachable_check(self, X, Y, Yaw):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        navigation_info = stub.Do(
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


    def add_walker(self,id,x,y,yaw=0,v=0,scope=100):
        loc = [x,y,yaw,v,scope]
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=loc)
        scene = stub.Do(action)
        # print(scene.info)
        walker_list=[]
        if (str(scene.info).find('unreachable') > -1):
            print('当前位置不可达,无法初始化NPC')
        else:
            walker_list.append(
                GrabSim_pb2.WalkerList.Walker(id=id, pose=GrabSim_pb2.Pose(X=loc[0], Y=loc[1], Yaw=loc[2])))
        stub.AddWalker(GrabSim_pb2.WalkerList(walkers=walker_list, scene=self.sceneID))

        w = self.status.walkers
        num_customer = len(w)
        self.state["customer_mem"][w[-1].name] = num_customer-1

    def walker_index2mem(self,index):
        for mem,i in self.state["customer_mem"].items():
            if index == i:
                return mem


    def add_walkers(self,walker_loc=[[0, 880], [250, 1200], [-55, 750], [70, -200]]):
        print('------------------add_walkers----------------------')
        for i,walker in enumerate(walker_loc):
            if len(walker)==2:
                self.add_walker(i,walker[0],walker[1])
            elif len(walker)==3:
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

        index_shift_list = [ 0 for _ in range(len(self.state["customer_mem"])) ]

        stub.RemoveWalkers(GrabSim_pb2.RemoveList(IDs=remove_list, scene=self.sceneID))

        w = self.status.walkers
        for i in range(len(w)):
            self.state["customer_mem"][w[i].name] = i

    def remove_walkers(self,IDs=[0]):
        s = stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))
        scene = stub.RemoveWalkers(GrabSim_pb2.RemoveList(IDs=IDs, scene=self.sceneID))
        time.sleep(2)
        return


    def clean_walker(self):
        stub.CleanWalkers(GrabSim_pb2.SceneID(value=self.sceneID))

    def control_walker(self, walkerID,autowalk,speed,X,Y,Yaw=0):
        pose = GrabSim_pb2.Pose(X=X, Y=Y, Yaw=Yaw)
        scene = stub.ControlWalkers(
            GrabSim_pb2.WalkerControls(controls=[GrabSim_pb2.WalkerControls.WControl(id=walkerID, autowalk=autowalk, speed=speed, pose=pose)], scene=self.sceneID)
        )
        return scene
        # stub.ControlWalkers(
        #     GrabSim_pb2.WalkerControls(controls=control_list, scene=self.sceneID)
        # )

    def control_walkers_and_say(self, control_list_ls):
        """ 同时处理行人的行走和对话
        control_list_ls =[walkerID,autowalk,speed,X,Y,Yaw,cont]
        """
        control_list= []
        for control in control_list_ls:
            if control[-1]!= None:
                walkerID = control[0]
                # cont = self.status.walkers[walkerID].name + ":"+control[-1]
                # self.control_robot_action(control[walkerID], 3, cont)
                self.customer_say(walkerID,control[-1])
            control_list.append(self.walker_control_generator(walkerID=control[0], autowalk=control[1], speed=control[2], X=control[3], Y=control[4], Yaw=control[5]))
        # 收集没有对话的统一控制
        scene = stub.ControlWalkers(
            GrabSim_pb2.WalkerControls(controls=control_list, scene=self.sceneID)
        )
        return scene

    def control_walkers(self,walker_loc=[[-55, 750], [70, -200], [250, 1200], [0, 880]],is_autowalk = True):
        """pose:表示行人的终止位置姿态"""
        scene = self.status
        walker_loc = walker_loc
        controls = []
        for i in range(len(walker_loc)):
            loc = walker_loc[i]
            is_autowalk = is_autowalk
            pose = GrabSim_pb2.Pose(X=loc[0], Y=loc[1], Yaw=180)
            controls.append(GrabSim_pb2.WalkerControls.WControl(id=i, autowalk=is_autowalk, speed=80, pose=pose))
        scene = stub.ControlWalkers(GrabSim_pb2.WalkerControls(controls=controls, scene=self.sceneID))
        return scene

    def control_joints(self, angles):
        stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.RotateJoints,
                values=angles,
            )
        )

    def add_object(self, type, X, Y, Z, Yaw=0):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        stub.AddObjects(
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
        stub.RemoveObjects(GrabSim_pb2.RemoveList(IDs=remove_list, scene=self.sceneID))

    def clean_object(self):
        stub.CleanObjects(GrabSim_pb2.SceneID(value=self.sceneID))

    def grasp(self, handID, objectID):
        stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.Grasp,
                values=[handID, objectID],
            )
        )

    def release(self, handID):
        stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.Release,
                values=[handID],
            )
        )

    def get_camera_color(self, image_only=True):
        camera_data = stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Color], scene=self.sceneID
            )
        )
        if image_only:
            return show_image(camera_data)
        else:
            return camera_data

    def get_camera_depth(self, image_only=True):
        camera_data = stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Depth], scene=self.sceneID
            )
        )
        if image_only:
            return show_image(camera_data)
        else:
            return camera_data

    def get_camera_segment(self, show=True):
        camera_data = stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Segment], scene=self.sceneID
            )
        )
        if show:
            show_image(camera_data)

        return camera_data

    def chat_bubble(self, message):
        stub.ControlRobot(
            GrabSim_pb2.ControlInfo(
                scene=self.sceneID, type=0, action=1, content=message.strip()
            )
        )

    def walker_bubble(self, name, message):
        talk_content = name + ":" + message
        self.control_robot_action(0, 3, talk_content)

    def customer_say(self,name,sentence,show_bubble=True):
        if isinstance(name,int):
            name = self.walker_index2mem(name)

        print(f'{name} say: {sentence}')
        if self.show_bubble and show_bubble:
            self.walker_bubble(name,sentence)
        self.state['chat_list'].append((name,sentence))

    # def control_robot_action(self, scene_id=0, type=0, action=0, message="你好"):
    #     print('------------------control_robot_action----------------------')
    #     scene = stub.ControlRobot(
    #         GrabSim_pb2.ControlInfo(scene=scene_id, type=type, action=action, content=message))
    #     if (str(scene.info).find("Action Success") > -1):
    #         print(scene.info)
    #         return True
    #     else:
    #         print(scene.info)
    #         return False

    def animation_control(self, animation_type):
        # animation_type: 1:make coffee 2: pour water 3: grab food 4: mop floor 5: clean table
        scene = stub.ControlRobot(
            GrabSim_pb2.ControlInfo(scene=self.sceneID, type=animation_type, action=1)
        )
        if scene.info == "action success":
            for i in range(2, animation_step[animation_type - 1] + 1):
                stub.ControlRobot(
                    GrabSim_pb2.ControlInfo(
                        scene=self.sceneID, type=animation_type, action=i
                    )
                )

    def animation_reset(self):
        stub.ControlRobot(GrabSim_pb2.ControlInfo(scene=self.sceneID, type=0, action=0))

    # 手指移动到指定位置
    def ik_control_joints(self, handNum=2, x=30, y=40, z=80):
        # print('------------------ik_control_joints----------------------')
        # IK控制,双手, 1左手, 2右手; 暂时只动右手
        HandPostureObject = [GrabSim_pb2.HandPostureInfos.HandPostureObject(handNum=handNum, x=x, y=y, z=z, roll=0, pitch=0, yaw=0),
                             # GrabSim_pb2.HandPostureInfos.HandPostureObject(handNum=1, x=0, y=0, z=0, roll=0, pitch=0, yaw=0),
                            ]
        temp = stub.GetIKControlInfos(GrabSim_pb2.HandPostureInfos(scene=self.sceneID, handPostureObjects=HandPostureObject))


    def move_to_obj(self,obj_id):
        scene = self.status
        obj_info = scene.objects[obj_id]
        # Robot
        obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
        walk_v = [obj_x + 50, obj_y] + [180, 180, 0]
        if obj_y >= 820 and obj_y <= 1200 and obj_x >= 240 and obj_x <= 500:  # 物品位于斜的抹布桌上 ([240,500],[820,1200])
            walk_v = [obj_x + 40, obj_y - 35, 130, 180, 0]
            obj_x += 3
            obj_y += 2.5
        walk_v[0]+=1
        print("walk:",walk_v)
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
        scene = stub.Do(action)
        print("After Walk Position:", [scene.location.X, scene.location.Y, scene.rotation.Yaw])


    # 移动到进行操作任务的指定地点
    def move_task_area(self, op_type, obj_id=0, release_pos=[247.0, 520.0, 100.0]):
        scene = self.status
        cur_pos = [scene.location.X, scene.location.Y, scene.rotation.Yaw]
        print("Current Position:", cur_pos, "开始任务:", self.op_dialog[op_type])
        if op_type == 11 or op_type == 12:  # 开关窗帘不需要移动
            return
        print('------------------moveTo_Area----------------------')
        if op_type < 8:    # 动画控制相关任务的移动目标
            walk_v = self.op_v_list[op_type] + [scene.rotation.Yaw, 180, 0]
        if 8 <= op_type <= 10:     # 控灯相关任务的移动目标
            walk_v = self.op_v_list[6] + [scene.rotation.Yaw, 180, 0]
        if op_type in [13,14,15]:          # 空调相关任务的移动目标
            walk_v = [240, -140.0] + [0, 180, 0]
        if op_type == 16:    # 抓握物体，移动到物体周围的可达区域
            scene = self.status
            obj_info = scene.objects[obj_id]
            obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
            walk_v = [obj_x + 50, obj_y] + [180, 180, 0]
            if 820 <= obj_y <= 1200 and 240 <= obj_x <= 500:  # 物品位于斜的抹布桌上 ([240,500],[820,1200])
                walk_v = [obj_x + 40, obj_y - 35, 130, 180, 0]
                obj_x += 3
                obj_y += 2.5
        if op_type == 17:   # 放置物体，移动到物体周围的可达区域
            walk_v = release_pos[:-1] + [180, 180, 0]
            if release_pos == [340.0, 900.0, 99.0]:
                walk_v[2] = 130
        # 移动到目标位置
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
        scene = stub.Do(action)
        print("After Walk Position:", [scene.location.X, scene.location.Y, scene.rotation.Yaw])



    # 相应的行动，由主办方封装
    def control_robot_action(self, type=0, action=0, message="你好"):
        scene = stub.ControlRobot(
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
    def adjust_kongtiao(self,op_type):
        obj_loc = self.obj_loc[:]
        obj_loc[2] -= 5
        if op_type == 13: obj_loc[1] -= 2
        if op_type == 14: obj_loc[1] -= 0
        if op_type == 15: obj_loc[1] += 2
        self.ik_control_joints(2, obj_loc[0], obj_loc[1], obj_loc[2])
        time.sleep(3.0)
        self.robo_recover()   # 恢复肢体关节
        return True

    def gen_obj(self,h=100):
        # 4;冰红(盒) 5;酸奶  7:保温杯 9;冰红(瓶) 13:代语词典  14:cake 61:甜牛奶
        scene = self.status
        ginger_loc = [scene.location.X, scene.location.Y, scene.location.Z]
        obj_list = [GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 40, z = 95, roll=0, pitch=0, yaw=0, type=5),
                    # GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 50, y=ginger_loc[1] - 40, z=h, roll=0, pitch=0, yaw=0, type=9),
                    # GrabSim_pb2.ObjectList.Object(x=340, y=960, z=88, roll=0, pitch=0, yaw=90, type=7),
                    # GrabSim_pb2.ObjectList.Object(x=340, y=960, z = 88, roll=0, pitch=0, yaw=90, type=9),
                    # GrabSim_pb2.ObjectList.Object(x=340, y=952, z=88, roll=0, pitch=0, yaw=90, type=4),
                    GrabSim_pb2.ObjectList.Object(x=-102, y=10, z=90, roll=0, pitch=0, yaw=90, type=7),
                    GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 55, y=ginger_loc[1] - 70, z=95, roll=0, pitch=0, yaw=0, type=9),

                    ]
        scene = stub.AddObjects(GrabSim_pb2.ObjectList(objects=obj_list, scene=self.sceneID))
        time.sleep(1.0)

    # 实现抓握操作
    def grasp_obj(self,obj_id,hand_id=1):
        print('------------------adjust_joints----------------------')
        scene = self.status
        obj_info = scene.objects[obj_id]
        obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
        if obj_info.name=="CoffeeCup":
            # obj_x += 1
            # obj_y -= 1
            # values = [0,0,0,0,0, 10,-25,-45,-45,-45]
            # values= [-6, 0, 0, 0, 0, -6, 0, 45, 45, 45]
            # stub.Do(GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Finger, values=values))
            pass
        if obj_info.name=="Glass":
            pass
        # Finger
        self.ik_control_joints(2, obj_x-9, obj_y, obj_z)   # -10, 0, 0
        time.sleep(3.0)
        # Grasp Obj
        print('------------------grasp_obj----------------------')
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Grasp, values=[hand_id, obj_id])
        scene = stub.Do(action)
        time.sleep(3.0)
        return True

    # robot的肢体恢复原位
    def robo_recover(self):
        action = GrabSim_pb2.Action(scene=self.sceneID,action=GrabSim_pb2.Action.ActionType.RotateJoints,    # 恢复原位
                                    values=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        scene = stub.Do(action)

    # 恢复手指关节
    def standard_finger(self):
        values = [0,0,0,0,0, 0,0,0,0,0]
        stub.Do(GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Finger, values=values))
        time.sleep(1.0)

    # 弯腰以及手掌与放置面平齐
    def robo_stoop_parallel(self):
        # 0-3是躯干，4-6是脖子和头，7-13是左胳膊，14-20是右胳膊
        scene = self.status
        angle = [scene.joints[i].angle for i in range(21)]
        angle[0] = 15   # 15
        angle[19] = -15
        angle[20] = -30
        action = GrabSim_pb2.Action(scene=self.sceneID,action=GrabSim_pb2.Action.ActionType.RotateJoints,    # 弯腰
                                    values=angle)
        scene = stub.Do(action)
        time.sleep(1.0)

    # 实现放置操作
    def release_obj(self,release_pos):
        print("------------------adjust_joints----------------------")
        if release_pos==[340.0, 900.0, 99.0]:
            self.ik_control_joints(2, release_pos[0]-40, release_pos[1]+35, release_pos[2])
            time.sleep(2.0)
        else:
            self.ik_control_joints(2, release_pos[0] - 80, release_pos[1], release_pos[2])
            time.sleep(2.0)
            self.robo_stoop_parallel()
        print("------------------release_obj----------------------")
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Release, values=[1])
        scene = stub.Do(action)
        time.sleep(2.0)
        self.robo_recover()       # 恢复肢体关节
        self.standard_finger()    # 恢复手指关节
        return True

    # 执行过程: Robot输出"开始(任务名)" -> 按步骤数执行任务 -> Robot输出成功或失败的对话
    def op_task_execute(self,op_type,obj_id=0,release_pos=[247.0, 520.0, 100.0]):
        self.control_robot_action(0, 1, "开始"+self.op_dialog[op_type])   # 输出正在执行的任务
        if op_type < 8:
            result = self.control_robot_action(op_type, 1)
        if 8 <= op_type <= 12:
            result = self.control_robot_action(self.op_typeToAct[op_type][0], self.op_typeToAct[op_type][1])
        if op_type in [13, 14, 15]:  # 调整空调:13代表按开关,14升温,15降温
            result = self.adjust_kongtiao(op_type)
        if op_type == 16:            # 抓握物体, 需要传入物品id
            result = self.grasp_obj(obj_id)
        if op_type == 17:            # 放置物体, 放置物品, 需要传入放置地点
            result = self.release_obj(release_pos)
        self.control_robot_action(0, 2)
        if result:
            if self.op_act_num[op_type]>0:
                for i in range(2,2+self.op_act_num[op_type]):
                    self.control_robot_action(op_type,i)
                    self.control_robot_action(0, 2)
            # self.control_robot_action(0, 1, "成功"+self.op_dialog[op_type])
        # else:
        #     self.control_robot_action(0, 1, self.op_dialog[op_type]+"失败")

    def find_obj(self,name):
        for id, item in enumerate(self.status.objects):
            if item.name == name:
                print("name:",name,"id:",id,"X:",item.location.X,"Y:",item.location.Y,"Z:",item.location.Z,)

    def test_move(self):
        v_list = [[0, 880], [250, 1200], [-55, 750], [70, -200]]
        scene = self.status
        for walk_v in v_list:
            walk_v = walk_v + [scene.rotation.Yaw - 90, 600, 100]
            print("walk_v", walk_v)
            action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
            scene = stub.Do(action)
            print(scene.info)

    def navigation_move(self, cur_objs, objs_name_set, cur_obstacle_world_points, v_list, map_ratio, scene_id=0, map_id=11):
        print('------------------navigation_move----------------------')
        scene = stub.Observe(GrabSim_pb2.SceneID(value=scene_id))
        walk_value = [scene.location.X, scene.location.Y]
        print("position:", walk_value)

        if not cur_objs:
            walk_v = [scene.location.X, scene.location.Y + 1]
            yaw = Navigator.get_yaw(walk_value, walk_v)
            walk_v = walk_value + [yaw, 250, 10]
            print("walk_v", walk_v)
            action = GrabSim_pb2.Action(scene=scene_id, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
            scene = stub.Do(action)
            cur_obstacle_world_points = camera.get_obstacle_point(scene, cur_obstacle_world_points,map_ratio)

            cur_objs, objs_name_set = camera.get_semantic_map(GrabSim_pb2.CameraName.Head_Segment, cur_objs,
                                                              objs_name_set)
            # if scene.info == "Unreachable":
            print(scene.info)

        # if map_id == 11:  # coffee
        #     v_list = [[0, 880], [250, 1200], [-55, 750], [70, -200]]
        # else:
        #     v_list = [[0.0, 0.0]]

        else:
            for walk_v in v_list:
                yaw = Navigator.get_yaw(walk_value, walk_v)
                walk_v = walk_v + [yaw, 250, 10]
                print("walk_v", walk_v)
                action = GrabSim_pb2.Action(scene=scene_id, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
                scene = stub.Do(action)

                cur_obstacle_world_points = camera.get_obstacle_point(scene, cur_obstacle_world_points, map_ratio)

                cur_objs, objs_name_set = camera.get_semantic_map(GrabSim_pb2.CameraName.Head_Segment, cur_objs,
                                                                  objs_name_set)
                # if scene.info == "Unreachable":
                print(scene.info)
        return cur_objs, objs_name_set, cur_obstacle_world_points

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
        scene = stub.Observe(GrabSim_pb2.SceneID(value=0))
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
            print(f"主动探索完成！以下是场景中可以到达的点：{free_array}；其余点均是障碍物不可达")

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



    def cal_distance_to_robot(self,objx,objy,objz):
        scene = self.status
        ginger_x, ginger_y, ginger_z = [int(scene.location.X), int(scene.location.Y),100]
        return math.sqrt((ginger_x - objx) ** 2 + (ginger_y - objy) ** 2 + (ginger_z - objz) ** 2)

    # 根据map文件判断是否可达
    def reachable(self, pos):
        x, y = self.real2map(pos[0], pos[1])
        if self.map_file[x, y] == 0:
            return True
        else:
            return False
