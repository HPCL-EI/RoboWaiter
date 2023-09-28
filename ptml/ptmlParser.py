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
        4,1,20,65,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,1,0,1,0,1,0,1,0,4,0,19,8,0,11,0,12,0,20,1,0,1,0,1,1,1,1,1,1,1,
        1,1,1,3,1,30,8,1,1,2,1,2,1,2,1,2,3,2,36,8,2,1,2,1,2,1,3,1,3,1,3,
        1,3,3,3,44,8,3,1,3,1,3,1,3,1,3,1,3,3,3,51,8,3,5,3,53,8,3,10,3,12,
        3,56,9,3,1,4,1,4,1,4,1,5,1,5,1,6,1,6,1,6,0,0,7,0,2,4,6,8,10,12,0,
        2,1,0,10,13,1,0,14,15,70,0,14,1,0,0,0,2,29,1,0,0,0,4,31,1,0,0,0,
        6,43,1,0,0,0,8,57,1,0,0,0,10,60,1,0,0,0,12,62,1,0,0,0,14,15,3,2,
        1,0,15,18,5,1,0,0,16,19,3,4,2,0,17,19,3,0,0,0,18,16,1,0,0,0,18,17,
        1,0,0,0,19,20,1,0,0,0,20,18,1,0,0,0,20,21,1,0,0,0,21,22,1,0,0,0,
        22,23,5,0,0,1,23,1,1,0,0,0,24,30,5,2,0,0,25,30,5,3,0,0,26,27,5,4,
        0,0,27,30,5,17,0,0,28,30,5,5,0,0,29,24,1,0,0,0,29,25,1,0,0,0,29,
        26,1,0,0,0,29,28,1,0,0,0,30,3,1,0,0,0,31,32,5,6,0,0,32,33,5,16,0,
        0,33,35,5,7,0,0,34,36,3,6,3,0,35,34,1,0,0,0,35,36,1,0,0,0,36,37,
        1,0,0,0,37,38,5,8,0,0,38,5,1,0,0,0,39,44,3,8,4,0,40,44,5,17,0,0,
        41,44,5,18,0,0,42,44,3,12,6,0,43,39,1,0,0,0,43,40,1,0,0,0,43,41,
        1,0,0,0,43,42,1,0,0,0,44,54,1,0,0,0,45,50,5,9,0,0,46,51,3,8,4,0,
        47,51,5,17,0,0,48,51,5,18,0,0,49,51,3,12,6,0,50,46,1,0,0,0,50,47,
        1,0,0,0,50,48,1,0,0,0,50,49,1,0,0,0,51,53,1,0,0,0,52,45,1,0,0,0,
        53,56,1,0,0,0,54,52,1,0,0,0,54,55,1,0,0,0,55,7,1,0,0,0,56,54,1,0,
        0,0,57,58,3,10,5,0,58,59,5,16,0,0,59,9,1,0,0,0,60,61,7,0,0,0,61,
        11,1,0,0,0,62,63,7,1,0,0,63,13,1,0,0,0,7,18,20,29,35,43,50,54
    ]

class ptmlParser ( Parser ):

    grammarFileName = "ptml.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "':'", "'sequence'", "'selector'", "'parallel'", 
                     "'decorator'", "'act'", "'('", "')'", "','", "'int'", 
                     "'float'", "'bool'", "'string'", "'True'", "'False'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "Names", "Integer", "Float", "LINE_COMMENT", "WS" ]

    RULE_tree = 0
    RULE_internal_node = 1
    RULE_action_sign = 2
    RULE_action_parm = 3
    RULE_var_decls = 4
    RULE_var_type = 5
    RULE_boolean = 6

    ruleNames =  [ "tree", "internal_node", "action_sign", "action_parm", 
                   "var_decls", "var_type", "boolean" ]

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
    T__13=14
    T__14=15
    Names=16
    Integer=17
    Float=18
    LINE_COMMENT=19
    WS=20

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


        def EOF(self):
            return self.getToken(ptmlParser.EOF, 0)

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
        self.enterRule(localctx, 0, self.RULE_tree)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.internal_node()
            self.state = 15
            self.match(ptmlParser.T__0)
            self.state = 18 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 18
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [6]:
                    self.state = 16
                    self.action_sign()
                    pass
                elif token in [2, 3, 4, 5]:
                    self.state = 17
                    self.tree()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 20 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 124) != 0)):
                    break

            self.state = 22
            self.match(ptmlParser.EOF)
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
        self.enterRule(localctx, 2, self.RULE_internal_node)
        try:
            self.state = 29
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 24
                self.match(ptmlParser.T__1)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 25
                self.match(ptmlParser.T__2)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 26
                self.match(ptmlParser.T__3)
                self.state = 27
                self.match(ptmlParser.Integer)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 4)
                self.state = 28
                self.match(ptmlParser.T__4)
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

        def Names(self):
            return self.getToken(ptmlParser.Names, 0)

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
        self.enterRule(localctx, 4, self.RULE_action_sign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self.match(ptmlParser.T__5)
            self.state = 32
            self.match(ptmlParser.Names)
            self.state = 33
            self.match(ptmlParser.T__6)
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 457728) != 0):
                self.state = 34
                self.action_parm()


            self.state = 37
            self.match(ptmlParser.T__7)
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

        def var_decls(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ptmlParser.Var_declsContext)
            else:
                return self.getTypedRuleContext(ptmlParser.Var_declsContext,i)


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
        self.enterRule(localctx, 6, self.RULE_action_parm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10, 11, 12, 13]:
                self.state = 39
                self.var_decls()
                pass
            elif token in [17]:
                self.state = 40
                self.match(ptmlParser.Integer)
                pass
            elif token in [18]:
                self.state = 41
                self.match(ptmlParser.Float)
                pass
            elif token in [14, 15]:
                self.state = 42
                self.boolean()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 54
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==9:
                self.state = 45
                self.match(ptmlParser.T__8)
                self.state = 50
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [10, 11, 12, 13]:
                    self.state = 46
                    self.var_decls()
                    pass
                elif token in [17]:
                    self.state = 47
                    self.match(ptmlParser.Integer)
                    pass
                elif token in [18]:
                    self.state = 48
                    self.match(ptmlParser.Float)
                    pass
                elif token in [14, 15]:
                    self.state = 49
                    self.boolean()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 56
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Var_declsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var_type(self):
            return self.getTypedRuleContext(ptmlParser.Var_typeContext,0)


        def Names(self):
            return self.getToken(ptmlParser.Names, 0)

        def getRuleIndex(self):
            return ptmlParser.RULE_var_decls

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar_decls" ):
                listener.enterVar_decls(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar_decls" ):
                listener.exitVar_decls(self)




    def var_decls(self):

        localctx = ptmlParser.Var_declsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_var_decls)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.var_type()
            self.state = 58
            self.match(ptmlParser.Names)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Var_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ptmlParser.RULE_var_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar_type" ):
                listener.enterVar_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar_type" ):
                listener.exitVar_type(self)




    def var_type(self):

        localctx = ptmlParser.Var_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_var_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 15360) != 0)):
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
        self.enterRule(localctx, 12, self.RULE_boolean)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            _la = self._input.LA(1)
            if not(_la==14 or _la==15):
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





