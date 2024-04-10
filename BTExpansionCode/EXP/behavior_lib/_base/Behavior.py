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

    # tables_for_guiding = {"QuietTable1","QuietTable2",
    #                       "BrightTable1","BrightTable2","BrightTable3","BrightTable4","BrightTable5","BrightTable6",
    #                       'CoffeeTable','WaterTable','Table1', 'Table2', 'Table3'}
    tables_for_guiding = set()

    tables_for_placement = {
        # 'Bar', 'Bar2',  'Table',
        #                     'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3','WindowTable6',
        #                     "QuietTable1", "QuietTable2",
        #                     "BrightTable1", "BrightTable2", "BrightTable3", "BrightTable4", "BrightTable5",
        'Bar', 'Bar2', 'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3', 'WindowTable6', #'Table',
        'WindowTable4', 'WindowTable5',
        'QuietTable1', 'QuietTable2', 'QuietTable3', 'ReadingNook', 'Entrance', 'Exit', 'LoungeArea', 'HighSeats',
        'VIPLounge', 'MerchZone' #20

    }

    all_place = tables_for_guiding | tables_for_placement

    all_object = {
        'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk', 'VacuumCup',
        'Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater', #'Tea' #15

        'Apple', 'Banana', 'Mangosteen', 'Orange',
        'Kettle', 'PaperCup', 'Bread', 'LunchBox',
        'Teacup', 'Chocolate', 'Sandwiches', 'Mugs',
        'Watermelon', 'Tomato', 'CleansingFoam','CocountMilk',
        'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup',
        'Tissue', 'YogurtDrink', 'Newspaper', 'Box',
        'PaperCupStarbucks', 'CoffeeMachine', 'Straw', 'Cake',
        'Tray', 'Bread','Glass', 'Door',
        'Mug', 'Machine','PackagedCoffee', 'CubeSugar',
        'Apple', 'Spoon','Drinks', 'Drink',
        'Ice', 'Saucer','TrashBin', 'Knife','Cube'
        #45



        # 'Coffee', 'Water', 'Dessert', 'Softdrink','Tea',
        # 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk','VacuumCup',
        # 'Chips', 'NFCJuice', 'Bernachon', 'SpringWater',
        # 'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk',
        #  'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup',
        #  'Tissue', 'YogurtDrink', 'Newspaper', 'Box',
        #  'PaperCupStarbucks', 'CoffeeMachine', 'GingerLHand', 'GingerRHand',
        #  'Straw', 'Cake', 'Tray', 'Bread',
        #  'Glass', 'Door', 'Mug', 'Machine',
        #  'PackagedCoffee', 'CubeSugar', 'Apple', 'Spoon',
        #  'Drinks', 'Drink', 'Take-AwayCup', 'Saucer',
        #  'TrashBin', 'Knife', 'Ginger', 'Floor',
        #  'Roof', 'Wall'
        }

    # tables_for_placement = {'Bar', 'WaterTable', 'CoffeeTable', 'Table1'}

    # easy——easy
    # all_object = {
    #     'Coffee', 'Water', 'Dessert', 'Yogurt'}



    # all_object = {
    #     'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk','VacuumCup',
    #     'Chips', 'NFCJuice', 'Bernachon', 'SpringWater',
    #
    #
        # 'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk',
        #  'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup',
        #  'Tissue', 'YogurtDrink', 'Newspaper', 'Box',
        #  'PaperCupStarbucks', 'CoffeeMachine', 'GingerLHand', 'GingerRHand',
        #  'Straw', 'Cake', 'Tray', 'Bread',
        #  'Glass', 'Door', 'Mug', 'Machine',
        #  'PackagedCoffee', 'CubeSugar', 'Apple', 'Spoon',
        #  'Drinks', 'Drink', 'Take-AwayCup', 'Saucer',
        #  'TrashBin', 'Knife', 'Ginger', 'Floor',
        #  'Roof', 'Wall'
    # }

    # all_object = {
    #     'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk','VacuumCup',
    #     'Chips', 'NFCJuice', 'Bernachon', 'SpringWater'}

    # all_object.update({'CleansingFoam', 'CocountMilk', 'Tomato'})

    # all_object.update({'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk',
    #  'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup',
    #  'TrashBin', 'Knife', 'Ginger', 'Floor',
    # 'Straw', 'Cake', 'Tray', 'Bread',
    #  'Roof', 'Wall'})




    # all_object.update({'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk',
    #  'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup',
    #  'Tissue', 'YogurtDrink', 'Newspaper', 'Box',
    #  'PaperCupStarbucks', 'CoffeeMachine', 'GingerLHand', 'GingerRHand',
    #  'Straw', 'Cake', 'Tray', 'Bread',
    #  'Glass', 'Door', 'Mug', 'Machine',
    #  'PackagedCoffee', 'CubeSugar', 'Apple', 'Spoon',
    #  'Drinks', 'Drink', 'Take-AwayCup', 'Saucer',
    #  'TrashBin', 'Knife', 'Ginger', 'Floor',
    #  'Roof', 'Wall'})


    # tables_for_guiding = set()


    # tables_for_placement = {'Bar', 'CoffeeTable', 'Table2',"BrightTable6", 'WaterTable'}
    # all_object = {'Coffee', 'Yogurt'}


    num_of_obj_on_place={
        'Bar': 0,  # (247.0, 520.0, 100.0)
        'Bar2': 0,
        'WaterTable': 0,
        'CoffeeTable': 0,
        'Table1': 0,
        'Table2': 0,
        'Table3': 0,
        'BrightTable6': 0,
    }

    place_xyz_dic={
        'Bar': (247.0, 520.0, 100.0), #(247.0, 520.0, 100.0)
        'Bar2': (240.0, 40.0, 100.0),
        'WaterTable':(-70.0, 500.0, 107),
        'CoffeeTable':(250.0, 310.0, 100.0),
        'Table1': (340.0, 900.0, 99.0),
        'Table2': (-55.0, 0.0, 107),
        'Table3':(-55.0, 150.0, 107),
        'BrightTable6': (5, -315, 116.5),
    }

    place_have_obj_xyz_dic = {
        'QuietTable1': (480, 1300, 70),
        'QuietTable2': (250, -240, 70),
        'BrightTable1': (230, 1200, 35),
        'BrightTable2': (65, 1000, 35),
        'BrightTable3': (-80, 850, 35),
        'BrightTable4': (-270, 520, 70),
        'BrightTable5': (-270, 420, 35)
    }
    place_have_obj_xyz_dic.update(place_xyz_dic)

    place_en2zh_name={
        'Bar': "吧台",
        'Bar2': "另一侧的吧台",
        'WaterTable': "大厅的茶水桌",
        'CoffeeTable': "咖啡桌",
        'Table1': "前门斜桌子",
        'Table2': "大厅长桌子西侧",
        'Table3': "大厅长桌子东侧",
        'BrightTable6': "后门靠窗边圆桌",
        'QuietTable1': "前门角落双人圆桌",
        'QuietTable2': "后门角落三人圆桌",
        'BrightTable1': "靠窗边第一个四人矮桌",
        'BrightTable2': "靠窗边第二个四人矮桌",
        'BrightTable3': "靠窗边第三个四人矮桌",
        'BrightTable4': "大厅里靠窗边长桌子",
        'BrightTable5': "大厅里靠窗边多人矮桌",
    }

    place_xy_yaw_dic={
        'Bar': (247.0, 520.0, 180),  # (247.0, 520.0, 100.0)
        'Bar2': (240.0, 40.0, 100.0),
        'WaterTable': (-70.0, 500.0, 107),
        'CoffeeTable': (250.0, 310.0, 100.0),
        'Table1': (340.0, 900.0, 99.0),
        'Table2': (-55.0, 0.0, 107),
        'Table3': (-55.0, 150.0, 107),
        'BrightTable6': (5, -315, 116.5),

        'QuietTable1':(480,1300,90),
        'QuietTable2':(250,-240,-65),
        'BrightTable1':(230,1200,-135),
        'BrightTable2': (65, 1000, 135),
        'BrightTable3': (-80, 850, 135),
        'BrightTable4': (-270, 520, 150),
        'BrightTable5': (-270, 420, 90) #(-270, 420, -135)
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



    # let behavior node Interact with the scene
    def set_scene(self, scene=None):
        if scene:
            self.scene = scene
            self.robot = scene.robot

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