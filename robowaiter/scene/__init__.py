
from .scene import Scene
from robowaiter.scene.tasks.AEM import SceneAEM
from robowaiter.scene.tasks.GQA import SceneGQA
from robowaiter.scene.tasks.VLN import SceneVLN
from robowaiter.scene.tasks.VLM import SceneVLM
from robowaiter.scene.tasks.Open_tasks import SceneOT
from robowaiter.scene.tasks.Auto_tasks import SceneAT

task_map = {
    "AEM": SceneAEM,
    "GQA": SceneGQA,
    "VLN": SceneVLN,
    "VLM": SceneVLM,
    "OT": SceneOT,
    "AT": SceneAT,
}