import py_trees as ptree
from typing import Any

class Sequence(ptree.composites.Sequence):
    print_name = "Sequence"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

