import re
from collections import deque

from .Types.Complex import Imaginary, Real, Complex
from .Types.Function import Function
from .Types.Function import FunctionList
from .Types.AType import AType
from .Types.Polynomial import Polynomial
from .Types.Polynomial_degree1 import Polynomial_degree1
from .Types.Polynomial_degree2 import Polynomial_degree2

from .exceptions import ComputerV2Exception

def negative_sign_handler(expression: str) -> str:
    from .globals import operators
    ops = ""
    for op in operators:
        if operators[op]["precedence"] > 0:
            ops += "\\" + op
    
    return re.sub(f"([{ops}])-({Imaginary.pattern}|{Real.pattern}|{FunctionList.pattern}|[a-zA-Z]+)", r"\1(0-\2)", expression)
        

def parantheses_check(expression: str) -> bool:
    left_p, right_p = "{[(", "}])"
    sta = deque()

    for el in expression:
        if el in left_p:
            sta.append(el)
        elif el in right_p:
            if not sta:
                return False
            if right_p.index(el) != left_p.index(sta.pop()):
                return False
    if sta:
        return False
    return True

def preprocess_expression(expression: str) -> str:
    expression = re.sub(r"\s+", "", expression)

    if (not parantheses_check(expression)):
        raise ComputerV2Exception("Parantheses are not balanced")
    expression = re.sub(r"\*\*", ".", expression) # replace ** with . for power operator
    expression = negative_sign_handler(expression)
    return expression.lower()

def infix_to_postfix(expression: str) -> list:
    from .Types.Matrix import Matrix
    from .globals import operators, user_defined_variables, builtin_functions, EvaluationDirection
    variable_type = [Imaginary, Real, Matrix]
    variable_patterns = [var.pattern for var in variable_type] # [Imaginary.pattern, Real.pattern, Complex.pattern]
    operator_patterns = ["\\" + e for e in operators]
    all_variables = {**user_defined_variables, **builtin_functions}
    
    all_patterns = variable_patterns + operator_patterns + [r"[a-zA-Z]+"]
    expression = preprocess_expression(expression)

    tokens = re.findall("|".join(all_patterns), expression)
    classed_tokens = []
    variable_patterns_list = list(enumerate(re.compile(p) for p in variable_patterns))

    #types_regex = list(enumerate(re.compile(p) for p in types_patterns))
    for token in tokens:
        for i, pattern in variable_patterns_list:
            if pattern.fullmatch(token):
                classed_tokens.append(variable_type[i](token))
                break
        else:
            classed_tokens.append(token) # if no match is found, we append the token as is (a string)

    for i, token in enumerate(classed_tokens):
        if (isinstance(token, str)) and (token in all_variables):
            classed_tokens[i] = all_variables[token]

    _list = []

    stack = deque()
    for token in classed_tokens:
        if token in operators:
        
            if (token == ","):
                while (len(stack) > 0):
                    op = stack[-1]
                    if (op == '(' or op == ","):
                        break
                    list.append(stack.pop())
        
            elif (token == "("):
                stack.append(token)
            
            elif (token == ")"):
                while (len(stack) > 0):
                    op = stack.pop()
                    if (op == "("):
                        break
                    _list.append(op)
                else:
                    raise ComputerV2Exception("Parantheses are not balanced unmatched )")
            else:
                while(len(stack) > 0):
                    last = stack[-1]
                    if (isinstance(last, Function)):
                        _list.append(stack.pop())
                    else:
                        last = operators[last]
                        if (last["precedence"] > operators[token]["precedence"]):
                            _list.append(stack.pop())
                        elif (last["precedence"] == operators[token]["precedence"] and operators[token]["eval_dir"] == EvaluationDirection.LEFT_TO_RIGHT):
                            _list.append(stack.pop())
                        else:
                            break
                stack.append(token)
        elif (isinstance(token, Function)):
            stack.append(token)
        elif (isinstance(token, AType) or isinstance(token, str)):
            _list.append(token)
    
    while (len(stack) > 0):
        _list.append(stack.pop())
    return _list


def evalute_postfix(expression: list):
    from .globals import operators
    result = deque()
    if not expression:
        raise ComputerV2Exception("Empty expression")
    
    for token in expression:
        if (token in operators):
            right = result.pop()
            if (len(result) == 0): # if we are at the end of the expression
                if (token == "+" or token == "-"):
                    left = Complex(0, 0)
                else:
                   raise ComputerV2Exception(f"Invalid number of arguments for operator {token}")
            else:
                left = result.pop()

            try:
                result.append(operators[token]["function"](left, right))
            except ZeroDivisionError:
                raise ComputerV2Exception("Division by zero")
        elif isinstance(token, Function):
            if (len(expression) != 1):
                if (len(result) < token.varnum):
                    raise ComputerV2Exception(f"Invalid number of arguments for function {token}")
                params = []
                for _ in range(token.varnum):
                    params.append(result.pop())
                result.append(token(*params))
            else:
                return token
        elif (isinstance(token, AType)):
            result.append(token)
        else:
            raise ComputerV2Exception(f"Invalid variable {token}")
    
    if (len(result) != 1):
        raise ComputerV2Exception("Invalid expression")
    return result.pop()

def evaluate_expression_str(expression: str):
   return evalute_postfix(infix_to_postfix(expression))

def evaluate_expression_wih_qm(expression: str):
    expr = expression.split("=")[0]
    if (expr[-1] != "?"):
        raise ComputerV2Exception("Invalid expression")
    expr = expr[:-1]
    result = evaluate_expression_str(expr)
    return result

def evaluate_equation(expression: str):
    left, right = expression[:-1].split("=")

    polynomial_expression = Polynomial_degree1.fromexpr(left) - Polynomial_degree1.fromexpr(right)

    if (polynomial_expression.degree > 2):
        raise ComputerV2Exception("The polynomial degree is stricly greater than 2, I can't solve.")
    if (polynomial_expression.degree == 0):
        if (polynomial_expression.coefs[0] == 0):
            return "All real numbers are solutions"
        return "No solution"
    if (polynomial_expression.degree == 1):
        return Polynomial_degree1(polynomial_expression.coefs).solve()
    if (polynomial_expression.degree == 2):
        return Polynomial_degree2(polynomial_expression.coefs).solve()
    
def evaluate_assignment(expression: str):
    from .globals import user_defined_variables
    variable_name, value = expression.split("=")
    variable_name = (re.sub(r"\s+", "", variable_name)).lower()
    
    if (not variable_name):
        raise ComputerV2Exception("Empty variable name")
    elif (variable_name == "i" or variable_name == "j"):
        raise ComputerV2Exception("Cannot assign to imaginary unit")
    elif (re.fullmatch(r"[a-zA-Z]+", variable_name)):
        result = evaluate_expression_str(value)
        user_defined_variables[variable_name] = result
    elif (m := re.fullmatch(r"([a-zA-Z]+)\((.+)\)", variable_name)): # function definition
        variables = m.group(2).split(",")
        for var in variables:
            if (not re.fullmatch(r"[a-zA-Z]+", var)):
                raise ComputerV2Exception(f"Invalid variable name: {var}, variable names must be alphabetic characters")
        list_of_functions = FunctionList(value, variables, m.group(1))
        user_defined_variables[m.group(1)] = list_of_functions
        result = list_of_functions.subvars()
    else:
        raise ComputerV2Exception(f"Invalid variable name: {variable_name}, variable names must be alphabetic characters")
    return result
    