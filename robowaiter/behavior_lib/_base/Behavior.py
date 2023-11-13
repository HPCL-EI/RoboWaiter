import py_trees as ptree
from typing import Any
import enum
from py_trees.common import Status


# _base Behavior
class Bahavior(ptree.behaviour.Behaviour):
    can_be_expanded = False
    num_params = 0
    valid_params='''
        None
        '''
    scene = None
    print_name_prefix = ""

    @classmethod
    def get_ins_name(cls,*args):
        name = cls.__name__
        if len(args) > 0:
            ins_name = f'{name}({",".join(list(args))})'
        else:
            ins_name = f'{name}()'
        return ins_name

    def __init__(self,*args):
        name = self.__class__.__name__
        if len(args)>0:
            name = f'{name}({",".join(list(args))})'
        self.name = name
        #get valid args
        # self.valid_arg_list = []
        # lines = self.valid_params.strip().splitlines()
        # for line in lines:
        #     self.valid_arg_list.append((x.strip for x in line.split(",")))
        self.args = args


        super().__init__(self.name)

    def _update(self) -> ptree.common.Status:
        print("this is just a _base behavior node.")
        return Status.INVALID

    @property
    def print_name(self):
        return f'{self.print_name_prefix}{self.get_ins_name(*self.args)}'



    # let behavior node interact with the scene
    def set_scene(self, scene):
        self.scene = scene

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)

    def initialise(self) -> None:
        return super().initialise()

    def update(self) -> Status:
        re = self._update()
        return re

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)

    @property
    def arg_str(self):
        return ",".join(self.args)