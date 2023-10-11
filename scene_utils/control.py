import time
import gym
import grpc
import numpy as np

from proto import GrabSim_pb2
from proto import GrabSim_pb2_grpc

from ptml import ptmlCompiler

channel = grpc.insecure_channel(
    "localhost:30001",
    options=[
        ("grpc.max_send_message_length", 1024 * 1024 * 1024),
        ("grpc.max_receive_message_length", 1024 * 1024 * 1024),
    ],
)
stub = GrabSim_pb2_grpc.GrabSimStub(channel)

animation_step = [4, 5, 7, 3, 3]


def init_world(scene_num, mapID):
    stub.SetWorld(GrabSim_pb2.BatchMap(count=scene_num, mapID=mapID))
    time.sleep(3)  # wait for the map to load


def walker_control_generator(walkerID, autowalk, speed, X, Y, Yaw):
    return GrabSim_pb2.WalkerControls.WControl(
        id=walkerID,
        autowalk=autowalk,
        speed=speed,
        pose=GrabSim_pb2.Pose(X=X, Y=Y, Yaw=Yaw),
    )


def image_extract(camera_data):
    image = camera_data.images[0]
    return np.frombuffer(image.data, dtype=image.dtype).reshape(
        (image.height, image.width, image.channels)
    )


class Scene:
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

    def __init__(self, sceneID):
        self.sceneID = sceneID
        self.BT = None
        self.reset()

    @property
    def status(self):
        return stub.Observe(GrabSim_pb2.SceneID(value=self.sceneID))

    def reset(self):
        stub.Reset(GrabSim_pb2.ResetParams(scene=self.sceneID))

    def walk_to(self, X, Y, Yaw, velocity, dis_limit):
        stub.Do(
            GrabSim_pb2.Action(
                scene=self.sceneID,
                action=GrabSim_pb2.Action.ActionType.WalkTo,
                values=[X, Y, Yaw, velocity, dis_limit],
            )
        )

    def reachable_check(self, X, Y, Yaw):
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

    def add_object(self, X, Y, Yaw, Z, type):
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

    def get_camera_color(self):
        camera_data = stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Color], scene=self.sceneID
            )
        )
        return image_extract(camera_data)

    def get_camera_depth(self):
        camera_data = stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Depth], scene=self.sceneID
            )
        )
        return image_extract(camera_data)

    def get_camera_segment(self):
        camera_data = stub.Capture(
            GrabSim_pb2.CameraList(
                cameras=[GrabSim_pb2.CameraName.Head_Segment], scene=self.sceneID
            )
        )
        return image_extract(camera_data)

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

    def load_BT(self, ptml_path):
        self.BT = ptmlCompiler.load(ptml_path, "ptml/behaviour_lib")
