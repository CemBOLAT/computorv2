import re
import copy
from collections import deque
from .Function import FunctionList
from .Complex import Complex
from .Function import Function
from ..exceptions import ComputerV2Exception
from ..globals import operators
from enum import auto


class Polynomial:

    def __init__(self, coefficients):
        self.coefs = self.__trim_coefs(coefficients)
        self.degree = len(self.coefs) - 1

    def __str__(self):
        res = ""
        if (len(self.coefs) < 1):
            return ("0")
        for index, coef in enumerate(self.coefs):
            if (coef == 0):
                continue
            else:
                real_coef = auto()
                if (isinstance(coef, int) or coef.is_integer()):
                    real_coef = int(coef)
                else:
                    real_coef = float("%.2f" % coef)
                if (index == 0):
                    res += str(real_coef)
                else:
                    res += " + " if real_coef > 0 else " - "
                    if (abs(real_coef) != 1):
                        res += str(abs(real_coef))
                    if (index > 1):
                        res += "x^%d" % index
                    else:
                        res += "x"
        return (res)
    
    def __add__(self, other):
        p1 = self.coefs
        p2 = self._set_op_param("+", other).coefs

        # p1 is the bigger polynomial
        if (len(p1) < len(p2)):
            p1, p2 = p2, p1        
        
        for i in range(len(p2)):
            p1[i] += p2[i]
        
        return Polynomial(p1)
        
    def __sub__(self, other):
        p1 = self.coefs
        p2 = self._set_op_param("-", other).coefs

        if (len(p1) < len(p2)):
            # do the substraction in the other way
            for i in range(len(p1)):
                p2[i] -= p1[i]
                return Polynomial(p2)
        for i in range(len(p2)):
            p1[i] -= p2[i]
            return Polynomial(p1)
    
    def __mul__(self, other):
        p1 = self.coefs
        p2 = self._set_op_param("*", other).coefs
        new_len = len(p1) + len(p2) - 2 # -2 because we start at 0
        result = [0] * (new_len + 1)
        for i in range(len(p1)):
            for j in range(len(p2)):
                p1_coef = (p1[j] if j < len(p1) else 0)
                p2_coef = (p2[j] if i - j < len(p2) else 0)
                result[i] += p1_coef * p2_coef
        return Polynomial(self.__trim_coefs(result))

    def __truediv__(self, other):
        p1 = self.coefs
        n = int(self._set_op_param("/", other).coefs[0])

        for i in range(len(p1)):
            p1[i] /= n
        return Polynomial(p1)

    def __pow__(self, other):
        p1 = self
        n = self._set_op_param("**", other).coefs[0]

        if (n == 0):
            return Polynomial([1] * (self.degree + 1))
        if (n == 1):
            return copy.deepcopy(self)
        if (n < 0):
            raise self.PolynominalError("Can't raise a polynomial to a negative number.")
        if ((not n.is_integer()) or (not isinstance(n, int))):
            raise self.PolynominalError("Can't raise a polynomial to a non integer number.")
        result = p1
        n = int(n)
        for _ in range(n - 1): 
            result = result * p1

        return result
    
    @classmethod
    def fromexpr(self, expr):
        from ..executor import infix_to_postfix
        rpn_list = infix_to_postfix(expr)
        # check if there is more than one variables
        if len(set([e for e in rpn_list if isinstance(e, str) and re.fullmatch(r"[a-zA-Z]+", e)])) > 1:
            raise ComputerV2Exception(
                "functions  with more than one variables are not supported")
        i = 0
        while i < (len(rpn_list)):
            if isinstance(rpn_list[i], Function):
                if not isinstance(rpn_list[i], FunctionList):
                    raise ComputerV2Exception(
                        "built in functions are not supported in equations")
                if i - 1 >= 0:
                    rpn_list[i] = self.fromfunc(rpn_list[i])

                del rpn_list[i - 1]
            else:
                i += 1

        return self._eval_postfix(rpn_list)
    
    @classmethod
    def fromfunc(self, func):
        if (not isinstance(func, FunctionList)):
            raise ComputerV2Exception("Function must be a FunctionList")
        if (len(func.args) != 1):
            raise ComputerV2Exception("Function must have only one argument")

        rpn_list = func.rpn_list
        for i in range(len(rpn_list)):
            if type(rpn_list[i]) is str and rpn_list[i].isnumeric():
                rpn_list[i] = "x"
            else:
                raise ComputerV2Exception("Function must be a polynomial")
        return self._eval_postfix(rpn_list)


    def __trim_coefs(self, coefs):
        while (len(coefs) > 1 and coefs[-1] == 0):
            coefs.pop()
        return (coefs)
    
    def _set_op_param(self, op, other):
        if (not isinstance(other, Polynomial)):
            if (isinstance(other, int) or isinstance(other, float)):
                return Polynomial([other])
            else:
                raise self.PolynominalError(f"{op} is not suported for Polynomial an {type(other)}")
        else:
            if ((op == "/" or op == "**") and other.degree > 0):
                if op == "/":
                    raise self.PolynominalError("Can't divide by a Polynomial with degree more than 0 (real number).")
                if op == "**":
                    raise self.PolynominalError("Can't raise a polynomial with degree more than 0 (real number) to another polynomial.")
            return other
        
    @classmethod
    def _to_postfix(self, arr) -> list:
        operators = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3,
        }

        stack = deque()
        postfix = list()

        for elem in arr:
            if (elem == "("):
                stack.append(elem)
            elif (elem == ")"):
                while (len(stack) > 0):
                    e = stack.pop()
                    if (e == "("):
                        break
                    else:
                        stack.append(e)
            if (elem in operators):
                while (len(stack) > 0 and stack[-1] in operators and operators[stack[-1]] >= operators[elem]):
                    if (elem != "^"):
                        postfix.append(stack.pop())
                operators.append(elem)
            else:
                postfix.append(elem)
        while (len(stack) > 0):
            postfix.append(stack.pop())
        return postfix
    
    @classmethod
    def _eval_postfix(self, postfix):
        deq = deque()

        for elem in postfix:
            if (elem in operators):
                b = deq.pop()
                if (len(deq) == 0):
                    if (elem == "+" or elem == "-"):
                        a = Polynomial([0])
                    else:
                        raise ComputerV2Exception(
                            f"operator {elem} needs 2 oprands got 1")
                else:
                    a = deq.pop()
                deq.append(operators[elem]["func"](a, b))
            elif isinstance(elem, Function):
                if (len(deq) < elem.varnum):
                    raise ComputerV2Exception(f"Function {elem.name} needs {elem.varnum} operands")
                params = []
                for _ in range(elem.varnum):
                    params.append(deq.pop())
                deq.append(elem(*params).re)
            elif (isinstance(elem, Complex)):
                deq.append(self([elem.re]))
            elif(type(elem) is str):
                pattern = r"[a-zA-Z]+"
                if (re.match(pattern, elem)):
                    deq.append(self([0, 1]))
                else:
                    deq.append(self([float(elem)]))
            elif isinstance(elem, self):
                deq.append(elem)
            else:
                raise ComputerV2Exception("Invalid element in the postfix list")
        if (len(deq) == 0):
            raise ComputerV2Exception("Invalid expression in the postfix list")
        elif (len(deq) > 1):
            raise ComputerV2Exception("Invalid expression in the postfix list") 
        return deq[0]
        
    class PolynominalError(Exception):
        msg = ""

        def __init__(self, msg):
            self.msg = msg
            Exception.__init__(self, msg)

        def __str__(self):
            return (self.msg)