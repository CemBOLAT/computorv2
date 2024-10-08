from .Types.Imaginary import Imaginary
from .Types.Matrix import Matrix
from .Types.Rational import Rational, String
from .globals import user_defined_variables
from .globals import user_defined_variables, user_defined_functions
from .exceptions import ComputerV2Exception
from math import sin, cos, tan, sqrt
from .my_math import _abs

class Executer:
    def execute(self, node):
        if isinstance(node, tuple) and node[0] == 'variables_and_functions':
            # Değişkenleri ve fonksiyonları stringe kaydet
            variables_and_functions = ""
            variable_keys = list(user_defined_variables.keys())
            varialbe_values = list(user_defined_variables.values())
            for i in range(len(variable_keys)):
                variables_and_functions += f"{variable_keys[i]} = {varialbe_values[i]}\n"
            function_keys = list(user_defined_functions.keys())
            function_values = list(user_defined_functions.values())
            for i in range(len(function_keys)):
                variables_and_functions += f"{function_keys[i]} = {self.expression_from_node(function_values[i][1])}\n"

            variables_and_functions = variables_and_functions.strip()
            return variables_and_functions


        if isinstance(node, tuple) and node[0] in ('+', '-', '*', '/', '**', '%', '^'):
            left = self.execute(node[1])
            right = self.execute(node[2])

            # Burada left ve right'ın Rational olup olmadığını kontrol edin
            if isinstance(left, (int, float)):
                left = Rational(left)
            if isinstance(right, (int, float)):
                right = Rational(right)
            if isinstance(left, str):
                left = String(left)
            if isinstance(right, str):
                right = String(right)


            if node[0] == '+':
                if isinstance(left, String) or isinstance(right, String):
                    return str(left) + " + " + str(right)
                return left + right
            elif node[0] == '-':
                if isinstance(left, String) or isinstance(right, String):
                    return str(left) + " - " + str(right)
                return left - right
            elif node[0] == '*':
                if isinstance(left, String) or isinstance(right, String):
                    return str(left) + " * " + str(right)
                return left * right
            elif node[0] == '/':
                if isinstance(left, String) or isinstance(right, String):
                    return str(left) + " / " + str(right)
                return left / right
            elif node[0] == '**':  # matrix multiplication
                if isinstance(left, Matrix) and isinstance(right, Matrix):
                    return left * right
                else:
                    raise Exception("Matrix multiplication is only allowed between two matrices.")
            elif node[0] == '^':
                if isinstance(left, String) or isinstance(right, String):
                    return str(left) + " ^ " + str(right)
                return left ** right
            elif node[0] == '%':
                if isinstance(left, String) or isinstance(right, String):
                    return str(left) + " % " + str(right)
                return left % right

        elif isinstance(node, str) and node in user_defined_variables:
            return user_defined_variables[node]  # Değişkeni döndür
        
        # Buraya ekle
        elif isinstance(node, Matrix):
            return node  # Eğer node bir Matrix ise olduğu gibi döndür
        
        # Buraya ekle
        elif isinstance(node, (int, float)):
            return Rational(node)  # Eğer node bir int veya float ise Rational olarak döndür

        # Matris oluşturma
        elif isinstance(node, tuple) and node[0] == 'matrix':
            matrix_data = node[1]  # matrisi içeren veriyi al
            return Matrix(matrix_data)  # Matris oluştur
        elif isinstance(node, tuple) and node[0] == 'function_def':
            # Fonksiyon tanımlamasını kaydet
            function_name = node[1]
            param = node[2]
            body = node[3]
            # Tanımlanan fonksiyonu yazdır
            return (f"{function_name}({param}) = {self.expression_from_node(body)}")
        elif isinstance(node, tuple) and node[0] == 'function_call':
            function_name = node[1]
            param = self.execute(node[2])  # Parametreyi çözümle
            return self.execute_function_call(function_name, param)
        elif isinstance(node, tuple) and node[0] == 'sin':
            result = self.execute(node[1])
            if (not isinstance(result, (int, float))) and (not isinstance(result, Rational)):
                raise ComputerV2Exception(f"Invalid argument for sin function: {result}")
            print("type of result: ", type(result))
            return sin(result)
        elif isinstance(node, tuple) and node[0] == 'cos':
            result = self.execute(node[1])
            if (not isinstance(result, (int, float))) and (not isinstance(result, Rational)):
                raise ComputerV2Exception(f"Invalid argument for cos function: {result}")
            return cos(result)
        elif isinstance(node, tuple) and node[0] == 'tan':
            result = self.execute(node[1])
            if (not isinstance(result, (int, float))) and (not isinstance(result, Rational)):
                raise ComputerV2Exception(f"Invalid argument for tan function: {result}")
            return tan(result)
        elif isinstance(node, tuple) and node[0] == 'cot':
            result = self.execute(node[1])
            if (not isinstance(result, (int, float))) and (not isinstance(result, Rational)):
                raise ComputerV2Exception(f"Invalid argument for cot function: {result}")
            return 1.0 / result
        elif isinstance(node, tuple) and node[0] == 'sqrt':
            result = self.execute(node[1])
            if (not isinstance(result, (int, float))) and (not isinstance(result, Rational)):
                raise ComputerV2Exception(f"Invalid argument for sqrt function: {result}")
            if result < 0:
                raise ComputerV2Exception("Square root of a negative number is not allowed.")
            return sqrt(result)
        elif isinstance(node, tuple) and node[0] == 'abs':
            result = self.execute(node[1])
            if (not isinstance(result, (int, float))) and (not isinstance(result, Rational)):
                raise ComputerV2Exception(f"Invalid argument for abs function: {result}")
            return _abs(result)
        else:
            return node  # Sayı, Imaginary, Matrix, Rational ya da değişken olursa olduğu gibi döndür

    def expression_from_node(self, node):
        """ Node yapısından ifadenin string temsiline dönüşüm yapar. """
        if isinstance(node, tuple):
            if node[0] == 'binary_op':
                left = self.expression_from_node(node[2])
                right = self.expression_from_node(node[3])
                return f"({left} {node[1]} {right})"
            elif node[0] == 'num':
                return str(node[1])
            elif node[0] == 'var':
                return node[1]
            elif node[0] == 'imaginary':
                return str(node[1])  # Imaginary türünü string olarak döndür
        return str(node)  # Diğer türleri olduğu gibi döndür
    

    def execute_function_call(self, function_name, param):
        # Fonksiyon çağrısını yürüt
        if function_name not in user_defined_functions:
            raise ComputerV2Exception(f"Function {function_name} is not defined.")
        
        func_param, func_body = user_defined_functions[function_name]
        
        # Parametreyi geçici olarak değişkenlere ekleyin
        user_defined_variables[func_param] = param
        
        # Gövdeyi yürütün
        return self.execute(func_body)