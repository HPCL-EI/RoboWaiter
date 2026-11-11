# Generated from ptml.g4 by ANTLR 4.13.1
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
        4,1,18,68,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,4,
        0,14,8,0,11,0,12,0,15,1,0,1,0,1,1,1,1,1,1,1,1,5,1,24,8,1,10,1,12,
        1,27,9,1,1,1,1,1,1,2,1,2,1,2,1,2,3,2,35,8,2,1,3,1,3,3,3,39,8,3,1,
        3,1,3,1,3,3,3,44,8,3,1,3,1,3,1,4,1,4,1,4,1,4,3,4,52,8,4,1,4,1,4,
        1,4,1,4,1,4,3,4,59,8,4,5,4,61,8,4,10,4,12,4,64,9,4,1,5,1,5,1,5,0,
        0,6,0,2,4,6,8,10,0,2,1,0,6,7,1,0,12,13,75,0,13,1,0,0,0,2,19,1,0,
        0,0,4,34,1,0,0,0,6,36,1,0,0,0,8,51,1,0,0,0,10,65,1,0,0,0,12,14,3,
        2,1,0,13,12,1,0,0,0,14,15,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,0,16,
        17,1,0,0,0,17,18,5,0,0,1,18,1,1,0,0,0,19,20,3,4,2,0,20,25,5,1,0,
        0,21,24,3,6,3,0,22,24,3,2,1,0,23,21,1,0,0,0,23,22,1,0,0,0,24,27,
        1,0,0,0,25,23,1,0,0,0,25,26,1,0,0,0,26,28,1,0,0,0,27,25,1,0,0,0,
        28,29,5,2,0,0,29,3,1,0,0,0,30,35,5,3,0,0,31,35,5,4,0,0,32,33,5,5,
        0,0,33,35,5,15,0,0,34,30,1,0,0,0,34,31,1,0,0,0,34,32,1,0,0,0,35,
        5,1,0,0,0,36,38,7,0,0,0,37,39,5,8,0,0,38,37,1,0,0,0,38,39,1,0,0,
        0,39,40,1,0,0,0,40,41,5,14,0,0,41,43,5,9,0,0,42,44,3,8,4,0,43,42,
        1,0,0,0,43,44,1,0,0,0,44,45,1,0,0,0,45,46,5,10,0,0,46,7,1,0,0,0,
        47,52,5,15,0,0,48,52,5,16,0,0,49,52,3,10,5,0,50,52,5,14,0,0,51,47,
        1,0,0,0,51,48,1,0,0,0,51,49,1,0,0,0,51,50,1,0,0,0,52,62,1,0,0,0,
        53,58,5,11,0,0,54,59,5,15,0,0,55,59,5,16,0,0,56,59,3,10,5,0,57,59,
        5,14,0,0,58,54,1,0,0,0,58,55,1,0,0,0,58,56,1,0,0,0,58,57,1,0,0,0,
        59,61,1,0,0,0,60,53,1,0,0,0,61,64,1,0,0,0,62,60,1,0,0,0,62,63,1,
        0,0,0,63,9,1,0,0,0,64,62,1,0,0,0,65,66,7,1,0,0,66,11,1,0,0,0,9,15,
        23,25,34,38,43,51,58,62
    ]

