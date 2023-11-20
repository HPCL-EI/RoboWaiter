import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Cond import Cond
import itertools

class NewCustomer(Cond):
    can_be_expanded = False
    num_params = 0
    valid_args = ()

    def __init__(self,*args):
        super().__init__(*args)


    def _update(self) -> ptree.common.Status:

        # 获取customer的位置
        # bar (247.0, 520.0, 100.0)
        close_to_bar = False
        scene = self.scene.status
        queue_list = []
        for walker in scene.walkers:
            x, y, yaw = walker.pose.X, walker.pose.Y, walker.pose.Yaw
            # 到达一定区域就打招呼
            if y >= 450 and y <= 620 and x >= 40 and x <= 100 and yaw>=-10 and yaw <=10: #450-620
                # close_to_bar = True
                queue_list.append((x,y,walker.name))

        if queue_list == []:
            return ptree.common.Status.FAILURE

        queue_list.sort()
        x,y,name = queue_list[0]
        if name not in self.scene.state["greeted_customers"]:
            self.scene.state['attention']["customer"] = name
            return ptree.common.Status.SUCCESS
        else:
            return ptree.common.Status.FAILURE