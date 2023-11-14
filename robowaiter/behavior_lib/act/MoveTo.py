import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.algos.navigate.navigate import Navigator

class MoveTo(Act):
    can_be_expanded = True
    num_args = 1
    valid_args = (
        "Bar",
        "Table",
    )

    def __init__(self, target_place):
        super().__init__(target_place)
        self.target_place = target_place


    @classmethod
    def get_info(self,arg):
        info = {
            "add": {f'At(Robot,{arg})'},
        }
        return info


    def _update(self) -> ptree.common.Status:
        # self.scene.test_move()

        navigator = Navigator(scene=self.scene, area_range=[-350, 600, -400, 1450], map=self.scene.state["map"]["2d"])
        goal = self.scene.state['map']['obj_pos'][self.args[0]]
        navigator.navigate(goal, animation=False)

        self.scene.state['condition_set'].add('At(Robot,Table)')

        # goal = self.scene.state['map']['obj_pos'][self.args[0]]
        # self.scene.walk_to(goal[0],goal[1])

        return ptree.common.Status.RUNNING
