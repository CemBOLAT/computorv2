
from .exceptions import ComputerV2Exception
from .globals import user_defined_functions, user_defined_variables
from .lexer import Lexer
from .expander import Expander
from .executer import Executer
from .globals import TokenType
from .Types.Imaginary import Imaginary
import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        # İlk olarak var<id> = <expression>, <id> = <expression> ya da <expression> olup olmadığını kontrol et
        if self.tokens[self.pos][1] == TokenType.KW_VAR:
            return self.parse_var_assignment()
        elif self.tokens[self.pos][1] == TokenType.IDENTIFIER and self.peek_next_token_type() == TokenType.SIGN_EQUAL:
            return self.parse_assignment()
        elif self.tokens[self.pos][1] == TokenType.KW_FUNC:
            # KW_FUNC, IDENTIFIER, LPAREN, NUMBER|IMAGINARY, RPAREN > function call

            # Liste uzunluğu yeterli mi?
            if len(self.tokens) > self.pos + 4:
                if self.tokens[self.pos + 1][1] == TokenType.IDENTIFIER and self.tokens[self.pos + 2][1] == TokenType.LPAREN and self.tokens[self.pos + 3][1] in (TokenType.INTEGER, TokenType.FLOAT, TokenType.IDENTIFIER, TokenType.IMAGINARY) and self.tokens[self.pos + 4][1] == TokenType.RPAREN:
                    
                    # Eğer parametre bir değişkense (IDENTIFIER), onu user_defined_variables içinde kontrol edin
                    if self.tokens[self.pos + 3][1] == TokenType.IDENTIFIER:
                        if self.tokens[self.pos + 3][0] in user_defined_variables:
                            return self.parse_function_call()
                        else:
                            return self.parse_function_definition()
                    # Değişken değilse (örneğin INTEGER), doğrudan parse_function_call yap
                    return self.parse_function_call()

            return self.parse_function_definition()

        else:
            return self.parse_expression()


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
        
        return ('function_call', function_name, param)


    def parse_var_assignment(self):
        # var<id> = <expression> yapısını çözümle
        self.pos += 1  # 'var' atla
        if self.pos >= len(self.tokens):
            raise ComputerV2Exception("Expected variable name after 'var' keyword.")
        variable = self.tokens[self.pos][0]
        self.pos += 2  # <id> ve = işaretini atla
        if self.pos >= len(self.tokens):
            raise ComputerV2Exception("Expected expression after '='.")
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
        else:
            raise ComputerV2Exception(f"Unexpected token {token}.")

    def peek_next_token_type(self):
        # Sonraki token tipini kontrol et
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1][1]
        return None


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
        print("Lexer valid")
    parser = Parser(lexer.tokens)
    if test:
        print("Parser ok", parser)
    tokens = parser.parse()
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
