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
        if self.target_obj=="Coffee":
            self.op_type = 1
        elif self.target_obj=="Water":
            self.op_type = 2
        elif self.target_obj=="Dessert":
            self.op_type = 3


    @classmethod
    def get_info(cls,arg):
        info = {}
        info["pre"]= {f'Holding(Nothing)'}
        info['del_set'] = set()
        info['add'] = {f'Exist({arg})'}
        if arg == "Coffee":
            info["add"] |= {f'On(Coffee,CoffeeTable)'}
        elif arg == "Water":
            info["add"] |= {f'On(Water,WaterTable)'}
        elif arg == "Dessert":
            info["add"] |= {f'On(Dessert,Bar)'}
        return info

    def _update(self) -> ptree.common.Status:

        self.scene.move_task_area(self.op_type)
        self.scene.op_task_execute(self.op_type)

        # self.scene.gen_obj(type=40)

        obj_dict = self.scene.status.objects
        if len(obj_dict) != 0:
            # 获取obj_id
            for id, obj in enumerate(obj_dict):
                if obj.name == "CoffeeCup":
                    obj_info = obj_dict[id]
                    obj_x, obj_y, obj_z = obj_info.location.X, obj_info.location.Y, obj_info.location.Z
                    print(id,obj.name,obj_x,obj_y,obj_z)

        self.scene.state["condition_set"] |= (self.info["add"])
        self.scene.state["condition_set"] -= self.info["del_set"]

        return Status.RUNNING