from enum import Enum, auto
from .Types import Function
from . import my_math
from .my_print import _print

class EvaluationDirection(Enum):
    LEFT_TO_RIGHT = auto()
    RIGHT_TO_LEFT = auto()
    NONE = auto()

builtin_functions = {

    "abs": Function(my_math._abs, "abs"),
    "pow": Function(my_math._pow, "pow"),
    "max": Function(my_math._max, "max"),
    "min": Function(my_math._min, "min"),
    "delta": Function(my_math._delta, "delta"),  
    "sqrt": Function(my_math.ft_sqrt, "sqrt"),
}

user_defined_variables = {}

command_list = [
    {
        "name": "exit",
        "needs_params": False,
        "function": exit,
    },
    {
        "name": "clear",
        "needs_params": False,
        "function": lambda: print("\033[H\033[J"),  # Lambda kullanarak fonksiyon çağrısını sarmalayın
    },
    {
        "name": "print",
        "needs_params": True,
        "function": _print,
    }
]

computorv_commands = {
    "user_defined_variables": lambda: print({key: str(val) for key, val in user_defined_variables.items()}),
    "builtin_functions": lambda: print([str(v) for v in builtin_functions.values()])
}


operators = {
    "(": {
        "precedence": -1,
        "eval_dir": EvaluationDirection.NONE,
    },
    ")": {
        "precedence": -1,
        "eval_dir": EvaluationDirection.NONE,
    },
    ",": {
        "precedence": -1,
        "eval_dir": EvaluationDirection.NONE,
    },
    "^": {
        "precedence": 4,
        "eval_dir": EvaluationDirection.RIGHT_TO_LEFT,
        "function": lambda a, b: a ** b,
    },
    ".": {
        "precedence": 2,
        "eval_dir": EvaluationDirection.LEFT_TO_RIGHT,
        "function": lambda a, b: a * b
    },
    "*": {
        "precedence": 3,
        "eval_dir": EvaluationDirection.LEFT_TO_RIGHT,
        "function": lambda a, b: a * b
    },
    "/": {
        "precedence": 3,
        "eval_dir": EvaluationDirection.LEFT_TO_RIGHT,
        "function": lambda a, b: a / b
    },
    "%": {
        "precedence": 3,
        "eval_dir": EvaluationDirection.LEFT_TO_RIGHT,
        "function": lambda a, b: a % b
    },
    "+": {
        "precedence": 1,
        "eval_dir": EvaluationDirection.LEFT_TO_RIGHT,
        "function": lambda a, b: a + b
    },
    "-": {
        "precedence": 1,
        "eval_dir": EvaluationDirection.LEFT_TO_RIGHT,
        "function": lambda a, b: a - b
    },
}