import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.algos.navigator.navigate import Navigator

class ServeCustomer(Act):

    def __init__(self, *args):
        super().__init__(*args)

    @classmethod
    def get_info(cls):
        info = {}
        info['pre'] = set()
        info["add"] = {"CustomerServed()"}
        info["del_set"] = set()
        info['cost']=0
        return info

    def _update(self) -> ptree.common.Status:
        # if self.scene.time - self.scene.state["serve_state"]["last_chat_time"] > 10:
        #     self.chat_bubble

        goal = Act.place_xyz_dic['Bar']
        self.scene.walk_to(goal[0]-5,goal[1], 180, 180, 0)
        if self.scene.show_bubble:
            self.scene.chat_bubble("欢迎光临！请问有什么可以帮您？")
        return ptree.common.Status.RUNNING
