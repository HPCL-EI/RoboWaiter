import py_trees as ptree
from robowaiter.behavior_lib._base.Act import Act

class MoveTo(Act):
    can_be_expanded = True
    num_args = 1
    valid_args = Act.all_object | Act.tables_for_placement | Act.tables_for_guiding
    # valid_args.add('Customer')

    def __init__(self, target_place):
        super().__init__(target_place)
        self.target_place = target_place

    @classmethod
    def get_info(cls,arg):
        info = {}
        info['pre'] = set()
        if arg in Act.all_object:
            info['pre'] |= {f'Exists({arg})'}
        # info['pre'] |= {f'Not RobotNear({arg})'}

        info["add"] = {f'RobotNear({arg})'}
        info["add"] |= {f'Not RobotNear({place})' for place in cls.valid_args if place != arg}

        info["del_set"] = {f'RobotNear({place})' for place in cls.valid_args if place != arg}
        info["del_set"] |= {f'Not RobotNear({arg})'}

        info['cost'] = 10
        return info

    def _update(self) -> ptree.common.Status:
        # self.scene.test_move()

        # navigator = Navigator(scene=self.scene, area_range=[-350, 600, -400, 1450], map=self.scene.state["map"]["2d"])
        # goal = self.scene.state['map']['obj_pos'][self.args[0]]
        # navigator.navigate_old(goal, animation=False)

        # 拍照片
        if self.scene.show_ui:
            self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio, is_nav=True)

        # #####################################
        # 走到固定的地点
        if self.target_place in Act.place_xy_yaw_dic:
            goal = Act.place_xy_yaw_dic[self.target_place]
            if self.scene.is_nav_walk:
                self.scene.navigator.navigate(goal=(goal[0] + 1, goal[1]), animation=False)
                self.scene.walk_to(goal[0]+2, goal[1], goal[2])
            else:
                self.scene.walk_to(goal[0]+1,goal[1],goal[2])
        # 走到物品边上
        else:
            # 是否用容器装好
            if self.target_place in Act.container_dic:
                target_name = Act.container_dic[self.target_place]
            else:
                target_name = self.target_place
            # 根据物体名字找到最近的这类物体对应的位置
            obj_id = -1
            min_dis = float('inf')
            obj_dict = self.scene.status.objects
            if len(obj_dict)!=0:
                # 获取obj_id
                for id,obj in enumerate(obj_dict):
                    if obj.name == target_name:
                        obj_info = obj_dict[id]
                        dis = self.scene.cal_distance_to_robot(obj_info.location.X, obj_info.location.Y, obj_info.location.Z)
                        if dis<min_dis:
                            min_dis = dis
                            obj_id = id
            if obj_id == -1:
                return ptree.common.Status.FAILURE
            self.scene.move_to_obj(obj_id=obj_id)
            # #####################################

        if self.scene.show_ui:
            self.scene.get_obstacle_point(self.scene.db, self.status, map_ratio=self.scene.map_ratio, is_nav=True)


        self.scene.state["condition_set"] |= (self.info["add"])
        self.scene.state["condition_set"] -= self.info["del_set"]
        return ptree.common.Status.RUNNING
