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
        4,1,21,72,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,4,0,18,8,0,11,0,12,0,19,1,0,1,0,1,1,1,1,1,1,1,1,4,
        1,28,8,1,11,1,12,1,29,1,2,1,2,1,2,1,2,1,2,3,2,37,8,2,1,3,1,3,1,3,
        1,3,3,3,43,8,3,1,3,1,3,1,4,1,4,1,4,1,4,3,4,51,8,4,1,4,1,4,1,4,1,
        4,1,4,3,4,58,8,4,5,4,60,8,4,10,4,12,4,63,9,4,1,5,1,5,1,5,1,6,1,6,
        1,7,1,7,1,7,0,0,8,0,2,4,6,8,10,12,14,0,3,1,0,6,7,1,0,11,14,1,0,15,
        16,77,0,17,1,0,0,0,2,23,1,0,0,0,4,36,1,0,0,0,6,38,1,0,0,0,8,50,1,
        0,0,0,10,64,1,0,0,0,12,67,1,0,0,0,14,69,1,0,0,0,16,18,3,2,1,0,17,
        16,1,0,0,0,18,19,1,0,0,0,19,17,1,0,0,0,19,20,1,0,0,0,20,21,1,0,0,
        0,21,22,5,0,0,1,22,1,1,0,0,0,23,24,3,4,2,0,24,27,5,1,0,0,25,28,3,
        6,3,0,26,28,3,2,1,0,27,25,1,0,0,0,27,26,1,0,0,0,28,29,1,0,0,0,29,
        27,1,0,0,0,29,30,1,0,0,0,30,3,1,0,0,0,31,37,5,2,0,0,32,37,5,3,0,
        0,33,34,5,4,0,0,34,37,5,18,0,0,35,37,5,5,0,0,36,31,1,0,0,0,36,32,
        1,0,0,0,36,33,1,0,0,0,36,35,1,0,0,0,37,5,1,0,0,0,38,39,7,0,0,0,39,
        40,5,17,0,0,40,42,5,8,0,0,41,43,3,8,4,0,42,41,1,0,0,0,42,43,1,0,
        0,0,43,44,1,0,0,0,44,45,5,9,0,0,45,7,1,0,0,0,46,51,3,10,5,0,47,51,
        5,18,0,0,48,51,5,19,0,0,49,51,3,14,7,0,50,46,1,0,0,0,50,47,1,0,0,
        0,50,48,1,0,0,0,50,49,1,0,0,0,51,61,1,0,0,0,52,57,5,10,0,0,53,58,
        3,10,5,0,54,58,5,18,0,0,55,58,5,19,0,0,56,58,3,14,7,0,57,53,1,0,
        0,0,57,54,1,0,0,0,57,55,1,0,0,0,57,56,1,0,0,0,58,60,1,0,0,0,59,52,
        1,0,0,0,60,63,1,0,0,0,61,59,1,0,0,0,61,62,1,0,0,0,62,9,1,0,0,0,63,
        61,1,0,0,0,64,65,3,12,6,0,65,66,5,17,0,0,66,11,1,0,0,0,67,68,7,1,
        0,0,68,13,1,0,0,0,69,70,7,2,0,0,70,15,1,0,0,0,8,19,27,29,36,42,50,
        57,61
    ]

class ptmlParser ( Parser ):

    grammarFileName = "ptml.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "':'", "'sequence'", "'selector'", "'parallel'", 
                     "'decorator'", "'task'", "'cond'", "'('", "')'", "','", 
                     "'int'", "'float'", "'bool'", "'string'", "'True'", 
                     "'False'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "Names", "Integer", "Float", "LINE_COMMENT", 
                      "WS" ]

    RULE_root = 0
    RULE_tree = 1
    RULE_internal_node = 2
    RULE_action_sign = 3
    RULE_action_parm = 4
    RULE_var_decls = 5
    RULE_var_type = 6
    RULE_boolean = 7

    ruleNames =  [ "root", "tree", "internal_node", "action_sign", "action_parm", 
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
    T__15=16
    Names=17
    Integer=18
    Float=19
    LINE_COMMENT=20
    WS=21

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
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
            self.state = 17 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 16
                self.tree()
                self.state = 19 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 60) != 0)):
                    break

            self.state = 21
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
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.internal_node()
            self.state = 24
            self.match(ptmlParser.T__0)
            self.state = 27 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 27
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [6, 7]:
                        self.state = 25
                        self.action_sign()
                        pass
                    elif token in [2, 3, 4, 5]:
                        self.state = 26
                        self.tree()
                        pass
                    else:
                        raise NoViableAltException(self)


                else:
                    raise NoViableAltException(self)
                self.state = 29 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

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
            self.state = 36
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 31
                self.match(ptmlParser.T__1)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 32
                self.match(ptmlParser.T__2)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 33
                self.match(ptmlParser.T__3)
                self.state = 34
                self.match(ptmlParser.Integer)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 4)
                self.state = 35
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
        self.enterRule(localctx, 6, self.RULE_action_sign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            _la = self._input.LA(1)
            if not(_la==6 or _la==7):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 39
            self.match(ptmlParser.Names)
            self.state = 40
            self.match(ptmlParser.T__7)
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 915456) != 0):
                self.state = 41
                self.action_parm()


            self.state = 44
            self.match(ptmlParser.T__8)
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
        self.enterRule(localctx, 8, self.RULE_action_parm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 13, 14]:
                self.state = 46
                self.var_decls()
                pass
            elif token in [18]:
                self.state = 47
                self.match(ptmlParser.Integer)
                pass
            elif token in [19]:
                self.state = 48
                self.match(ptmlParser.Float)
                pass
            elif token in [15, 16]:
                self.state = 49
                self.boolean()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 52
                self.match(ptmlParser.T__9)
                self.state = 57
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [11, 12, 13, 14]:
                    self.state = 53
                    self.var_decls()
                    pass
                elif token in [18]:
                    self.state = 54
                    self.match(ptmlParser.Integer)
                    pass
                elif token in [19]:
                    self.state = 55
                    self.match(ptmlParser.Float)
                    pass
                elif token in [15, 16]:
                    self.state = 56
                    self.boolean()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 63
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
        self.enterRule(localctx, 10, self.RULE_var_decls)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.var_type()
            self.state = 65
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
        self.enterRule(localctx, 12, self.RULE_var_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 30720) != 0)):
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
        self.enterRule(localctx, 14, self.RULE_boolean)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
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





