# Generated from ./ptml.g4 by ANTLR 4.13.0
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,5,55,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,1,
        0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,
        3,1,3,1,3,1,4,1,4,5,4,51,8,4,10,4,12,4,54,9,4,0,0,5,1,1,3,2,5,3,
        7,4,9,5,1,0,2,3,0,65,90,95,95,97,122,4,0,48,57,65,90,95,95,97,122,
        55,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,1,
        11,1,0,0,0,3,20,1,0,0,0,5,29,1,0,0,0,7,38,1,0,0,0,9,48,1,0,0,0,11,
        12,5,115,0,0,12,13,5,101,0,0,13,14,5,113,0,0,14,15,5,117,0,0,15,
        16,5,101,0,0,16,17,5,110,0,0,17,18,5,99,0,0,18,19,5,101,0,0,19,2,
        1,0,0,0,20,21,5,115,0,0,21,22,5,101,0,0,22,23,5,108,0,0,23,24,5,
        101,0,0,24,25,5,99,0,0,25,26,5,116,0,0,26,27,5,111,0,0,27,28,5,114,
        0,0,28,4,1,0,0,0,29,30,5,112,0,0,30,31,5,97,0,0,31,32,5,114,0,0,
        32,33,5,97,0,0,33,34,5,108,0,0,34,35,5,108,0,0,35,36,5,101,0,0,36,
        37,5,108,0,0,37,6,1,0,0,0,38,39,5,100,0,0,39,40,5,101,0,0,40,41,
        5,99,0,0,41,42,5,111,0,0,42,43,5,114,0,0,43,44,5,97,0,0,44,45,5,
        116,0,0,45,46,5,111,0,0,46,47,5,114,0,0,47,8,1,0,0,0,48,52,7,0,0,
        0,49,51,7,1,0,0,50,49,1,0,0,0,51,54,1,0,0,0,52,50,1,0,0,0,52,53,
        1,0,0,0,53,10,1,0,0,0,54,52,1,0,0,0,2,0,52,0
    ]

class ptmlLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    Names = 5

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'sequence'", "'selector'", "'parallel'", "'decorator'" ]

    symbolicNames = [ "<INVALID>",
            "Names" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "Names" ]

    grammarFileName = "ptml.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


