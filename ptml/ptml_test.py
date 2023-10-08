import os
import sys
project_path = "/home/wu/RoboWaiter/ptml"
sys.path.append(project_path)

from antlr4 import *
from ptmlTranslator import ptmlTranslator
from ptmlParser import ptmlParser as Parser
from ptmlLexer import ptmlLexer as Lexer


if __name__ == '__main__':
    
    text_path = os.path.join(project_path, 'CoffeeDelivery.ptml')
    input_stream = FileStream(text_path, encoding='utf-8')
    
    # testing lexer & parser
    lexer = Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Parser(stream)
    tree = parser.root()
    
    walker = ParseTreeWalker()
    ptml = ptmlTranslator() # listener mode
    walker.walk(ptml, tree)