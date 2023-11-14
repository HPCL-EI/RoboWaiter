from robowaiter.behavior_lib._base.Behavior import Bahavior

class Act(Bahavior):
    print_name_prefix = "act "
    type = 'Act'
    all_place = {'Bar', 'Bar2', 'WaterTable', 'CoffeeTable', 'Table1', 'Table2', 'Table3'}
    all_object = {'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk',
                  'VacuumCup'}
    place_xyz_dic={
        'Bar': (247.0, 520.0, 100.0),
        'Bar2': (240.0, 40.0, 70.0),
        'WaterTable':(-70.0, 500.0, 107),
        'CoffeeTable':(247.0, 520.0, 100.0), # 位置需要更改！！！
        'Table1': (247.0, 520.0, 100.0),# 位置需要更改！！！
        'Table2': (-55.0, 0.0, 107),
        'Table3':(-55.0, 150.0, 107)
    }
    def __init__(self,*args):
        super().__init__(*args)
        self.info = self.get_info(*args)

    @classmethod
    def get_info(self,*arg):
        return None
