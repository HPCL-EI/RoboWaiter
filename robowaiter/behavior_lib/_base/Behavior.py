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
    # all_place = {'Bar', 'Bar2', 'WaterTable', 'CoffeeTable', 'Table1', 'Table2', 'Table3'}
    # all_object = {'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk',
    #               'VacuumCup'}
    all_place = {'Bar', 'WaterTable', 'CoffeeTable'}
    # all_object = {'Coffee', 'Water', 'Dessert', 'Softdrink', 'Yogurt'}
    all_object = {'Coffee', 'Water'}
    place_xyz_dic={
        'Bar': (247.0, 520.0, 100.0),
        'Bar2': (240.0, 40.0, 70.0),
        'WaterTable':(-70.0, 500.0, 107),
        'CoffeeTable':(250.0, 310.0, 100.0),
        'Table1': (340.0, 900.0, 98.0),
        'Table2': (-55.0, 0.0, 107),
        'Table3':(-55.0, 150.0, 107)
    }
    container_dic={
        'Coffee':'CoffeeCup',
        'Water': 'Glass',
        'Dessert':'Plate'
    }
    
    @classmethod
    def get_ins_name(cls,*args):
        name = cls.__name__
        if len(args) > 0:
            ins_name = f'{name}({",".join(list(args))})'
        else:
            ins_name = f'{name}()'
        return ins_name

    def __init__(self,*args):
        ins_name = self.__class__.get_ins_name(*args)
        self.args = args

        super().__init__(ins_name)

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