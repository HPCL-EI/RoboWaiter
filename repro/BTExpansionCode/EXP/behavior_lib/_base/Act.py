from EXP.behavior_lib._base.Behavior import Bahavior

class Act(Bahavior):
    print_name_prefix = "act "
    type = 'Act'

    def __init__(self,*args):
        super().__init__(*args)
        self.info = self.get_info(*args)

    @classmethod
    def get_info(self,*arg):
        return None
