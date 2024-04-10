import py_trees as ptree
from EXP.behavior_lib._base.Act import Act

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
