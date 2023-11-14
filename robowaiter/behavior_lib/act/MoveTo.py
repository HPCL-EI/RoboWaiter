import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.algos.navigate.navigate import Navigator

class MoveTo(Act):
    can_be_expanded = True
    num_args = 1
    valid_args = Act.all_object | Act.all_place
    valid_args.add('Customer')

    def __init__(self, target_place):
        super().__init__(target_place)
        self.target_place = target_place


    @classmethod
    def get_info(cls,arg):
        info = {}
        info['pre'] = set()
        info["add"] = {f'At(Robot,{arg})'}
        info["del_set"] = {f'At(Robot,{place})' for place in cls.valid_args if place != arg}
        return info


    def _update(self) -> ptree.common.Status:
        # self.scene.test_move()

        # navigator = Navigator(scene=self.scene, area_range=[-350, 600, -400, 1450], map=self.scene.state["map"]["2d"])
        # goal = self.scene.state['map']['obj_pos'][self.args[0]]
        # navigator.navigate(goal, animation=False)

        if self.target_place in Act.place_xyz_dic:
            goal = Act.place_xyz_dic[self.target_place]
            self.scene.walk_to(goal[0],goal[1])
        else:
            # 获取obj_id
            for id,obj in enumerate(self.scene.objects):
                if obj.name == self.target_place:
                    obj_id = id
                    break

            obj_info = self.scene.objects[obj_id]
            obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
            self.scene.walk_to(obj_x,obj_y)

        # goal = self.scene.state['map']['obj_pos'][self.args[0]]
        # self.scene.walk_to(goal[0],goal[1]) # X, Y, Yaw=None, velocity=200, dis_limit=0


        self.scene.state["condition_set"] |= (self.info["add"])
        self.scene.state["condition_set"] -= self.info["del_set"]
        return ptree.common.Status.RUNNING
