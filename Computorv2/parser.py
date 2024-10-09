
from .exceptions import ComputerV2Exception
from .globals import user_defined_functions, user_defined_variables
from .lexer import Lexer
from .expander import Expander
from .executer import Executer
from .globals import TokenType
from .Types.Imaginary import Imaginary
from .Types.Symbol import Symbol
from .Types.Equation import Equation
import re
import math
from .Types.Rational import Rational

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        # İlk olarak var<id> = <expression>, <id> = <expression> ya da <expression> olup olmadığını kontrol et
        if len(self.tokens) > self.pos + 2 and self.tokens[self.pos][1] == TokenType.KW_VAR and self.tokens[self.pos + 1][1] == TokenType.IDENTIFIER and self.tokens[self.pos + 2][1] == TokenType.SIGN_EQUAL:
            return self.parse_var_assignment()
        elif self.tokens[self.pos][1] == TokenType.IDENTIFIER and self.peek_next_token_type() == TokenType.SIGN_EQUAL:
            return self.parse_assignment()
        elif self.tokens[len(self.tokens) - 1][1] == TokenType.SIGN_QMARK and self.tokens[len(self.tokens) - 2][1] == TokenType.SIGN_EQUAL:
            # delete the last two tokens
            del self.tokens[self.pos - 1]
            del self.tokens[self.pos - 1]
            return self.parse()
        elif self.tokens[self.pos][1] == TokenType.KW_LIST:
            return self.parse_variables_and_functions()
        # son tokende ? ve bir öncesidne IDENTIFIER varsa bu bir polinomdur
        elif self.tokens[len(self.tokens) - 1][1] == TokenType.SIGN_QMARK:
            return self.parse_polynomial()
        elif self.tokens[self.pos][1] == TokenType.KW_FUNC:
            # KW_FUNC, IDENTIFIER, LPAREN, IDENTIFIER, RPAREN ve eşittir işareti -> function definition
            if len(self.tokens) > self.pos + 5 and self.tokens[self.pos + 1][1] == TokenType.IDENTIFIER and self.tokens[self.pos + 2][1] == TokenType.LPAREN and self.tokens[self.pos + 3][1] == TokenType.IDENTIFIER and self.tokens[self.pos + 4][1] == TokenType.RPAREN and self.tokens[self.pos + 5][1] == TokenType.SIGN_EQUAL:
                return self.parse_function_definition()
            # Eğer IDENTIFIER ve parantez var ise (function call)
            elif len(self.tokens) > self.pos + 2 and self.tokens[self.pos + 1][1] == TokenType.IDENTIFIER and self.tokens[self.pos + 2][1] == TokenType.LPAREN:
                return self.parse_function_call()
            elif self.peek_next_token_type() == TokenType.IDENTIFIER:
                # return the variable value
                key = self.tokens[self.pos + 1][0]
                # eğer key yoksa hata ver
                if key not in user_defined_functions:
                    raise ComputerV2Exception(f"Undefined variable {key}.")
                variable_tuple = user_defined_functions[self.tokens[self.pos + 1][0]]
                tuple_creation = ('function_def', key, variable_tuple[0], variable_tuple[1])
                return tuple_creation
        else:
            return self.parse_expression()
        
    def parse_variables_and_functions(self):
        # return all saved variables and functions from user_defined_variables and user_defined_functions
        return ('variables_and_functions', user_defined_variables, user_defined_functions)

    def collect_coefficients(self, expr, symbol_name):
        """
        Recursively collect coefficients for x^2, x, and constant terms from an expression.
        Returns a tuple (a, b, c) for ax^2 + bx + c.
        Raises an exception if an exponent greater than 2 is encountered.
        """
        if expr[0] == 'num':
            return 0, 0, expr[1]  # Constant term
        elif expr[0] == 'var' and expr[1] == symbol_name:
            return 0, 1, 0  # Linear term
        elif expr[0] == 'binary_op':
            op = expr[1]
            left_a, left_b, left_c = self.collect_coefficients(expr[2], symbol_name)
            right_a, right_b, right_c = self.collect_coefficients(expr[3], symbol_name)
            
            if op == '+':
                return left_a + right_a, left_b + right_b, left_c + right_c
            elif op == '-':
                return left_a - right_a, left_b - right_b, left_c - right_c
            elif op == '*':
                # Detecting quadratic terms and linear terms
                if expr[2][0] == 'num' and expr[3][0] == 'var' and expr[3][1] == symbol_name:
                    return 0, expr[2][1], 0  # Linear term
                elif expr[3][0] == 'num' and expr[2][0] == 'var' and expr[2][1] == symbol_name:
                    return 0, expr[3][1], 0  # Linear term
                elif expr[2][0] == 'binary_op' and expr[2][1] == '^' and expr[2][2][1] == symbol_name:
                    if expr[2][3][0] == 'num' and expr[2][3][1] > 2:
                        raise ComputerV2Exception("Polynomial terms with exponents greater than 2 are not supported.")
                    return expr[3][1], 0, 0  # Quadratic term
                elif expr[3][0] == 'binary_op' and expr[3][1] == '^' and expr[3][2][1] == symbol_name:
                    if expr[3][3][0] == 'num' and expr[3][3][1] > 2:
                        raise ComputerV2Exception("Polynomial terms with exponents greater than 2 are not supported.")
                    return expr[2][1], 0, 0  # Quadratic term
            elif op == '^':
                if expr[2][0] == 'var' and expr[3][0] == 'num':
                    exponent = expr[3][1]
                    if exponent != 2 and exponent != 1 and exponent != 0:
                        raise ComputerV2Exception("Only polynomials with exponents 0, 1, and 2 are supported.")
                    elif exponent == 2:
                        return 1, 0, 0  # Quadratic term
                    elif exponent == 1:
                        return 0, 1, 0  # Linear term
                    else:  # exponent == 0
                        return 0, 0, 1  # This essentially makes it a constant term
        return 0, 0, 0
    
    def parse_polynomial(self):
        if len(self.tokens) < 8:
            raise ComputerV2Exception("Invalid polynomial expression.")
        # Remove the question mark '?'
        self.tokens.pop()

        # Retrieve the function name
        function_name_token = self.tokens[1]
        function_name = function_name_token[0]

        # Check if the function is defined
        if function_name not in user_defined_functions:
            raise ComputerV2Exception(f"Function {function_name} is not defined.")
        
        # Move position to target value location
        self.pos = 6
        target_value_expr = self.parse_expression()

        target_value_expr = Expander().expand(target_value_expr)


        target_value_expr = Executer().execute(target_value_expr)

        # Get function definition and unpack parameter and expression
        func_definition = user_defined_functions[function_name]
        param_name, body_expr = func_definition

        # Parse the target value expression (either as a variable or constant)
        target_value = target_value_expr

        # Verify polynomial degree and collect coefficients
        a, b, c = self.collect_coefficients(body_expr, param_name)
        a = Rational(a)
        b = Rational(b)
        c = Rational(c)
        if a > 2:
            raise ComputerV2Exception("Only polynomials of degree 2 or lower are supported.")

        # Solve the polynomial ax^2 + bx + (c - target_value) = 0
        solutions = self.solve_polynomial(a, b, c - target_value)
        
        solutionsRet = []

        for solution in solutions:
            if isinstance(solution, Imaginary):
                solutionsRet.append(f"{solution.real_part} + {solution.imag_part}i")
            else:
                solutionsRet.append(str(solution))
        
        return ('solutions', solutions)

    def solve_polynomial(self, a, b, c):
        """
        Solves a polynomial of the form ax^2 + bx + c = 0.
        Returns a list of solutions.
        """
        # Check if it's a linear equation (a = 0)
        if a == 0:
            if b == 0:
                return [] if c != 0 else ["All real numbers"]  # No solution or all solutions
            return [-c / b]  # Linear solution

        # Quadratic solution
        Rational_2 = Rational(2)
        Rational_4 = Rational(4)
        discriminant = b ** Rational_2 - Rational_4 * a * c
        if discriminant < 0:
            solution1 = Imaginary(-b, math.sqrt(-discriminant)) / (Rational_2 * a)
            solution2 = Imaginary(-b, -math.sqrt(-discriminant)) / (Rational_2 * a)
            return [solution1, solution2]
        elif discriminant == 0:
            return [-b / (Rational_2 * a)]  # Single solution
        else:
            sqrt_disc = math.sqrt(discriminant)
            return [(-b + sqrt_disc) / (Rational_2 * a), (-b - sqrt_disc) / (Rational_2 * a)]


    def parse_function_call(self):
        # funA(5) gibi bir fonksiyon çağrısını çözümle
        self.pos += 1  # 'fun' anahtar kelimesini atla
        if self.pos >= len(self.tokens):
            raise ComputerV2Exception("Expected function name after 'fun' keyword.")
        function_name = self.tokens[self.pos][0]  # Fonksiyon adı
        
        self.pos += 1  # Fonksiyon adını atla
        if self.pos >= len(self.tokens) or self.tokens[self.pos][1] != TokenType.LPAREN:
            raise ComputerV2Exception("Expected '(' after function name.")
        
        self.pos += 1  # Parantezi atla
        if self.pos >= len(self.tokens):
            raise ComputerV2Exception("Expected parameter after '('.")
        param = self.parse_expression()  # Parametreyi işleyin

        if self.tokens[self.pos][1] != TokenType.RPAREN:
            raise ComputerV2Exception("Expected ')' after parameter.")
        self.pos += 1  # Parantezi atla
        
        return (('function_call', function_name, param))


    def parse_var_assignment(self):
        # var<id> = <expression> yapısını çözümle
        self.pos += 1  # 'var' atla
        if self.pos >= len(self.tokens):
            raise ComputerV2Exception("Expected variable name after 'var' keyword.")
        variable = self.tokens[self.pos][0]
        self.pos += 1  # <id> ve = işaretini atla
        if self.pos >= len(self.tokens):
            self.pos -= 1
            return self.parse_expression()
        self.pos += 1
        expression = self.parse_expression()
        return ('var_assignment', variable, expression)

    def parse_assignment(self):
        # <id> = <expression> yapısını çözümle
        variable = self.tokens[self.pos][0]
        self.pos += 2  # <id> ve = işaretini atla
        expression = self.parse_expression()
        return ('assignment', variable, expression)

    def parse_function_definition(self):
        # fun<id>(<id>) = <expression> yapısını çözümle
        self.pos += 1  # 'fun' anahtar kelimesini atla
        if self.pos >= len(self.tokens):
            raise ComputerV2Exception("Expected function name after 'fun' keyword.")
        function_name = self.tokens[self.pos][0]  # Fonksiyon adı
        self.pos += 1  # Fonksiyon adını atla
        if self.pos >= len(self.tokens) or self.tokens[self.pos][1] != TokenType.LPAREN:
            raise ComputerV2Exception(f"Expected '(' after function name.")

        self.pos += 1  # '(' karakterini atla
        if self.pos >= len(self.tokens):
            raise ComputerV2Exception(f"Expected parameter after '('.")
        param = self.tokens[self.pos][0]  # Parametre
        self.pos += 1  # Parametreyi atla

        if self.pos >= len(self.tokens) or self.tokens[self.pos][1] != TokenType.RPAREN:
            raise ComputerV2Exception(f"Expected ')' after parameter.")

        self.pos += 1  # ')' karakterini atla

        if self.pos >= len(self.tokens) or self.tokens[self.pos][1] != TokenType.SIGN_EQUAL:
            raise ComputerV2Exception(f"Expected '=' after function parameters.")

        self.pos += 1  # '=' karakterini atla
        body = self.parse_expression()  # Fonksiyon gövdesini çözümle

        return ('function_def', function_name, param, body)  # Fonksiyon tanımı döndür

    def parse_expression(self):
        left = self.parse_term()  # İlk terimi al
        
        while self.pos < len(self.tokens):
            token, token_type = self.tokens[self.pos]

            if token_type in (TokenType.OP_PLUS, TokenType.OP_MINUS):
                self.pos += 1
                right = self.parse_term()  # Sağ terimi al
                left = ('binary_op', token, left, right)  # Binary işlem olarak kaydet

            else:
                break  # Daha fazla işlem yoksa döngüden çık

        return left
    
    def parse_matrix(self):
        self.pos += 1  # [ karakterini atla
        matrix = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] != TokenType.S_RPAREN:  # ] karakterine kadar devam et
            row = self.parse_row()  # Satırları çözümle
            matrix.append(row)
            if self.tokens[self.pos][1] == TokenType.OP_SEMICOLON:  # ; karakterini kontrol et
                self.pos += 1  # ; karakterini atla
        self.pos += 1  # ] karakterini atla
        return ('matrix', matrix)

    def parse_row(self):
        self.pos += 1  # [ karakterini atla
        row = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] != TokenType.S_RPAREN:  # ] karakterine kadar devam et
            token, token_type = self.tokens[self.pos]
            if token_type == TokenType.INTEGER or token_type == TokenType.FLOAT:
                value = float(token) if token_type == TokenType.FLOAT else int(token)
                row.append(value)
                self.pos += 1
                if self.tokens[self.pos][1] == TokenType.OP_COLON:  # , karakterini kontrol et
                    self.pos += 1  # , karakterini atla
            elif token_type == TokenType.S_RPAREN:  # Son eleman kontrolü
                break
            else:
                raise ComputerV2Exception(f"Unexpected token {token} in row.")
        self.pos += 1  # ] karakterini atla
        return row


    def parse_term(self):
        # Çarpma, bölme ve üstel işlemler
        left = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in (TokenType.OP_MULTIPLY, TokenType.OP_DIVIDE, TokenType.OP_POWER, TokenType.OP_MODULO, TokenType.OP_MATRICE_MULTIPLY):
            operator = self.tokens[self.pos][0]
            self.pos += 1
            right = self.parse_factor()
            left = ('binary_op', operator, left, right)
        return left

    def parse_factor(self):
        # Sayılar, değişkenler veya parantezli ifadeler
        token, token_type = self.tokens[self.pos]
        
        if token_type == TokenType.INTEGER or token_type == TokenType.FLOAT:
            self.pos += 1
            return ('num', float(token) if token_type == TokenType.FLOAT else int(token))
        elif token_type == TokenType.IDENTIFIER:
            self.pos += 1
            return ('var', token)
        elif token_type == TokenType.IMAGINARY:
            self.pos += 1
            return ('imaginary', Imaginary(0, 1))  # burada 1, hayali kısmı temsil eder
        elif token_type == TokenType.LPAREN:
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] == TokenType.RPAREN:
                self.pos += 1
            return expr
        elif token_type == TokenType.S_LPAREN:  # Matris başlangıcını kontrol et
            return self.parse_matrix()  # Matrisleri parse et
        elif token_type == TokenType.KW_FUNC:
            return self.parse_function_call()
        elif token_type == TokenType.KW_VAR:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected variable name after 'var' keyword.")
            variable = self.tokens[self.pos][0]
            self.pos += 1
            return ('var', variable)
        elif token_type == TokenType.OP_MINUS:
            self.pos += 1
            # Negatif sayıyı bir binary işlem olarak tanı
            if self.tokens[self.pos][1] in (TokenType.INTEGER, TokenType.FLOAT):
                # Negatif sayıyı döndür
                value = -float(self.tokens[self.pos][0]) if self.tokens[self.pos][1] == TokenType.FLOAT else -int(self.tokens[self.pos][0])
                self.pos += 1
                return ('num', value)
            elif self.tokens[self.pos][1] == TokenType.IMAGINARY:
                self.pos += 1
                return ('imaginary', Imaginary(0, -1))  # Negatif hayali sayıyı döndür
        elif token_type == TokenType.KW_SIN:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected '(' after 'sin' keyword.")
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] != TokenType.RPAREN:
                raise ComputerV2Exception("Expected ')' after expression.")
            self.pos += 1
            return ('sin', expr)
        elif token_type == TokenType.KW_RAD:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected '(' after 'sin' keyword.")
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] != TokenType.RPAREN:
                raise ComputerV2Exception("Expected ')' after expression.")
            self.pos += 1
            return ('rad', expr)
        elif token_type == TokenType.KW_EXP:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected '(' after 'sin' keyword.")
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] != TokenType.RPAREN:
                raise ComputerV2Exception("Expected ')' after expression.")
            self.pos += 1
            return ('exp', expr)
        elif token_type == TokenType.KW_COS:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected '(' after 'cos' keyword.")
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] != TokenType.RPAREN:
                raise ComputerV2Exception("Expected ')' after expression.")
            self.pos += 1
            return ('cos', expr)
        elif token_type == TokenType.KW_TAN:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected '(' after 'tan' keyword.")
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] != TokenType.RPAREN:
                raise ComputerV2Exception("Expected ')' after expression.")
            self.pos += 1
            return ('tan', expr)
        elif token_type == TokenType.KW_COT:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected '(' after 'cot' keyword.")
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] != TokenType.RPAREN:
                raise ComputerV2Exception("Expected ')' after expression.")
            self.pos += 1
            return ('cot', expr)
        elif token_type == TokenType.KW_SQRT:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected '(' after 'sqrt' keyword.")
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] != TokenType.RPAREN:
                raise ComputerV2Exception("Expected ')' after expression.")
            self.pos += 1
            return ('sqrt', expr)
        elif token_type == TokenType.KW_ABS:
            self.pos += 1
            if self.pos >= len(self.tokens):
                raise ComputerV2Exception("Expected '(' after 'abs' keyword.")
            self.pos += 1
            expr = self.parse_expression()
            if self.tokens[self.pos][1] != TokenType.RPAREN:
                raise ComputerV2Exception("Expected ')' after expression.")
            self.pos += 1
            return ('abs', expr)
        else:
            raise ComputerV2Exception(f"Unexpected token {token}.")
    
    def peek_next_token_type(self):
        # Sonraki token tipini kontrol et
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1][1]
        return None

