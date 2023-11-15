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
        if arg in Act.all_object:
            info['pre'] |= {f'Exist({arg})'}
        info["add"] = {f'At(Robot,{arg})'}
        info["del_set"] = {f'At(Robot,{place})' for place in cls.valid_args if place != arg}
        return info


    def _update(self) -> ptree.common.Status:
        # self.scene.test_move()

        # navigator = Navigator(scene=self.scene, area_range=[-350, 600, -400, 1450], map=self.scene.state["map"]["2d"])
        # goal = self.scene.state['map']['obj_pos'][self.args[0]]
        # navigator.navigate(goal, animation=False)

        # 走到固定的地点
        if self.target_place in Act.place_xyz_dic:
            goal = Act.place_xyz_dic[self.target_place]
            self.scene.walk_to(goal[0],goal[1])
        else: # 走到物品边上

            self.scene.move_task_area(16, obj_id=273)
            self.scene.op_task_execute(16, obj_id=273)

            # obj_id = -1
            # obj_dict = self.scene.status.objects
            # if len(obj_dict)!=0:
            #     # 获取obj_id
            #     for id,obj in enumerate(obj_dict):
            #         if obj.name == self.target_place:
            #             obj_id = id
            #             break
            #     # 为了演示，写死咖啡位置
            #     if self.target_place=="Coffee":
            #         obj_id = 273
            # if obj_id == -1:
            #     return ptree.common.Status.FAILURE
            # obj_info = obj_dict[obj_id]
            # obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
            # self.scene.walk_to(obj_x,obj_y)
            # print("MoveTo",obj_x, obj_y, obj_z," obj_id:",obj_id," obj_info:",obj_info.name)


        # goal = self.scene.state['map']['obj_pos'][self.args[0]]
        # self.scene.walk_to(goal[0],goal[1]) # X, Y, Yaw=None, velocity=200, dis_limit=0


        self.scene.state["condition_set"] |= (self.info["add"])
        self.scene.state["condition_set"] -= self.info["del_set"]
        return ptree.common.Status.RUNNING
