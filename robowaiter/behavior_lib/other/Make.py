import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act
from robowaiter.behavior_lib._base.Behavior import Status

class Make(Act):
    can_be_expanded = True
    num_args = 1
    valid_args = (
        "Coffee","Water","Dessert"
    )

    def __init__(self, *args):
        super().__init__(*args)
        self.target_obj = self.args[0]
        self.op_type = 1
        if self.target_obj==self.valid_args[0]:
            self.op_type = 1
        elif self.target_obj==self.valid_args[1]:
            self.op_type = 2
        elif self.target_obj==self.valid_args[2]:
            self.op_type = 3


    @classmethod
    def get_info(cls,arg):
        info = {}
        info["pre"]= {f'Holding(Nothing)'}
        info['del_set'] = set()
        info['add'] = {f'Exist({arg})'}
        if arg == cls.valid_args[0]:
            info["add"] |= {f'On({arg},CoffeeTable)'}
        elif arg == cls.valid_args[1]:
            info["add"] |= {f'On({arg},WaterTable)'}
        elif arg == cls.valid_args[2]:
            info["add"] |= {f'On({arg},Bar)'}
        info['cost'] = 2
        return info

    def _update(self) -> ptree.common.Status:

        if self.scene.show_ui:
            self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio)

        self.scene.move_task_area(self.op_type)
        self.scene.op_task_execute(self.op_type)

        # self.scene.gen_obj(type=40)

        # obj_dict = self.scene.status.objects
        # if len(obj_dict) != 0:
        #     # 获取obj_id
        #     for id, obj in enumerate(obj_dict):
        #         print("id:",id,"obj",obj.name)

                # if obj.name == "Coffee":
                #     obj_info = obj_dict[id]
                #     obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
                #     print(id,obj.name,obj_x,obj_y,obj_z)
        if self.scene.show_ui:
            self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio,update_info_count=1)

        self.scene.state["condition_set"] |= (self.info["add"])
        self.scene.state["condition_set"] -= self.info["del_set"]

        # print("condition_set:",self.scene.state["condition_set"])

        return Status.RUNNING