import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.algos.navigator.navigate import Navigator

class GreetCustomer(Act):
    can_be_expanded = True
    num_args = 0
    valid_args = ()

    def __init__(self, *args):
        super().__init__(*args)

    @classmethod
    def get_info(cls):
        info = {}
        info['pre'] = set()
        info["add"] = set()
        info["del_set"] = set()
        info['cost']=0
        return info

    def _update(self) -> ptree.common.Status:

        goal = Act.place_xyz_dic['Bar']
        self.scene.walk_to(goal[0]-5,goal[1], 180, 180, 0)
        self.scene.chat_bubble("欢迎光临！请问有什么可以帮您？")

        customer_name = self.scene.state['attention']['customer']
        self.scene.state['greeted_customers'].add(customer_name)

        return ptree.common.Status.RUNNING
