class Rational:
    def __init__(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self.value = value
        elif isinstance(value, Rational):
            self.value = value.value
        else:
            raise ValueError("Rational class only accepts integer or float values.")

    def __add__(self, other):
        from .Imaginary import Imaginary
        if isinstance(other, Rational):
            return Rational(self.value + other.value)
        elif isinstance(other, Imaginary):
            return Imaginary(self.value + other.real_part.value, other.imag_part.value)
        elif isinstance(other, (int, float)):
            return Rational(self.value + other)
        raise TypeError("Unsupported operation between Rational and non-Rational")

    def __sub__(self, other):
        from .Imaginary import Imaginary
        if isinstance(other, Rational):
            return Rational(self.value - other.value)
        elif isinstance(other, Imaginary):
            return Imaginary(self.value - other.real_part.value, other.imag_part.value)
        elif isinstance(other, (int, float)):
            return Rational(self.value - other)
        raise TypeError("Unsupported operation between Rational and non-Rational")

    def __mul__(self, other):
        from .Imaginary import Imaginary
        from .Matrix import Matrix
        if isinstance(other, Rational):
            return Rational(self.value * other.value)
        elif isinstance(other, Imaginary):
            return Imaginary(self.value * other.real_part.value, self.value * other.imag_part.value)
        elif isinstance(other, (int, float)):
            return Rational(self.value * other)
        elif isinstance(other, Matrix):
            result = [[value * self for value in row] for row in other.rows]
            return Matrix(result)
        raise TypeError("Unsupported operation between Rational and non-Rational")

    def __truediv__(self, other):
        from .Imaginary import Imaginary
        from .Matrix import Matrix
        if isinstance(other, Rational):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero is undefined")
            return Rational(self.value / other.value)
        elif isinstance(other, Imaginary):
            if other.real_part.value == 0 and other.imag_part.value == 0:
                raise ZeroDivisionError("Division by zero is undefined")
            return Imaginary(self.value / other.real_part.value, self.value / other.imag_part.value)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero is undefined")
            return Rational(self.value / other)
        elif isinstance(other, Matrix):
            raise TypeError("Unsupported operation between Rational and Matrix")
        raise TypeError("Unsupported operation between Rational and non-Rational")
    
    def __pow__(self, other):
        if isinstance(other, Rational):
            return Rational(self.value ** other.value)
        elif isinstance(other, (int, float)):
            return Rational(self.value ** other)
        raise TypeError("Unsupported operation between Rational and non-Rational")
    
    def __mod__(self, other):
        if isinstance(other, Rational):
            return Rational(self.value % other.value)
        elif isinstance(other, (int, float)):
            return Rational(self.value % other)
        raise TypeError("Unsupported operation between Rational and non-Rational")

    def __str__(self):
        return str(self.value)
