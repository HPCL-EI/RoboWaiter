import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class PickUp(Act):
    can_be_expanded = True
    num_args = 1
    valid_args = Act.all_object
    # valid_args.add("Anything")
    def __init__(self, *args):
        super().__init__(*args)
        self.target_obj = self.args[0]


    @classmethod
    def get_info(cls,arg):
        info = {}
        info["pre"] = {f'At(Robot,{arg})','Holding(Nothing)'}
        info["add"] = {f'Holding({arg})'}
        info["del_set"] = {f'Holding(Nothing)',f'Exist({arg})'} #,
        for place in cls.valid_args:
            info["del_set"] |= {f'On({arg},{place})'}
        info['cost'] = 2

        # if arg != 'Anything':
        #     info['cost'] = 1
        # else:
        #     info['cost'] = 0
        #
        #     info["pre"] = {}

        return info


    def _update(self) -> ptree.common.Status:
        # self.scene.test_move()
        # op_type=16

        # 遍历场景里的所有物品，根据名字匹配位置最近的 obj-id
        # 是否用容器装好
        if self.target_obj in Act.container_dic:
            target_name = Act.container_dic[self.target_obj]
        else:
            target_name = self.target_obj
        # 根据物体名字找到最近的这类物体对应的位置
        obj_id = -1
        min_dis = float('inf')
        obj_dict = self.scene.status.objects
        if len(obj_dict) != 0:
            # 获取obj_id
            for id, obj in enumerate(obj_dict):
                if obj.name == target_name:
                    obj_info = obj_dict[id]
                    dis = self.scene.cal_distance_to_robot(obj_info.location.X, obj_info.location.Y,
                                                           obj_info.location.Z)
                    if dis < min_dis:
                        min_dis = dis
                        obj_id = id
        # if self.target_place == "CoffeeCup":
        #     # obj_id = 273
        #     obj_id = 275
        if obj_id == -1:
            return ptree.common.Status.FAILURE

        self.scene.move_task_area(op_type=16, obj_id=obj_id)
        self.scene.op_task_execute(op_type=16, obj_id=obj_id)

        if self.scene.show_ui:
            self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio,update_info_count=1)

        self.scene.state["condition_set"] |= (self.info["add"])
        self.scene.state["condition_set"] -= self.info["del_set"]
        return Status.RUNNING
