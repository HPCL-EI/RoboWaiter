import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.algos.navigator.navigate import Navigator

class GreetCustomer(Act):
    can_be_expanded = False
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

        goal = Act.place_xy_yaw_dic['Bar']
        if self.scene.is_nav_walk:
            self.scene.navigator.navigate(goal=(goal[0]-5,goal[1]), animation=False)
            self.scene.walk_to(goal[0] - 4, goal[1], 180, 180, 0)
        else:
            self.scene.walk_to(goal[0] - 5, goal[1], 180, 180, 0)

        # if self.scene.show_bubble:
        #     # self.scene.chat_bubble("欢迎光临！")
        #     # self.scene.chat_bubble("欢迎光临！请问有什么可以帮您？")
        #     self.scene.chat_bubble("Welcome! How can I help you?")

        customer_name = self.scene.state['attention']['customer']
        self.scene.state['greeted_customers'].add(customer_name)



        return ptree.common.Status.RUNNING