class ptmlParser ( Parser ):

    grammarFileName = "ptml.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'sequence'", "'selector'", 
                     "'parallel'", "'act'", "'cond'", "'Not'", "'('", "')'", 
                     "','", "'True'", "'False'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "String", "Integer", "Float", 
                      "LINE_COMMENT", "WS" ]

    RULE_root = 0
    RULE_tree = 1
    RULE_internal_node = 2
    RULE_action_sign = 3
    RULE_action_parm = 4
    RULE_boolean = 5

    ruleNames =  [ "root", "tree", "internal_node", "action_sign", "action_parm", 
                   "boolean" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    String=14
    Integer=15
    Float=16
    LINE_COMMENT=17
    WS=18

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ptmlParser.EOF, 0)

        def tree(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ptmlParser.TreeContext)
            else:
                return self.getTypedRuleContext(ptmlParser.TreeContext,i)


        def getRuleIndex(self):
            return ptmlParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)




    def root(self):

        localctx = ptmlParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 12
                self.tree()
                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 56) != 0)):
                    break

            self.state = 17
            self.match(ptmlParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TreeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def internal_node(self):
            return self.getTypedRuleContext(ptmlParser.Internal_nodeContext,0)


        def action_sign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ptmlParser.Action_signContext)
            else:
                return self.getTypedRuleContext(ptmlParser.Action_signContext,i)


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
        self.enterRule(localctx, 2, self.RULE_tree)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self.internal_node()
            self.state = 20
            self.match(ptmlParser.T__0)
            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 248) != 0):
                self.state = 23
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [6, 7]:
                    self.state = 21
                    self.action_sign()
                    pass
                elif token in [3, 4, 5]:
                    self.state = 22
                    self.tree()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 28
            self.match(ptmlParser.T__1)
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

        def Integer(self):
            return self.getToken(ptmlParser.Integer, 0)

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
        self.enterRule(localctx, 4, self.RULE_internal_node)
        try:
            self.state = 34
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 30
                self.match(ptmlParser.T__2)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 31
                self.match(ptmlParser.T__3)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 32
                self.match(ptmlParser.T__4)
                self.state = 33
                self.match(ptmlParser.Integer)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Action_signContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def String(self):
            return self.getToken(ptmlParser.String, 0)

        def action_parm(self):
            return self.getTypedRuleContext(ptmlParser.Action_parmContext,0)


        def getRuleIndex(self):
            return ptmlParser.RULE_action_sign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAction_sign" ):
                listener.enterAction_sign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAction_sign" ):
                listener.exitAction_sign(self)




    def action_sign(self):

        localctx = ptmlParser.Action_signContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_action_sign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            _la = self._input.LA(1)
            if not(_la==6 or _la==7):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 38
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 37
                self.match(ptmlParser.T__7)


            self.state = 40
            self.match(ptmlParser.String)
            self.state = 41
            self.match(ptmlParser.T__8)
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 126976) != 0):
                self.state = 42
                self.action_parm()


            self.state = 45
            self.match(ptmlParser.T__9)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Action_parmContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(ptmlParser.Integer)
            else:
                return self.getToken(ptmlParser.Integer, i)

        def Float(self, i:int=None):
            if i is None:
                return self.getTokens(ptmlParser.Float)
            else:
                return self.getToken(ptmlParser.Float, i)

        def boolean(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ptmlParser.BooleanContext)
            else:
                return self.getTypedRuleContext(ptmlParser.BooleanContext,i)


        def String(self, i:int=None):
            if i is None:
                return self.getTokens(ptmlParser.String)
            else:
                return self.getToken(ptmlParser.String, i)

        def getRuleIndex(self):
            return ptmlParser.RULE_action_parm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAction_parm" ):
                listener.enterAction_parm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAction_parm" ):
                listener.exitAction_parm(self)




    def action_parm(self):

        localctx = ptmlParser.Action_parmContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_action_parm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15]:
                self.state = 47
                self.match(ptmlParser.Integer)
                pass
            elif token in [16]:
                self.state = 48
                self.match(ptmlParser.Float)
                pass
            elif token in [12, 13]:
                self.state = 49
                self.boolean()
                pass
            elif token in [14]:
                self.state = 50
                self.match(ptmlParser.String)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11:
                self.state = 53
                self.match(ptmlParser.T__10)
                self.state = 58
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [15]:
                    self.state = 54
                    self.match(ptmlParser.Integer)
                    pass
                elif token in [16]:
                    self.state = 55
                    self.match(ptmlParser.Float)
                    pass
                elif token in [12, 13]:
                    self.state = 56
                    self.boolean()
                    pass
                elif token in [14]:
                    self.state = 57
                    self.match(ptmlParser.String)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 64
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ptmlParser.RULE_boolean

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolean" ):
                listener.enterBoolean(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolean" ):
                listener.exitBoolean(self)




    def boolean(self):

        localctx = ptmlParser.BooleanContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_boolean)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            _la = self._input.LA(1)
            if not(_la==12 or _la==13):
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





