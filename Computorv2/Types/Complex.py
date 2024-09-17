from ..exceptions import ComputerV2Exception
from .AType import AType
import copy
import re


class Complex(AType):
    _real_patern = r"\d+(?:\.\d+)?" # pattern for real number : 1, 1.0, 1.1
    pattern = (r"(-?{})([+-]{})i".format(_real_patern, _real_patern))

    def __init__(self, *args, **kwargs) -> None:
        if (len(args) == 1 and type(args[0]) is str):
            expr: str = re.sub(r"\s+", "", args[0])
            match = re.fullmatch(Complex.pattern, expr)
            if match:
                self.re, self.im = list(map(float, match.groups()))
            else:
                raise ComputerV2Exception("Invalid complex number.")
        elif (len(args) == 2):
            self.re, self.im = float(args[0]), float(args[1])
        else:
            raise ComputerV2Exception("Invalid complex number.")
        
    def __add__(self, other):
        if (isinstance(other, Complex)):
            return Complex.resolve(Complex(self.re + other.re, self.im + other.im))
        elif (isinstance(other, Real)):
            return Complex.resolve(Complex(self.re + other.re, self.im))
        elif (isinstance(other, Imaginary)):
            return Complex.resolve(Complex(self.re, self.im + other.im))
        
    def __sub__(self, other):
        if (isinstance(other, Complex)):
            return Complex.resolve(Complex(self.re - other.re, self.im - other.im))
        elif (isinstance(other, Real)):
            return Complex.resolve(Complex(self.re - other.re, self.im))
        elif (isinstance(other, Imaginary)):
            return Complex.resolve(Complex(self.re, self.im - other.im))
    
    def __mul__(self, other):
        from .Matrix import Matrix
        if (isinstance(other, Complex)):
            return Complex.resolve(Complex(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re))
        elif (isinstance(other, Real)):
            return Complex.resolve(Complex(self.re * other.re, self.im * other.re))
        elif (isinstance(other, Imaginary)):
            return Complex.resolve(Complex(-self.im * other.im, self.re * other.im))
        elif (isinstance(other, Matrix)):
            if (isinstance(other, Matrix)):
                res = copy.deepcopy(other.body)
                for i in range(len(res)):
                    for j in range(len(res[i])):
                        res[i][j] = self * res[i][j]
                return Matrix(res)

    def __truediv__(self, other):
        from ..my_math import _pow
        if (isinstance(other, Complex)):
            real_part = self.re * other.re + self.im * other.im
            im_part = self.im * other.re - self.re * other.im
            div = _pow(other.re, 2) + _pow(other.im, 2)
            return Complex.resolve(Complex(real_part / div, im_part / div))
        elif (isinstance(other, Real)):
            return Complex.resolve(Complex(self.re / other.re, self.im / other.re))
        elif (isinstance(other, Imaginary)):
            return Complex.resolve(Complex(self.im / other.im, -self.re / other.im))
        
    def __pow__(self, other):
        if (isinstance(other, Complex)):
            if other.im or not other.re.is_integer() or other.re < 0:
                raise ComputerV2Exception("Power only supported with integer positive number in Complex number")
            res = Complex(1, 0)
            b = other.re
            while(b):
                if (b % 2):
                    res *= self
                self *= self
                b //= 2
            return Complex.resolve(res)
        raise ComputerV2Exception("Power only supported with integer positive number in Complex number")
    
    @property # getter
    def inv(self):
        from ..my_math import _pow
        diviser = _pow(self.re, 2) + _pow(self.im, 2)
        conjugate = self.conjugate
        return Complex(conjugate.re / diviser, conjugate.im / diviser)
    
    @property
    def magnitude(self):
        from ..my_math import _sqrt
        return _sqrt(self.re * self.re + self.im * self.im)
    
    @property # getter
    def conjugate(self):
        return Complex(self.re, -self.im)
    
    def __str__(self) -> str:
        if (self.im == 0 and self.re == 0):
            return "0"
        res = ""
        if (self.re):
            res += f"{self.re:g}"
        if (self.im):
            if self.re:
                res += f" {self.im:+g}i"
            else:
                res += f" {self.im:g}i"
        return res
    
    @staticmethod
    def resolve(comp):
        """
            if result imaginary part is real, then return a Real class objecet instead of Complex,
            to use Real class additional functionality like comparition
        """
        if comp.im == 0:
            return Real(comp.re)
        return comp

class Imaginary(Complex):
    pattern = (f"(?:{Complex._real_patern})?i")

    def __init__(self, value) -> None:
        if type(value) is str:
            expr: str = re.sub(r"\s+", "", value)
            match = re.fullmatch(f"({Complex._real_patern})?i", expr)
            if match:
                if (match.group(1)):
                    self.re, self.im = 0, float(match.group(1))
                else:
                    self.re, self.im = 0, 1
            else:
                raise ComputerV2Exception("Invalid imaginary number.")
        else:
            super().__init__(0, value)

    def __str__(self) -> str:
        return f"{self.im:g}i"

class Real(Complex):
    pattern = (Complex._real_patern)

    def __init__(self, value) -> None:
        super().__init__(value, 0)

    def __gt__(self, other):
        return self.re > other.re

    def __ge__(self, other):
        return self.re >= other.re

    def __lt__(self, other):
        return self.re < other.re

    def __le__(self, other):
        return self.re <= other.re

    def __str__(self) -> str:
        return f"{self.re:g}"

    def __mod__(self, other):
        return Real(self.re % other.re)
