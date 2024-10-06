from .globals import user_defined_functions, user_defined_variables, token_patterns, TokenType
from .exceptions import ComputerV2Exception
import re


class Lexer():

    def __init__(self, expression:str):
        self.expression = expression
        self.tokens = []
        self.index = 0
        self.current_token = None
        self.tokenize()

    def tokenize(self):
        while self.index < len(self.expression):
            match = self.match_get_next_token()
            if match:
                self.tokens.append(match)
            else:
                raise ComputerV2Exception(f"Invalid token at index {self.index} in expression: {self.expression}")
    
    def match_get_next_token(self):
        remaining_expression = self.expression[self.index:]  # Geriye kalan ifadenin tamamını al
        for pattern, token_type in token_patterns:
            match = re.match(pattern, remaining_expression)
            if match:
                token = match.group(0)
                self.index += len(token)  # İlerlemeden sonra indexi güncelle
                return (token, token_type)
        return None
        
    def is_valid(self):
        # Parantezlerin validasyonu için stack kullanımı
        stack = []
        equalSign, questionMark = 0, 0
        operators = [TokenType.OP_PLUS, TokenType.OP_MINUS, TokenType.OP_MULTIPLY, TokenType.OP_DIVIDE, TokenType.OP_MATRICE_MULTIPLY, TokenType.OP_POWER, TokenType.OP_MODULO]
        keywords = [TokenType.KW_VAR, TokenType.KW_FUNC]
        types = [TokenType.FLOAT, TokenType.INTEGER, TokenType.IDENTIFIER]
        open_parenthesis = [TokenType.LPAREN, TokenType.S_LPAREN]
        close_parenthesis = [TokenType.RPAREN, TokenType.S_RPAREN]
        matrice_operators = [TokenType.OP_COLON, TokenType.OP_SEMICOLON]
        imaginary = [TokenType.IMAGINARY]

        for i, (token, token_type) in enumerate(self.tokens):
            if token_type in open_parenthesis:
                stack.append(token_type)
            elif token_type in close_parenthesis:
                if not stack:
                    raise ComputerV2Exception(f"Unbalanced parenthesis at token {token}.")
                if (token_type == TokenType.RPAREN and stack[-1] != TokenType.LPAREN) or (token_type == TokenType.S_RPAREN and stack[-1] != TokenType.S_LPAREN):
                    raise ComputerV2Exception(f"Unmatched parenthesis at token {token}.")
                stack.pop()
            elif token_type == TokenType.SIGN_EQUAL:
                equalSign += 1
                if i == 0:
                    # Eşittir işareti ilk token olamaz
                    raise ComputerV2Exception(f"Equal sign {token} cannot be the first token.")
            elif token_type == TokenType.SIGN_QMARK:
                # Soru işareti en son olmalı
                if i != len(self.tokens) - 1:
                    raise ComputerV2Exception(f"Question mark {token} must be the last token.")
                if i > 0 and (self.tokens[i - 1][1] != TokenType.SIGN_EQUAL and self.tokens[i - 1][1] != TokenType.IDENTIFIER):
                    raise ComputerV2Exception(f"Question mark {token} must be preceded by an equal sign or an identifier.")
                questionMark += 1
            elif token_type in operators:
                # Operatör son token olamaz
                if i == len(self.tokens) - 1:
                    raise ComputerV2Exception(f"Operator {token} cannot be the last token.")
                elif i == 0 and token_type != TokenType.OP_MINUS:
                    # Operatör ilk token olamaz
                    raise ComputerV2Exception(f"Operator {token} cannot be the first token.")
                # Arka arkaya iki operatör olamaz
                if self.tokens[i + 1][1] in operators:
                    raise ComputerV2Exception(f"Invalid consecutive operators {token} and {self.tokens[i + 1][0]}.")
            elif token_type in types:
                # Tip son token olabilir ve tipten sonra tip gelebilir (örneğin: 4 * 5 veya 4 5)
                pass
            elif token_type in keywords:
                # Keyword sonrasında identifier olmalı
                if i + 1 == len(self.tokens) or self.tokens[i + 1][1] != TokenType.IDENTIFIER:
                    raise ComputerV2Exception(f"Invalid token after keyword {token}.")
            elif token_type in matrice_operators:
                # ; için sağında açık parantez, solunda kapalı parantez olmalı
                if token_type == TokenType.OP_SEMICOLON:
                    if i == 0 or self.tokens[i - 1][1] != TokenType.S_RPAREN:
                        raise ComputerV2Exception(f"Invalid token before {token}.")
                    if i == len(self.tokens) - 1 or self.tokens[i + 1][1] != TokenType.S_LPAREN:
                        raise ComputerV2Exception(f"Invalid token after {token}.")
                # : için sağında ve solunda tip olmalı
                elif token_type == TokenType.OP_COLON:
                    if i == 0 or self.tokens[i - 1][1] not in types:
                        raise ComputerV2Exception(f"Invalid token before {token}.")
                    if i == len(self.tokens) - 1 or self.tokens[i + 1][1] not in types:
                        raise ComputerV2Exception(f"Invalid token after {token}.")
            elif token_type in imaginary:
                # Imaginary tek başına olabilir veya son token olabilir
                if i > 0 and self.tokens[i - 1][1] not in (operators + types) and i != len(self.tokens) - 1:
                    raise ComputerV2Exception(f"Invalid token before imaginary {token}.")
                #Bir önceki token bir tip ise, tip ile imaginary arasına * işareti ekle
                if i > 0 and self.tokens[i - 1][1] in types:
                    self.tokens.insert(i, ("*", TokenType.OP_MULTIPLY))
            
        # Tek bir eşittir ve soru işareti olmalı
        if equalSign > 1:
            raise ComputerV2Exception("Multiple equal signs are not allowed.")
        if questionMark > 1:
            raise ComputerV2Exception("Multiple question marks are not allowed.")
        # Parantezler dengeli olmalı
        if stack:
            raise ComputerV2Exception("Unbalanced parenthesis.")
