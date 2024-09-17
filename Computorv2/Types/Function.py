from inspect import signature
from typing import Callable, Any, List
import re
import copy

from .AType import AType

class Function(AType):
    def __init__(self, fn: Callable[..., Any], name: str = "anonymouse") -> None:
        self.name = name
        self.vars = list(signature(fn).parameters)
        self.expr = "[built-in]"
        self.fn = fn
        self.varnum = len(signature(fn).parameters)

    def __call__(self, *args, **kwds):
        return self.fn(*args, **kwds)

    def __str__(self) -> str:
        return f"{self.name}({','.join(self.vars)})={self.expr}"

class FunctionList(Function):
    pattern = r"fun[a-zA-Z]+\(.+\)"

    def __init__(self, expr: str, vars: List[str],  name: str = "anonymouse") -> None:
        from ..executor import infix_to_postfix
        self.name = name
        self.expr = expr
        self.vars = vars
        self.varnum = len(vars)
        rpn_list = infix_to_postfix(expr)
        for i in range(len(rpn_list)):
            if (rpn_list[i] in vars):
                rpn_list[i] = str(vars.index(rpn_list[i]))
        self.rpn_list = rpn_list

    def __call__(self, *args, **kwds):
        from ..executor import evalute_postfix
        res = copy.deepcopy(self.rpn_list)
        for i in range(len(self.rpn_list)):
            if isinstance(res[i], str) and res[i].isdigit():
                res[i] = args[int(res[i])]
        return evalute_postfix(res)
    
    def __str__(self) -> str:
        result = self.subvars()
        return f"{self.name}({','.join(self.vars)}) = {result}"

    def subvars(self):
        from ..globals import user_defined_variables
        def f(m: re.Match):
            word = m.group().lower()
            if word in user_defined_variables and not isinstance(user_defined_variables[word], Function):
                return(str(user_defined_variables[word]))
            else:
                return(m.group())
        result = re.sub(r"[a-zA-Z]+", f, self.expr)
        result = re.sub(r"([+\-*%/])", r" \1 ", result)
        return result.strip()