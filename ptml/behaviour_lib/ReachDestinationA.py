import py_trees as ptree
from typing import Any

class ReachDestinationA(ptree.behaviour.Behaviour):

    def __init__(self, name: str, scene):
        super().__init__(name)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)
    
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> ptree.common.Status:
        print('Start checking IsChatting...')
        return ptree.common.Status.SUCCESS
    
    def terminate(self, new_status: ptree.common.Status) -> None:
        return super().terminate(new_status)
    