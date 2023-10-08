import os
import sys
project_path = "/home/wu/RoboWaiter/ptml"
sys.path.append(project_path)

from antlr4 import *
from ptmlListener import ptmlListener
from ptmlParser import ptmlParser
from BT_api import BTAPI

class ptmlTranslator(ptmlListener):
    """Translate the ptml language to BT.

    Args:
        ptmlListener (_type_): _description_
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.stack = []
        self.api = BTAPI()
        
        
    # Enter a parse tree produced by ptmlParser#root.
    def enterRoot(self, ctx:ptmlParser.RootContext):
        pass

    # Exit a parse tree produced by ptmlParser#root.
    def exitRoot(self, ctx:ptmlParser.RootContext):
        pass
        
        
    # Enter a parse tree produced by ptmlParser#tree.
    def enterTree(self, ctx:ptmlParser.TreeContext):
        pass

    # Exit a parse tree produced by ptmlParser#tree.
    def exitTree(self, ctx:ptmlParser.TreeContext):
        pass


    # Enter a parse tree produced by ptmlParser#internal_node.
    def enterInternal_node(self, ctx:ptmlParser.Internal_nodeContext):
        type = str(ctx.children[0])
        print(type)

    # Exit a parse tree produced by ptmlParser#internal_node.
    def exitInternal_node(self, ctx:ptmlParser.Internal_nodeContext):
        pass


    # Enter a parse tree produced by ptmlParser#action_sign.
    def enterAction_sign(self, ctx:ptmlParser.Action_signContext):
        pass

    # Exit a parse tree produced by ptmlParser#action_sign.
    def exitAction_sign(self, ctx:ptmlParser.Action_signContext):
        pass


    # Enter a parse tree produced by ptmlParser#action_parm.
    def enterAction_parm(self, ctx:ptmlParser.Action_parmContext):
        pass

    # Exit a parse tree produced by ptmlParser#action_parm.
    def exitAction_parm(self, ctx:ptmlParser.Action_parmContext):
        pass


    # Enter a parse tree produced by ptmlParser#var_decls.
    def enterVar_decls(self, ctx:ptmlParser.Var_declsContext):
        pass

    # Exit a parse tree produced by ptmlParser#var_decls.
    def exitVar_decls(self, ctx:ptmlParser.Var_declsContext):
        pass


    # Enter a parse tree produced by ptmlParser#var_type.
    def enterVar_type(self, ctx:ptmlParser.Var_typeContext):
        pass

    # Exit a parse tree produced by ptmlParser#var_type.
    def exitVar_type(self, ctx:ptmlParser.Var_typeContext):
        pass


    # Enter a parse tree produced by ptmlParser#boolean.
    def enterBoolean(self, ctx:ptmlParser.BooleanContext):
        pass

    # Exit a parse tree produced by ptmlParser#boolean.
    def exitBoolean(self, ctx:ptmlParser.BooleanContext):
        pass
    
    
class BtNode():
    """
    
    """
    def __init__(self, type:str='BtNode') -> None:
        self.type = type
        self.name:str = ''