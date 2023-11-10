import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.algos.navigate.DstarLite.navigate import Navigator

class MoveTo(Act):

    def __init__(self, *args):
        super().__init__(*args)

    def _update(self) -> ptree.common.Status:
        # self.scene.test_move()

        navigator = Navigator(scene=self.scene, area_range=[-350, 600, -400, 1450], map=self.scene.state["map"]["2d"])
        goal = self.scene.state['map']['obj_pos'][self.args[0]]
        navigator.navigate(goal, animation=False)

        self.scene.state['condition_set'].add('At(Robot,Table)')


        return ptree.common.Status.RUNNING
