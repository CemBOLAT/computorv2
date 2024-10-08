class String:
    def __init__(self, value):
        if isinstance(value, str):
            self.value = value
        else:
            raise ValueError("String class only accepts string values.")
    
    def __add__(self, other):
        from .Imaginary import Imaginary
        from .Matrix import Matrix
        if isinstance(other, String):
            return String(self.value + " + " + other.value)
        elif isinstance(other, (Rational, Imaginary, Matrix, int, float)):
            return String(self.value + " + " + str(other))  # Diğer tipleri string'e çevir
        elif isinstance(other, str):
            return String(self.value + " + " + other)
        raise TypeError("Unsupported operation between String and non-String")
    
    def __sub__(self, other):
        from .Imaginary import Imaginary
        from .Matrix import Matrix
        if isinstance(other, String):
            return String(self.value + " - " + other.value)
        elif isinstance(other, (Rational, Imaginary, Matrix, int, float)):
            return String(self.value + " - " + str(other))  # Diğer tipleri string'e çevir
        elif isinstance(other, str):
            return String(self.value + " - " + other)
        raise TypeError("Unsupported operation between String and non-String")
    
    def __mul__(self, other):
        from .Imaginary import Imaginary
        from .Matrix import Matrix
        if isinstance(other, String):
            return String(self.value + " * " + other.value)
        elif isinstance(other, (Rational, Imaginary, Matrix, int, float)):
            return String(self.value + " * " + str(other))  # Diğer tipleri string'e çevir
        elif isinstance(other, str):
            return String(self.value + " * " + other)
        raise TypeError("Unsupported operation between String and non-String")
    
    def __truediv__(self, other):
        from .Imaginary import Imaginary
        from .Matrix import Matrix
        if isinstance(other, String):
            return String(self.value + " / " + other.value)
        elif isinstance(other, (Rational, Imaginary, Matrix, int, float)):
            return String(self.value + " / " + str(other))  # Diğer tipleri string'e çevir
        elif isinstance(other, str):
            return String(self.value + " / " + other)
        raise TypeError("Unsupported operation between String and non-String")
    
    def __pow__(self, other):
        from .Imaginary import Imaginary
        from .Matrix import Matrix
        if isinstance(other, String):
            return String(self.value + " ^ " + other.value)
        elif isinstance(other, (Rational, Imaginary, Matrix, int, float)):
            return String(self.value + " ^ " + str(other))  # Diğer tipleri string'e çevir
        elif isinstance(other, str):
            return String(self.value + " ^ " + other)
        raise TypeError("Unsupported operation between String and non-String")
    
    def __mod__(self, other):
        from .Imaginary import Imaginary
        from .Matrix import Matrix
        if isinstance(other, String):
            return String(self.value + " % " + other.value)
        elif isinstance(other, (Rational, Imaginary, Matrix, int, float)):
            return String(self.value + " % " + str(other))  # Diğer tipleri string'e çevir
        elif isinstance(other, str):
            return String(self.value + " % " + other)
        raise TypeError("Unsupported operation between String and non-String")
    
    def __eq__(self, other):
        if isinstance(other, String):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, String):
            return self.value < other.value
        elif isinstance(other, str):
            return self.value < other
        return False
    
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        return not self.__le__(other)
    
    def __ge__(self, other):
        return not self.__lt__(other)
    
    def __neg__(self):
        return String("-" + self.value)
    
    def __pos__(self):
        return String("+" + self.value)
    
    def __abs__(self):
        return String(abs(self.value))
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value


class Rational:
    def __init__(self, value):
        if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
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
        elif isinstance(other, String):
            return str(self) + " + " + other
        raise TypeError("Unsupported operation between Rational and non-Rational")

    def __sub__(self, other):
        from .Imaginary import Imaginary
        if isinstance(other, Rational):
            return Rational(self.value - other.value)
        elif isinstance(other, Imaginary):
            return Imaginary(self.value - other.real_part.value, other.imag_part.value)
        elif isinstance(other, (int, float)):
            return Rational(self.value - other)
        elif isinstance(other, String):
            return str(self) + " - " + other
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
        elif isinstance(other, String):
            return str(self) + " * " + other
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
        elif isinstance(other, String):
            return str(self) + " / " + other
        raise TypeError("Unsupported operation between Rational and non-Rational")
    
    def __pow__(self, other):
        if isinstance(other, Rational):
            return Rational(self.value ** other.value)
        elif isinstance(other, (int, float)):
            return Rational(self.value ** other)
        elif isinstance(other, str):
            return str(self.value) + other
        elif isinstance(other, str):
            return str(self.value) + " ^ " + other
        raise TypeError("Unsupported operation between Rational and non-Rational")
    
    def __mod__(self, other):
        if isinstance(other, Rational):
            return Rational(self.value % other.value)
        elif isinstance(other, (int, float)):
            return Rational(self.value % other)
        elif isinstance(other, String):
            return str(self) + " % " + other
        raise TypeError("Unsupported operation between Rational and non-Rational")
    
    def __eq__(self, other):
        if isinstance(other, Rational):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, Rational):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        return False
    
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        return not self.__le__(other)
    
    def __ge__(self, other):
        return not self.__lt__(other)
    
    def __neg__(self):
        return Rational(-self.value)
    
    def __pos__(self):
        return Rational(self.value)
    
    def __abs__(self):
        return Rational(abs(self.value))
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)

    def __str__(self):
        return str(self.value)
