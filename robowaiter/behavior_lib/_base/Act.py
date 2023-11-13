from robowaiter.behavior_lib._base.Behavior import Bahavior

class Act(Bahavior):
    print_name_prefix = "act "
    type = 'Act'
    all_place = {'Bar', 'WaterTable', 'CoffeeTable', 'Bar2', 'Table1', 'Table2', 'Table3'}
    all_object = {'Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk',
                  'VacuumCup'}

    def __init__(self,*args):
        super().__init__(*args)
        self.info = self.get_info(*args)

    @classmethod
    def get_info(self,*arg):
        return None
