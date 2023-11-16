import time
import math
import grpc
import numpy as np

import GrabSim_pb2
import GrabSim_pb2_grpc


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


def image_extract(camera_data):
    image = camera_data.images[0]
    return np.frombuffer(image.data, dtype=image.dtype).reshape(
        (image.height, image.width, image.channels)
    )


class Scene:
    robot = None
    event_list = []
    show_bubble = False

    default_state = {
        "map": {
            "2d": None,
            "obj_pos": {}
        },
        "chat_list": [],  # 未处理的顾客的对话, (顾客的位置,顾客对话的内容)
        "sub_goal_list": [],  # 子目标列表
        "status": None,  # 仿真器中的观测信息，见下方详细解释
        "condition_set": set()
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

        # init robot
        if robot:
            robot.set_scene(self)
            robot.load_BT()
        self.robot = robot

        # myx op
        # 1-7 正常执行, 8-10 控灯操作移动到6, 11-12窗帘操作不需要移动,
        self.op_dialog = ["","制作咖啡","倒水","夹点心","拖地","擦桌子","开筒灯","搬椅子",    # 1-7
                          "关筒灯","开大厅灯","关大厅灯","关闭窗帘","打开窗帘",              # 8-12
                          "调整空调开关","调高空调温度","调低空调温度",                      # 13-15
                          "抓握物体","放置物体"]                                         # 16-17
        self.op_act_num = [0,3,4,6,3,2,0,1,
                           0,0,0,0,0,
                           0,0,0,
                           0,0]
        self.op_v_list = [[[0.0,0.0]],[[250.0, 310.0]],[[-70.0, 480.0]],[[250.0, 630.0]],[[-70.0, 740.0]],[[260.0, 1120.0]],[[300.0, -220.0]],
                          [[0.0, -70.0]]]
        self.op_typeToAct = {8:[6,2],9:[6,3],10:[6,4],11:[8,1],12:[8,2]}
        # 空调面板位置
        self.obj_loc = [[300.5, -140.0,114]]


    def reset(self):
        # 基类reset，默认执行仿真器初始化操作
        self.reset_sim()

        # reset state
        self.state = self.default_state
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
        self._step()
        self.robot.step()

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
            print(f'顾客说：{sentence}')
            if self.show_bubble:
                self.chat_bubble(f'顾客说：{sentence}')
            self.state['chat_list'].append(f'{sentence}')

        return customer_say

    @property
    def status(self):
        return stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))

    def reset_sim(self):
        # reset world
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

    def walk_to(self, X, Y, Yaw=None, velocity=200, dis_limit=0):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]

        if Yaw is None:
            Yaw = self.status.rotation.Yaw

        v = [X, Y, Yaw - 90, velocity, dis_limit]
        print(v)
        action = GrabSim_pb2.Action(
            scene=self.sceneID,
            action=GrabSim_pb2.Action.ActionType.WalkTo,
            values=v
        )
        scene_info = stub.Do(action)
        return scene_info


    def reachable_check(self, X, Y, Yaw):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        navigation_info = stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.WalkTo,
                values=[X, Y, Yaw, 0, 0],
            )
        ).info
        if navigation_info == "Unreachable":
            return False
        else:
            return True

    def add_walker(self, X, Y, Yaw):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        if self.reachable_check(X, Y, Yaw):
            stub.AddWalker(
                GrabSim_pb2.WalkerList(
                    walkers=[
                        GrabSim_pb2.WalkerList.Walker(
                            id=0,
                            pose=GrabSim_pb2.Pose(
                                X=X, Y=Y, Yaw=Yaw
                            ),  # Parameter id is useless
                        )
                    ],
                    scene=self.sceneID,
                )
            )

    def remove_walker(self, *args):  # take single walkerID or a list of walkerIDs
        remove_list = []
        if isinstance(args[0], list):
            remove_list = args[0]
        else:
            for walkerID in args:
                # walkerID is the index of the walker in status.walkers.
                # Since status.walkers is a list, some walkerIDs would change after removing a walker.
                remove_list.append(walkerID)
        stub.RemoveWalkers(GrabSim_pb2.RemoveList(IDs=remove_list, scene=self.sceneID))

    def clean_walker(self):
        stub.CleanWalkers(GrabSim_pb2.SceneID(value=self.sceneID))

    def control_walker(self, control_list):
        stub.ControlWalkers(
            GrabSim_pb2.WalkerControls(controls=control_list, scene=self.sceneID)
        )

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
            return image_extract(camera_data)
        else:
            return camera_data

    def get_camera_depth(self, image_only=True):
        camera_data = stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Depth], scene=self.sceneID
            )
        )
        if image_only:
            return image_extract(camera_data)
        else:
            return camera_data

    def get_camera_segment(self, image_only=True):
        camera_data = stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Segment], scene=self.sceneID
            )
        )
        if image_only:
            return image_extract(camera_data)
        else:
            return camera_data

    def chat_bubble(self, message):
        stub.ControlRobot(
            GrabSim_pb2.ControlInfo(
                scene=self.sceneID, type=0, action=1, content=message
            )
        )

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

    # 移动到进行操作任务的指定地点
    # def move_task_area(self,op_type):
    #     if op_type==11 or op_type==12:  # 开关窗帘不需要移动
    #         return
    #     scene = stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))
    #     walk_value = [scene.location.X, scene.location.Y, scene.rotation.Yaw]
    #
    #     if op_type < 8:
    #         v_list = self.op_v_list[op_type]
    #     if op_type>=8 and op_type<=10:  # 控灯
    #         v_list = self.op_v_list[6]
    #     if op_type in [13,14,15]:   # 空调
    #         v_list = [[240, -140.0]]  # KongTiao [300.5, -140.0]  # 250
    #     print("------------------error version----------------------")
    #     print("------------------move_task_area----------------------")
    #     print("Current Position:", walk_value,"开始任务:",self.op_dialog[op_type])
    #     for walk_v in v_list:
    #         walk_v = walk_v + [scene.rotation.Yaw, 180, 0]
    #         walk_v[2] = 0 if (op_type in [13,14,15]) else scene.rotation.Yaw   # 空调操作朝向墙面
    #         action = GrabSim_pb2.Action(
    #             scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v
    #         )
    #         scene = stub.Do(action)
    #     print("After Walk Position:",[scene.location.X, scene.location.Y, scene.rotation.Yaw])

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

    def adjust_kongtiao(self,op_type):
        obj_loc = self.obj_loc[0][:]
        obj_loc[2] -= 5
        print("obj_loc:",obj_loc)
        if op_type == 13: obj_loc[1] -= 2
        if op_type == 14: obj_loc[1] -= 0
        if op_type == 15: obj_loc[1] += 2
        self.ik_control_joints(2, obj_loc[0], obj_loc[1], obj_loc[2])
        time.sleep(3.0)
        self.robo_recover()
        return True

    def gen_obj(self,h=100):
        # 4;冰红(盒) 5;酸奶  7:保温杯 9;冰红(瓶) 13:代语词典
        scene = stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))
        ginger_loc = [scene.location.X, scene.location.Y, scene.location.Z]
        obj_list = [GrabSim_pb2.ObjectList.Object(x=ginger_loc[0] - 50, y=ginger_loc[1] - 40, z = h, roll=0, pitch=0, yaw=0, type=9)]
        scene = stub.AddObjects(GrabSim_pb2.ObjectList(objects=obj_list, scene=self.sceneID))
        time.sleep(1.0)

    def grasp_obj(self,obj_id,hand_id=1):

        # Move to Obj
        print('------------------moveTo_obj----------------------')
        scene = stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))
        obj_info = scene.objects[obj_id]
        # Robot
        obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
        walk_v = [obj_x+50, obj_y] + [180, 180, 0]
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
        scene = stub.Do(action)
        time.sleep(1.0)
        # Finger
        self.ik_control_joints(2, obj_x-9, obj_y+0.5, obj_z)   # -10, 0, 0
        time.sleep(3.0)
        # Grasp Obj
        print('------------------grasp_obj----------------------')
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Grasp, values=[hand_id, obj_id])
        scene = stub.Do(action)
        time.sleep(4)
        return True

    # robot的肢体恢复原位
    def robo_recover(self):
        action = GrabSim_pb2.Action(scene=self.sceneID,action=GrabSim_pb2.Action.ActionType.RotateJoints,    # 恢复原位
                                    values=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        scene = stub.Do(action)


    def robo_stoop_parallel(self):
        # 0-3是躯干，4-6是脖子和头，7-13是左胳膊，14-20是右胳膊
        scene = stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))
        angle = [scene.joints[i].angle for i in range(21)]
        angle[0] = 15
        angle[19] = -15
        angle[20] = -30
        for i in range(18,21):
            print("name:",scene.joints[i].name,"angle:",scene.joints[i].angle)
        # print("angle:",angle)
        action = GrabSim_pb2.Action(scene=self.sceneID,action=GrabSim_pb2.Action.ActionType.RotateJoints,    # 弯腰
                                    values=angle)
        scene = stub.Do(action)
        time.sleep(1.0)

    def release_obj(self,release_pos):
        print("------------------Move to Realese Position----------------------")
        walk_v = [release_pos[i] for i in range(2)]
        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v + [180,180,0])
        scene = stub.Do(action)
        print("------------------release_obj----------------------")
        self.ik_control_joints(2, release_pos[0] - 80, release_pos[1], release_pos[2])
        time.sleep(2.0)
        self.robo_stoop_parallel()

        action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.Release, values=[1])
        scene = stub.Do(action)
        time.sleep(2.0)
        self.robo_recover()

        return True

    # 执行过程：输出"开始(任务名)" -> 按步骤数执行任务 -> Robot输出成功或失败的对话
    def op_task_execute(self,op_type,obj_id=0,yaw=180,release_pos=[240,-140]):
        self.control_robot_action(0, 1, "开始"+self.op_dialog[op_type])   # 开始制作咖啡
        if op_type in [13,14,15]:   # 调整空调:13代表按开关,14升温,15降温
            result = self.adjust_kongtiao(op_type)
        elif op_type ==16:
            result = self.grasp_obj(obj_id)
        elif op_type ==17:
            result = self.release_obj(release_pos)
        elif op_type>=8:
            result = self.control_robot_action(self.op_typeToAct[op_type][0], self.op_typeToAct[op_type][1])
            print("result:",result)
        else:
            result = self.control_robot_action(op_type, 1)    #
        self.control_robot_action(0, 2)
        if result:
            if self.op_act_num[op_type]>0:
                for i in range(2,2+self.op_act_num[op_type]):
                    self.control_robot_action(op_type,i)
                    self.control_robot_action(0, 2)
            # self.control_robot_action(0, 1, "成功"+self.op_dialog[op_type])
        # else:
        #     self.control_robot_action(0, 1, self.op_dialog[op_type]+"失败")

    def test_move(self):
        v_list = [[0, 880], [250, 1200], [-55, 750], [70, -200]]
        scene = self.status
        for walk_v in v_list:
            walk_v = walk_v + [scene.rotation.Yaw - 90, 600, 100]
            print("walk_v", walk_v)
            action = GrabSim_pb2.Action(scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v)
            scene = stub.Do(action)
            print(scene.info)