def print_whole_history(number_of_history:int):
    str_history = ""
    # with open(".computorv2_history_result", "r") as file:
    #     str_history = file.read()
    
    # read last number_of_history lines
    with open(".computorv2_history_result", "r") as file:
        lines = file.readlines()
        for line in lines[-number_of_history:]:
            str_history += line

    return str_history

def parser(line:str) -> list:
    """
    Parser function for the Computorv2 project.
    """
    line = line.replace(" ", "")
    line = line.lower()

    lexer = Lexer(line)

    if not lexer.tokens:
        raise ComputerV2Exception("No tokens found.")
    
    test = False

    if test:
        print("Lexer ok")
    lexer.is_valid()
    if test:
        print("Lexer valid", lexer.tokens)
    parser = Parser(lexer.tokens)
    if test:
        print("Parser ok", parser)
    tokens = parser.parse()
    if (isinstance(tokens, tuple) and tokens[0] == 'solutions'):
        # Number of solutions
        n = len(tokens[1])
        if n == 0:
            return "No real solutions"
        elif n == 1:
            return f"Single solution: {tokens[1][0]}"
        else:
            return f"Two solutions: {tokens[1][0]} and {tokens[1][1]}"
    if (lexer.tokens[0][1] == TokenType.KW_PRINT_HISTORY):
        if len(lexer.tokens) == 1:
            return print_whole_history(1)
        else:
            return print_whole_history(int(lexer.tokens[1][0]))
    if test:
        print("Parser valid", tokens)
    expander = Expander()
    if test:
        print("Expander ok")
    expanded = expander.expand(tokens)
    if test:
        print("Expander valid", expanded)
    executer = Executer()  # Executer instance oluşturuyoruz
    if test:
        print("Executer ok : ", expanded)
    result = executer.execute(expanded)  # execute() metodunu instance ile çağırıyoruz
    return result
