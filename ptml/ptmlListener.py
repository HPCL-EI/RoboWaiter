# Generated from ./ptml.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .ptmlParser import ptmlParser
else:
    from ptmlParser import ptmlParser

# This class defines a complete listener for a parse tree produced by ptmlParser.
class ptmlListener(ParseTreeListener):

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



del ptmlParser