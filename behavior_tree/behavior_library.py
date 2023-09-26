"""
    顶层行为树中的动作与条件节点
"""

from typing import *
import py_trees
from py_trees import common
from py_trees.common import Status


##############################################################
#                       条件节点 
##############################################################

class IsChatting(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super().__init__(name)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)
    
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> Status:
        print('Start checking IsChatting...')
        return True
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
    

class IsTakingAction(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super().__init__(name)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)
    
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> Status:
        print('Start checking IsTakingAction...')
        return True
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
    

class IsSomethingMore(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super().__init__(name)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)
    
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> Status:
        print('Start checking IsSomethingMore...')
        return True
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
    

##############################################################
#                       动作节点 
##############################################################

class Chatting(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super().__init__(name)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)
    
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> Status:
        print('Start executing Chatting...')
        return True
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
    

class TakingAction(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super().__init__(name)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)
    
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> Status:
        print('Start executing TakingAction...')
        return True
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
    

class TakingMoreAction(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super().__init__(name)

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)
    
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> Status:
        print('Start executing TakingMoreAction...')
        return True
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)