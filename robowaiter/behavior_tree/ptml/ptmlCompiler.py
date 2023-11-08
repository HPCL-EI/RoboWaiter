import os
import sys
from antlr4 import *

if "." in __name__:
    from .ptmlTranslator import ptmlTranslator
    from .ptmlParser import ptmlParser as Parser
    from .ptmlLexer import ptmlLexer as Lexer

else:
    from ptmlTranslator import ptmlTranslator
    from ptmlParser import ptmlParser as Parser
    from ptmlLexer import ptmlLexer as Lexer


def load(scene, ptml_path: str, behaviour_lib_path: str):
    """_summary_

    Args:
        ptml_path (str): _description_
        behaviour_lib_path (str): _description_

    Raises:
        FileNotFoundError: _description_
        FileNotFoundError: _description_
    """
    # error handle
    if not os.path.exists(ptml_path):
        raise FileNotFoundError("Given a fault ptml path: {}".format(ptml_path))
    if not os.path.exists(behaviour_lib_path):
        raise FileNotFoundError(
            "Given a fault behaviour library path: {}".format(behaviour_lib_path)
        )

    # noting fault, go next
    input_stream = FileStream(ptml_path, encoding="utf-8")

    lexer = Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Parser(stream)
    tree = parser.root()

    walker = ParseTreeWalker()


    sys.path.append(os.path.join(behaviour_lib_path,"cond"))
    sys.path.append(os.path.join(behaviour_lib_path,"act"))

    ptml = ptmlTranslator(scene, behaviour_lib_path)  # listener mode
    walker.walk(ptml, tree)

    return ptml.bt_root
