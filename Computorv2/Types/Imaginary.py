from .Rational import Rational
class Imaginary:
    def __init__(self, real_part=0, imag_part=0):
        self.real_part = Rational(real_part)  # Gerçek kısım
        self.imag_part = Rational(imag_part)  # Hayali kısım

    def __add__(self, other):
        if isinstance(other, Imaginary):
            return Imaginary(self.real_part + other.real_part, self.imag_part + other.imag_part)
        elif isinstance(other, (int, float)):
            return Imaginary(self.real_part + other, self.imag_part)
        elif isinstance(other, Rational):
            return Imaginary(self.real_part + other.value, self.imag_part)
        raise TypeError("Unsupported operation for Imaginary and non-Imaginary")

    def __sub__(self, other):
        if isinstance(other, Imaginary):
            return Imaginary(self.real_part - other.real_part, self.imag_part - other.imag_part)
        elif isinstance(other, (int, float)):
            return Imaginary(self.real_part - other, self.imag_part)
        elif isinstance(other, Rational):
            return Imaginary(self.real_part - other.value, self.imag_part)
        raise TypeError("Unsupported operation for Imaginary and non-Imaginary")

    def __mul__(self, other):
        if isinstance(other, Imaginary):
            real = (self.real_part * other.real_part) - (self.imag_part * other.imag_part)
            imag = (self.real_part * other.imag_part) + (self.imag_part * other.real_part)
            return Imaginary(real, imag)
        elif isinstance(other, (int, float)):
            return Imaginary(self.real_part * other, self.imag_part * other)
        elif isinstance(other, Rational):
            return Imaginary(self.real_part * other.value, self.imag_part * other.value)
        raise TypeError("Unsupported operation for Imaginary and non-Imaginary")

    def __truediv__(self, other):
        if isinstance(other, Imaginary):
            denom = other.real_part.value ** 2 + other.imag_part.value ** 2
            real = (self.real_part.value * other.real_part.value + self.imag_part.value * other.imag_part.value) / denom
            imag = (self.imag_part.value * other.real_part.value - self.real_part.value * other.imag_part.value) / denom
            return Imaginary(real, imag)
        elif isinstance(other, (int, float)):
            return Imaginary(self.real_part / other, self.imag_part / other)
        elif isinstance(other, Rational):
            return Imaginary(self.real_part / other.value, self.imag_part / other.value)
        raise TypeError("Unsupported operation for Imaginary and non-Imaginary")
    
    def __pow__(self, other):
        if isinstance(other, (int, float)):
            return Imaginary(self.real_part ** other, self.imag_part ** other)
        elif isinstance(other, Rational):
            return Imaginary(self.real_part ** other.value, self.imag_part ** other.value)
        raise TypeError("Unsupported operation for Imaginary and non-Imaginary")
    
    def __eq__(self, other):
        if isinstance(other, Imaginary):
            return self.real_part == other.real_part and self.imag_part == other.imag_part
        elif isinstance(other, (int, float)):
            return self.real_part == other and self.imag_part == 0
        elif isinstance(other, Rational):
            return self.real_part == other.value and self.imag_part == 0
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        if isinstance(other, Imaginary):
            return abs(self) < abs(other)
        elif isinstance(other, (int, float)):
            return abs(self) < abs(Imaginary(other))
        elif isinstance(other, Rational):
            return abs(self) < abs(Imaginary(other.value))
        raise TypeError("Unsupported operation for Imaginary and non-Imaginary")

    def __gt__(self, other):
        return not self < other
    
    def __le__(self, other):
        return self < other or self == other
    
    def __ge__(self, other):
        return not self < other
    
    def __pos__(self): # +Imaginary
        return Imaginary(self.real_part, self.imag_part)
    
    def __int__(self):
        if (self.imag_part == 0):
            return int(self.real_part)
        elif (self.real_part == 0):
            return f"{int(self.imag_part)}i"
        else:
            return f"{int(self.real_part)} + {int(self.imag_part)}i"
    
    def __float__(self):
        if (self.imag_part == 0):
            return float(self.real_part)
        elif (self.real_part == 0):
            return f"{float(self.imag_part)}i"
        else:
            return f"{float(self.real_part)} + {float(self.imag_part)}i"

    def __neg__(self):
        return Imaginary(-self.real_part, -self.imag_part)
    
    def __abs__(self):
        return (self.real_part ** 2 + self.imag_part ** 2) ** 0.5
    
    
    
    def __str__(self):
        if self.imag_part.value == 0:
            return str(self.real_part)
        elif self.real_part.value == 0:
            return f"{self.imag_part}i"
        else:
            return f"{self.real_part} + {self.imag_part}i"
