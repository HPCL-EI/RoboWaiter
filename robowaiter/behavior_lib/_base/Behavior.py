import py_trees as ptree
from typing import Any
import enum

class Status(enum.Enum):
    """An enumerator representing the status of a behavior."""

    SUCCESS = ptree.common.Status.SUCCESS
    """Behaviour check has passed, or execution of its action has finished with a successful result."""
    FAILURE = ptree.common.Status.FAILURE
    """Behaviour check has failed, or execution of its action finished with a failed result."""
    RUNNING = ptree.common.Status.RUNNING
    """Behaviour is in the middle of executing some action, result still pending."""
    INVALID = ptree.common.Status.INVALID
    """Behaviour is uninitialised and/or in an inactive state, i.e. not currently being ticked."""


# _base Behavior
class Bahavior(ptree.behaviour.Behaviour):
    can_be_expanded = False
    num_params = 0
    valid_params='''
        None
        '''
    scene = None
    print_name_prefix = ""

    def __init__(self,*args):
        name = self.__class__.__name__
        if len(args)>0:
            name = f'{name}({",".join(list(args))})'
        self.name = name
        self.args = args
        super().__init__(self.name)

    def _update(self) -> ptree.common.Status:
        print("this is just a _base behavior node.")
        return Status.INVALID

    @property
    def print_name(self):
        return f'{self.print_name_prefix}{self.name}'

    # let behavior node interact with the scene
    def set_scene(self, scene):
        self.scene = scene

    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)

    def initialise(self) -> None:
        return super().initialise()

    def update(self) -> Status:
        re = self._update()
        print(f"{self.__class__.__name__}: {re.value}")
        return re

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
