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
    ptml_path = format_trans_to_bracket(ptml_path)
    # print(ptml_path)
    input_stream = FileStream(ptml_path, encoding="utf-8")

    lexer = Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Parser(stream)
    tree = parser.root()

    walker = ParseTreeWalker()

    sys.path.append(os.path.join(behaviour_lib_path, "cond"))
    sys.path.append(os.path.join(behaviour_lib_path, "act"))

    ptml = ptmlTranslator(scene, behaviour_lib_path)  # listener mode
    walker.walk(ptml, tree)

    return ptml.bt_root


def format_trans_to_bracket(file_path: str) -> str:
    """_summary_

    Args:
        file_path (str): _description_

    Raises:
        FileNotFoundError: _description_

    Returns:
        str: the path tp temp file with '{}' form.
    """
    import autopep8

    if not os.path.exists(file_path):
        raise FileNotFoundError("Given a fault ptml path: {}".format(file_path))

    with open(file_path, 'r') as file:
        f = file.read()
        if "{" in f:
            return file_path

    def counter_(input: str) -> int:
        length = 0
        for i in range(len(input)):
            if input[i] == ' ':
                length += 1
            else:
                if length % 4 != 0:
                    raise TabError('Tab length in ptml file should be 4.')
                return length

    with open(file_path, 'r') as file:
        ptml_new = ''
        ptml_tab = file.readlines()

        level = 0
        for i in ptml_tab:

            if i.startswith('//'):
                continue

            new_level = counter_(i) // 4
            if new_level == level:
                ptml_new += i
            elif new_level > level:
                ptml_new += '{\n' + i
                level += 1
            elif new_level < level:
                ptml_new += '\n}' + i
                level -= 1
        for i in range(level):
            ptml_new += '}'

    file_name = os.path.basename(file_path).split(".")[0]
    dir_path = os.path.dirname(file_path)
    # import re
    # new_path = re.sub('\\\[a-zA-Z0-9_]*\.ptml', '/bracket_ptml.ptml', file_path)
    new_path = os.path.join(dir_path,file_name+"_bracket.ptml")
    with open(new_path, 'w') as file:
        file.write(ptml_new)
    return new_path

# format_trans_to_bracket('C:\\Users\\Estrella\\Desktop\\RoboWaiter\\robowaiter\\behavior_tree\\ptml\\test\\Default.ptml')