import os
import sys
import uuid

project_path = "/home/wu/RoboWaiter/ptml"
sys.path.append(project_path)

from antlr4 import *
from ptmlListener import ptmlListener
from ptmlParser import ptmlParser
from ptml.ptmlTranslateAPI import PyTreesAPI

class ptmlTranslator(ptmlListener):
    """Translate the ptml language to BT.

    Args:
        ptmlListener (_type_): _description_
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.stack = []
        self.api = PyTreesAPI()
        
        
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
        
        tag = str(uuid.uuid4())
        self.stack.append(tag)
        
        type = str(ctx.children[0])
        if type == 'sequence':
            self.api.newSequenceNode(tag)
        elif type == 'selector':
            self.api.newSelectorNode(tag)
        elif type == 'parallel':
            self.api.newParallelNode(tag, threshold=int(ctx.children[1]))
        elif type == 'decorator':
            self.api.newDecoratorNode(tag)

    # Exit a parse tree produced by ptmlParser#internal_node.
    def exitInternal_node(self, ctx:ptmlParser.Internal_nodeContext):
        pass


    # Enter a parse tree produced by ptmlParser#action_sign.
    def enterAction_sign(self, ctx:ptmlParser.Action_signContext):
        # cond / task
        type = str(ctx.children[0])
        name = str(ctx.Names())
        
        if len(ctx.children) > 4:
            # have params
            args = ctx.action_parm()
            print(args.Float())
        
        if type == 'cond':
            self.api.newBehaviourNode(name, isCond=True)
        else:
            self.api.newBehaviourNode(name, isCond=False)
        
    

    # Exit a parse tree produced by ptmlParser#action_sign.
    def exitAction_sign(self, ctx:ptmlParser.Action_signContext):
        pass


    # Enter a parse tree produced by ptmlParser#action_parm.
    def enterAction_parm(self, ctx:ptmlParser.Action_parmContext):
        pass

    # Exit a parse tree produced by ptmlParser#action_parm.
    def exitAction_parm(self, ctx:ptmlParser.Action_parmContext):
        pass


    # Enter a parse tree produced by ptmlParser#boolean.
    def enterBoolean(self, ctx:ptmlParser.BooleanContext):
        pass

    # Exit a parse tree produced by ptmlParser#boolean.
    def exitBoolean(self, ctx:ptmlParser.BooleanContext):
        pass
    