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
        4,1,5,25,2,0,7,0,2,1,7,1,1,0,1,0,4,0,7,8,0,11,0,12,0,8,1,0,4,0,12,
        8,0,11,0,12,0,13,1,0,4,0,17,8,0,11,0,12,0,18,3,0,21,8,0,1,1,1,1,
        1,1,0,0,2,0,2,0,1,1,0,1,4,26,0,20,1,0,0,0,2,22,1,0,0,0,4,6,3,2,1,
        0,5,7,5,5,0,0,6,5,1,0,0,0,7,8,1,0,0,0,8,6,1,0,0,0,8,9,1,0,0,0,9,
        21,1,0,0,0,10,12,3,2,1,0,11,10,1,0,0,0,12,13,1,0,0,0,13,11,1,0,0,
        0,13,14,1,0,0,0,14,16,1,0,0,0,15,17,5,5,0,0,16,15,1,0,0,0,17,18,
        1,0,0,0,18,16,1,0,0,0,18,19,1,0,0,0,19,21,1,0,0,0,20,4,1,0,0,0,20,
        11,1,0,0,0,21,1,1,0,0,0,22,23,7,0,0,0,23,3,1,0,0,0,4,8,13,18,20
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

        def internal_node(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ptmlParser.Internal_nodeContext)
            else:
                return self.getTypedRuleContext(ptmlParser.Internal_nodeContext,i)


        def Names(self, i:int=None):
            if i is None:
                return self.getTokens(ptmlParser.Names)
            else:
                return self.getToken(ptmlParser.Names, i)

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
        self._la = 0 # Token type
        try:
            self.state = 20
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 4
                self.internal_node()
                self.state = 6 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 5
                    self.match(ptmlParser.Names)
                    self.state = 8 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==5):
                        break

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 11 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 10
                    self.internal_node()
                    self.state = 13 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0)):
                        break

                self.state = 16 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 15
                    self.match(ptmlParser.Names)
                    self.state = 18 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==5):
                        break

                pass


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
            self.state = 22
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





