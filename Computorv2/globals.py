from enum import Enum, auto

user_defined_variables = {}
user_defined_functions = {}

class TokenType(Enum):
    FLOAT = auto()
    INTEGER = auto()
    IDENTIFIER = auto()
    OP_PLUS = auto()
    OP_MINUS = auto()
    OP_MULTIPLY = auto()
    OP_DIVIDE = auto()
    OP_MATRICE_MULTIPLY = auto()
    OP_POWER = auto()
    OP_MODULO = auto()
    LPAREN = auto()
    RPAREN = auto()
    S_LPAREN = auto()
    S_RPAREN = auto()
    OP_COLON = auto()
    OP_SEMICOLON = auto()
    KW_VAR = auto()
    KW_FUNC = auto()
    SIGN_EQUAL = auto()
    SIGN_QMARK = auto()
    IMAGINARY = auto()
    KW_LIST = auto()
    KW_PRINT_HISTORY = auto()
    KW_SIN = auto()
    KW_COS = auto()
    KW_TAN = auto()
    KW_COT = auto()
    KW_SQRT = auto()
    KW_ABS = auto()
    KW_EXP = auto()
    KW_RAD = auto()

token_patterns = [
    (r":history", TokenType.KW_PRINT_HISTORY),
    (r":list", TokenType.KW_LIST),
    (r"cot", TokenType.KW_COT),
    (r"tan", TokenType.KW_TAN),
    (r"cos", TokenType.KW_COS),
    (r"sin", TokenType.KW_SIN),
    (r"sqrt", TokenType.KW_SQRT),
    (r"abs", TokenType.KW_ABS),
    (r"exp", TokenType.KW_EXP),
    (r"rad", TokenType.KW_RAD),
    (r"\*\*", TokenType.OP_MATRICE_MULTIPLY),
    (r"i", TokenType.IMAGINARY),
    (r"var", TokenType.KW_VAR),
    (r"fun", TokenType.KW_FUNC),
    (r"=", TokenType.SIGN_EQUAL),
    (r"\?", TokenType.SIGN_QMARK),
    (r"\d+\.\d*", TokenType.FLOAT),
    (r"\d+", TokenType.INTEGER),
    (r"[a-zA-Z][a-zA-Z]*", TokenType.IDENTIFIER),
    (r"\+", TokenType.OP_PLUS),
    (r"\-", TokenType.OP_MINUS),
    (r"\*", TokenType.OP_MULTIPLY),
    (r"\/", TokenType.OP_DIVIDE),
    (r"\%", TokenType.OP_MODULO),
    (r"\^", TokenType.OP_POWER),
    (r",", TokenType.OP_COLON),
    (r";", TokenType.OP_SEMICOLON),
    (r"\(", TokenType.LPAREN),
    (r"\)", TokenType.RPAREN),
    (r"\[", TokenType.S_LPAREN),
    (r"\]", TokenType.S_RPAREN),
]
