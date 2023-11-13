from robowaiter.behavior_lib._base.Behavior import Bahavior

class Act(Bahavior):
    print_name_prefix = "act "
    type = 'Act'

    def __init__(self,*args):
        super().__init__(*args)

    def get_conds(self):
        self.pre = set()
        self.add = set()
        self.de = set()
        return self.pre, self.add, self.de