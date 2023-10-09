import os
import typing
import shortuuid

short_uuid = lambda : shortuuid.ShortUUID().random(length=8)

class PyTreesAPI():
    """
    
    """
    
    def __init__(self) -> None:
        self.pystr = ''
        self.prepare()
        
        
    def prepare(self) -> None:
        # import libraries
        self.pystr += 'import py_trees as tree\n'
        
        self.pystr += '\n' * 2
        
    def write_to_file(self, dir: str = './', filename: str = 'auto_generate.py') -> None:
        """_summary_

        Args:
            dir (str, optional): _description_. Defaults to './'.
            filename (str, optional): _description_. Defaults to 'auto_generate.py'.

        Raises:
            FileNotFoundError: _description_
        """
        # exceptions handling
        filepath = os.path.join(dir, filename)
        if not os.path.exists(dir):
            raise FileNotFoundError(
                ''
            )
        # if os.path.exists(filepath):
        #     raise FileExistsError(
        #         ''
        #     )
        
        with open(filepath, 'w') as file:
            file.write(self.pystr)
            
    def run() -> None:
        """_summary_
        """
        
    
    def newTree(self) -> None:
        """_summary_
        """
        
    def newSequenceNode(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        tag = 'sequence_' + short_uuid()
        return tag
    
    def newSelectorNode(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        tag = 'selector_' + short_uuid()
        return tag
    
    def newParallelNode(self, threshold:int) -> str:
        """_summary_

        Args:
            threshold (int): _description_

        Returns:
            str: _description_
        """
        tag = 'parallel_' + short_uuid()
        return tag
    
    def newDecoratorNode(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        tag = 'decorator_' + short_uuid()
        return tag
    
    def newBehaviourNode(self, 
                         name: str, 
                         args: typing.Optional[typing.List[str]] = [], 
                         isCond: bool = False
                        ) -> str:
        """_summary_

        Args:
            name (str): _description_
            args (typing.Optional[typing.List[str]], optional): _description_. Defaults to [].
            isCond (bool, optional): _description_. Defaults to False.

        Returns:
            str: _description_
        """
        tag = 'behavior_' + short_uuid()
        return tag
    
    def connect_to_parent(self, uuid_child:str, uuid_parent:str) -> None:
        """_summary_

        Args:
            uuid_child  (str): _description_
            uuid_parent (str): _description_
        """
        return