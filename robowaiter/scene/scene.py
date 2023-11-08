import time
import grpc
import numpy as np

from robowaiter.proto import GrabSim_pb2
from robowaiter.proto import GrabSim_pb2_grpc


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

    default_state = {
        "map": {
            "2d": None,
            "obj_pos": {}
        },
        "chat_list": [],  # 未处理的顾客的对话, (顾客的位置,顾客对话的内容)
        "sub_goal_list": [],  # 子目标列表
        "status": None,  # 仿真器中的观测信息，见下方详细解释
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
        self.use_offset = True
        self.start_time = time.time()
        self.time = 0

        # init robot
        if robot:
            robot.set_scene(self)
            robot.load_BT()
        self.robot = robot
        self.sub_task_seq = None

        # myx op
        # 1-7 正常执行, 8-10 移动到6, 11-12不需要移动
        self.op_dialog = ["","制作咖啡","倒水","夹点心","拖地","擦桌子","开筒灯","搬椅子","关筒灯","开大厅灯","关大厅灯","关闭窗帘","打开窗帘"]
        self.op_act_num = [0,3,4,6,3,2,0,1,0,0,0,0,0]
        self.op_v_list = [[[0.0,0.0]],[[250.0, 310.0]],[[-70.0, 480.0]],[[250.0, 630.0]],[[-70.0, 740.0]],[[260.0, 1120.0]],[[300.0, -220.0]],[[0.0, -70.0]]]
        self.op_typeToAct = {8:[6,2],9:[6,3],10:[6,4],11:[8,1],12:[8,2]}


    def _reset(self):
        # 场景自定义的reset
        pass

    def _run(self):
        # 场景自定义的run
        pass

    def _step(self):
        # 场景自定义的step
        pass


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
            self.chat_bubble(f'顾客说：{sentence}')
            self.state['chat_list'].append(f'{sentence}')

        return customer_say

    @property
    def status(self):
        return stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))

    def reset_sim(self):
        stub.Reset(GrabSim_pb2.ResetParams(scene=self.sceneID))

        # reset world
        init_world()


    def walker_control_generator(self, walkerID, autowalk, speed, X, Y, Yaw):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        return GrabSim_pb2.WalkerControls.WControl(
            id=walkerID,
            autowalk=autowalk,
            speed=speed,
            pose=GrabSim_pb2.Pose(X=X, Y=Y, Yaw=Yaw),
        )

    def walk_to(self, X, Y, Yaw, velocity=150, dis_limit=100):
        if self.use_offset:
            X, Y = X + loc_offset[0], Y + loc_offset[1]
        stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.WalkTo,
                values=[X, Y, Yaw, velocity, dis_limit],
            )
        )

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

    def op_task_execute(self,op_type):
        print("type:",self.op_typeToAct[op_type][0],"action:",self.op_typeToAct[op_type][1])
        self.control_robot_action(0, 1, "开始"+self.op_dialog[op_type])   # 开始制作咖啡
        if op_type>=8:
            result = self.control_robot_action(self.op_typeToAct[op_type][0], self.op_typeToAct[op_type][1])
        else:
            result = self.control_robot_action(op_type, 1)    #
        self.control_robot_action(0, 2)
        if result:
            print("op_num:",self.op_act_num[op_type])
            if self.op_act_num[op_type]>0:
                for i in range(2,2+self.op_act_num[op_type]):
                    self.control_robot_action(op_type,i)
                    self.control_robot_action(0, 2)
            self.control_robot_action(0, 1, "成功"+self.op_dialog[op_type])
        else:
            self.control_robot_action(0, 1, self.op_dialog[op_type]+"失败")

    def move_task_area(self,op_type=1):
        if op_type>=8 and op_type<=10:
            v_list = self.op_v_list[6]
        else:
            v_list = self.op_v_list[op_type]
        scene = stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))

        walk_value = [scene.location.X, scene.location.Y, scene.rotation.Yaw]
        print("------------------move_task_area----------------------")
        print("position:", walk_value,"开始任务:",self.op_dialog[op_type])
        for walk_v in v_list:
            walk_v = walk_v + [scene.rotation.Yaw, 60, 0]
            action = GrabSim_pb2.Action(
                scene=self.sceneID, action=GrabSim_pb2.Action.ActionType.WalkTo, values=walk_v
            )
            scene = stub.Do(action)


