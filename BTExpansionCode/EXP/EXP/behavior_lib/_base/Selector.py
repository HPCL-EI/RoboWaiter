import py_trees as ptree
from typing import Any

class Selector(ptree.composites.Selector):
    print_name = "Selector"
    ins_name = "Selector"
    type = "Selector"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
