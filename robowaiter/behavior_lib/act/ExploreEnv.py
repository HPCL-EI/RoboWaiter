import py_trees as ptree
from typing import Any
from robowaiter.behavior_lib._base.Act import Act

class ExploreEnv(Act):

    def __init__(self, *args):
        super().__init__(*args)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)
    
    def initialise(self) -> None:
        return super().initialise()
    
    def _update(self) -> ptree.common.Status:
        print('Start checking IsChatting...')
        return ptree.common.Status.SUCCESS
    
    def terminate(self, new_status: ptree.common.Status) -> None:
        return super().terminate(new_status)
    