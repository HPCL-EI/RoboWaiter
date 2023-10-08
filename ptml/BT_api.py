import py_trees as bt
import typing

class BTAPI():
    """
    
    """
    
    def __init__(self) -> None:
        self.string = None
    
    
    def newTree(self) -> bt.trees.BehaviourTree:
        """_summary_

        Returns:
            bt.trees.BehaviourTree: _description_
        """
        
    def newSequenceNode(self, tag: str='') -> None:
        """_summary_

        Args:
            tag (str, optional): _description_. Defaults to ''.
        """
        return
    
    def newSelectorNode(self, tag: str='') -> None:
        """_summary_

        Args:
            tag (str, optional): _description_. Defaults to ''.
        """
        return
    
    def newParallelNode(self, threshold:int) -> None:
        """_summary_

        Args:
            threshold (int): _description_
        """
        return
    
    def newDecoratorNode(self, tag: str='') -> None:
        """_summary_

        Args:
            tag (str, optional): _description_. Defaults to ''.
        """
        return
    
    def newBehaviourNode(self, name: str, args: typing.Optional[typing.List[str]]=[], tag:str='', isCond:bool=False) -> None:
        """_summary_

        Args:
            name (str): _description_
            args (typing.Optional[typing.List[str]], optional): _description_. Defaults to [].
            tag (str, optional): _description_. Defaults to ''.
            isCond (bool, optional): _description_. Defaults to False.
        """
        return
    
    def attach_to_parent(self, uuid_child:str, uuid_parent:str) -> None:
        """_summary_

        Args:
            uuid_child (str): _description_
            uuid_parent (str): _description_
        """
        return