from .exceptions import ComputerV2Exception
from .globals import user_defined_functions, user_defined_variables
from math import sin, cos, tan, sqrt
from .my_math import _abs

class Expander:
    def __init__(self):
        pass

    def expand(self, node):
        if node[0] == 'num':
            return node[1]
        elif node[0] == 'var':
            if node[1] in user_defined_variables:
                return user_defined_variables[node[1]]
            else:
                return node[1].lower()
        elif node[0] == 'var_assignment':
            # Değişkeni kaydet
            user_defined_variables[node[1]] = self.expand(node[2])
            return user_defined_variables[node[1]]
        elif node[0] == 'assignment':
            # Değişkeni kaydet
            user_defined_variables[node[1]] = self.expand(node[2])
            return user_defined_variables[node[1]]
        elif node[0] == 'imaginary':
            return node[1]  # Imaginary sayı zaten genişletilmiş
        elif node[0] == 'binary_op':
            left = self.expand(node[2])
            right = self.expand(node[3])
            return (node[1], left, right)
        elif node[0] == 'function_def':
            # Fonksiyonu kaydet
            user_defined_functions[node[1]] = (node[2], node[3])
        elif node[0] == 'function_call':
            func_name, arg_expr = node[1], node[2]
            if func_name in user_defined_functions:
                param, body = user_defined_functions[func_name]
                arg_value = self.expand(arg_expr)
                return self.expand(self.substitute(body, param, arg_value))
            else:
                raise ComputerV2Exception(f"Undefined function {func_name}.")
        elif node[0] == 'sin':
            return ('sin', self.expand(node[1]))
        elif node[0] == 'cos':
            return ('cos', self.expand(node[1]))
        elif node[0] == 'tan':
            return ('tan', self.expand(node[1]))
        elif node[0] == 'cot':
            return ('cot', (self.expand(node[1])))
        elif node[0] == 'sqrt':
            return ('sqrt', (self.expand(node[1])))
        elif node[0] == 'abs':
            return ('abs', (self.expand(node[1])))
        elif node[0] == 'exp':
            return ('exp', (self.expand(node[1])))
        elif node[0] == 'rad':
            return ('rad', (self.expand(node[1])))
        return node

    def substitute(self, body, param, value):
        # Fonksiyon parametresinin yerine gerçek değer koyma
        if body[0] == 'var' and body[1] == param:
            return ('num', value)
        elif body[0] == 'binary_op':
            left = self.substitute(body[2], param, value)
            right = self.substitute(body[3], param, value)
            return ('binary_op', body[1], left, right)
        return body
