import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond

class AnomalyDetected(Cond):


    def __init__(self):
        super().__init__()


    def _update(self) -> ptree.common.Status:
        # if self.scene.status?

        light_set = {'Is(HallLight,Off)', 'Is(TubeLight,Off)', 'Is(Curtain,Off)'}
        if light_set.issubset(self.scene.state["condition_set"]):
            self.scene.state["anomaly"] = "NoLight"
            return ptree.common.Status.SUCCESS

        # light_set = {'Is(Curtain,On)'}
        # if light_set.issubset(self.scene.state["condition_set"]):
        #     self.scene.chat_bubble("太暗了，开灯")
        #     self.scene.state["anomaly"] = "NoLight"
        #     return ptree.common.Status.SUCCESS


        return  ptree.common.Status.FAILURE
