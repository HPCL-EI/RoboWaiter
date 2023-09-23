import gym
import grpc
from proto import GrabSim_pb2
from proto import GrabSim_pb2_grpc

channel = grpc.insecure_channel(
    "localhost:30001",
    options=[
        ("grpc.max_send_message_length", 1024 * 1024 * 1024),
        ("grpc.max_receive_message_length", 1024 * 1024 * 1024),
    ],
)
stub = GrabSim_pb2_grpc.GrabSimStub(channel)


def init_world(scene_num, mapID):
    stub.SetWorld(GrabSim_pb2.BatchMap(count=scene_num, mapID=mapID))


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
        self.walkerID_set = set()
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
            walkerID = 0 if not self.walkerID_set else max(self.walkerID_set) + 1
            stub.AddWalker(
                GrabSim_pb2.WalkerList(
                    walkers=[
                        GrabSim_pb2.WalkerList.Walker(
                            id=walkerID, pose=GrabSim_pb2.Pose(X=X, Y=Y, Yaw=Yaw)
                        )
                    ],
                    scene=self.sceneID,
                )
            )
            self.walkerID_set.add(walkerID)
            return walkerID
        else:
            return None

    def remove_walker(self, *args):
        remove_list = []
        for walkerID in args:
            if walkerID in self.walkerID_set:
                remove_list.append(walkerID)
                self.walkerID_set.remove(walkerID)
        stub.RemoveWalkers(GrabSim_pb2.RemoveList(IDs=remove_list, scene=self.sceneID))

    def clean_walker(self):
        stub.CleanWalkers(GrabSim_pb2.SceneID(value=self.sceneID))

    def walker_control_generator(self, walkerID, autowalk, speed, X, Y, Yaw):
        return GrabSim_pb2.WalkerControls.WControl(
            id=walkerID,
            autowalk=autowalk,
            speed=speed,
            pose=GrabSim_pb2.Pose(X=X, Y=Y, Yaw=Yaw),
        )

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

