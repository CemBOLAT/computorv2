
from .exceptions import ComputerV2Exception
from .globals import user_defined_functions, user_defined_variables
from .lexer import Lexer
import re

def parser(line:str) -> list:
    """
    Parser function for the Computorv2 project.
    """

    line = line.replace(" ", "")
    line = line.lower()

    lexer = Lexer(line)
    if not lexer.tokens:
        raise ComputerV2Exception("No tokens found.")
    lexer.is_valid()
    return lexer.tokens
    
    