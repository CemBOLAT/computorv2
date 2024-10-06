from .Imaginary import Imaginary
from .Rational import Rational
from enum import auto

class Matrix:
    def __init__(self, rows):
        # Matris elemanlarının hepsi Rational veya Imaginary olmalı
        self.rows = [[self.convert_to_type(value) for value in row] for row in rows]

    def convert_to_type(self, value):
        """ Değerleri uygun türe dönüştür. """
        if isinstance(value, Imaginary):
            return value
        elif isinstance(value, (int, float)):
            return Rational(value)  # Sayıları Rational olarak sakla
        elif isinstance(value, Rational):
            return value
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def __add__(self, other):
        if isinstance(other, Matrix):
            if len(self.rows) != len(other.rows) or len(self.rows[0]) != len(other.rows[0]):
                raise ValueError("Matrix dimensions must match")
            result = [[self.rows[i][j] + other.rows[i][j] for j in range(len(self.rows[0]))] for i in range(len(self.rows))]
            return Matrix(result)
        raise TypeError("Unsupported operation for Matrix and non-Matrix")

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if len(self.rows) != len(other.rows) or len(self.rows[0]) != len(other.rows[0]):
                raise ValueError("Matrix dimensions must match")
            result = [[self.rows[i][j] - other.rows[i][j] for j in range(len(self.rows[0]))] for i in range(len(self.rows))]
            return Matrix(result)
        raise TypeError("Unsupported operation for Matrix and non-Matrix")

    def __mul__(self, other):
        if isinstance(other, Matrix):
            print(len(self.rows[0]), len(other.rows))
            if len(self.rows[0]) != len(other.rows):
                raise ValueError("Matrix dimensions are not aligned for multiplication")
            result = []
            for i in range(len(self.rows)):
                row = []
                for j in range(len(other.rows[0])):
                    if isinstance(self.rows[i][0], Imaginary):
                        value = Imaginary(0, 0)
                    elif isinstance(self.rows[i][0], Rational):
                        value = Rational(0)
                    elif isinstance(self.rows[i][0], (int, float)):
                        value = 0
                    for k in range(len(self.rows[0])):
                        value = self.rows[i][k] * other.rows[k][j] + value
                    row.append(value)
                result.append(row)
            return Matrix(result)
        elif isinstance(other, (Imaginary, Rational)):
            # Skalar çarpma
            result = [[self.rows[i][j] * other for j in range(len(self.rows[0]))] for i in range(len(self.rows))]
            return Matrix(result)
        raise TypeError("Unsupported operation for Matrix and non-Matrix")

    def __str__(self):
        return "\n".join(["[" + " , ".join([str(item) for item in row]) + "]" for row in self.rows])
