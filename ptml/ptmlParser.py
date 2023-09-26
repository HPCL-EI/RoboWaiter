# Generated from ./ptml.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,5,14,2,0,7,0,2,1,7,1,1,0,1,0,1,0,4,0,8,8,0,11,0,12,0,9,1,1,1,
        1,1,1,0,0,2,0,2,0,1,1,0,1,4,13,0,4,1,0,0,0,2,11,1,0,0,0,4,7,3,2,
        1,0,5,8,5,5,0,0,6,8,3,0,0,0,7,5,1,0,0,0,7,6,1,0,0,0,8,9,1,0,0,0,
        9,7,1,0,0,0,9,10,1,0,0,0,10,1,1,0,0,0,11,12,7,0,0,0,12,3,1,0,0,0,
        2,7,9
    ]

class ptmlParser ( Parser ):

    grammarFileName = "ptml.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'sequence'", "'selector'", "'parallel'", 
                     "'decorator'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "Names" ]

    RULE_tree = 0
    RULE_internal_node = 1

    ruleNames =  [ "tree", "internal_node" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    Names=5

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TreeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def internal_node(self):
            return self.getTypedRuleContext(ptmlParser.Internal_nodeContext,0)


        def Names(self, i:int=None):
            if i is None:
                return self.getTokens(ptmlParser.Names)
            else:
                return self.getToken(ptmlParser.Names, i)

        def tree(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ptmlParser.TreeContext)
            else:
                return self.getTypedRuleContext(ptmlParser.TreeContext,i)


        def getRuleIndex(self):
            return ptmlParser.RULE_tree

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTree" ):
                listener.enterTree(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTree" ):
                listener.exitTree(self)




    def tree(self):

        localctx = ptmlParser.TreeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_tree)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 4
            self.internal_node()
            self.state = 7 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 7
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [5]:
                        self.state = 5
                        self.match(ptmlParser.Names)
                        pass
                    elif token in [1, 2, 3, 4]:
                        self.state = 6
                        self.tree()
                        pass
                    else:
                        raise NoViableAltException(self)


                else:
                    raise NoViableAltException(self)
                self.state = 9 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Internal_nodeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ptmlParser.RULE_internal_node

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInternal_node" ):
                listener.enterInternal_node(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInternal_node" ):
                listener.exitInternal_node(self)




    def internal_node(self):

        localctx = ptmlParser.Internal_nodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_internal_node)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





