from .Types.Imaginary import Imaginary
from .Types.Matrix import Matrix
from .Types.Rational import Rational
from .globals import user_defined_variables

class Executer:
    def execute(self, node):
        if isinstance(node, tuple) and node[0] in ('+', '-', '*', '/', '**', '%', '^'):
            left = self.execute(node[1])
            right = self.execute(node[2])

            # Burada left ve right'ın Rational olup olmadığını kontrol edin
            if isinstance(left, (int, float)):
                left = Rational(left)
            if isinstance(right, (int, float)):
                right = Rational(right)

            if node[0] == '+':
                return left + right
            elif node[0] == '-':
                return left - right
            elif node[0] == '*':
                return left * right
            elif node[0] == '/':
                return left / right
            elif node[0] == '**':  # matrix multiplication
                if isinstance(left, Matrix) and isinstance(right, Matrix):
                    return left * right
                else:
                    raise Exception("Matrix multiplication is only allowed between two matrices.")
            elif node[0] == '^':
                return left ** right
            elif node[0] == '%':
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