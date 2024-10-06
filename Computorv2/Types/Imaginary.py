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

    def __str__(self):
        if self.imag_part.value == 0:
            return str(self.real_part)
        elif self.real_part.value == 0:
            return f"{self.imag_part}i"
        else:
            return f"{self.real_part} + {self.imag_part}i"
