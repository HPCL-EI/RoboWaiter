from antlr4 import *
from .ptmlListener import ptmlListener
from .ptmlParser import ptmlParser

class ptmlTranslator(ptmlListener):
    """Translate the ptml language to BT.

    Args:
        ptmlListener (_type_): _description_
    """
    
    def __init__(self) -> None:
        super().__init__()
        
        
    # Enter a parse tree produced by ptmlParser#tree.
    def enterTree(self, ctx:ptmlParser.TreeContext):
        pass

    # Exit a parse tree produced by ptmlParser#tree.
    def exitTree(self, ctx:ptmlParser.TreeContext):
        pass


    # Enter a parse tree produced by ptmlParser#internal_node.
    def enterInternal_node(self, ctx:ptmlParser.Internal_nodeContext):
        pass

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