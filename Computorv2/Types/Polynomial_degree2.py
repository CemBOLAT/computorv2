from .Polynomial import Polynomial
from enum import auto
from ..my_math import _sqrt

class Polynomial_degree2(Polynomial):
    def __init__(self, coefs):
        super().__init__(coefs)
        if (len(coefs) != 3):
            raise self.PolynominalError("Polynomial_degree1 can only be created with a degree of 1.")
        c = self.coefs[0]
        b = self.coefs[1]
        a = self.coefs[2]
        self.delta = (b * b) - (4 * a * c)
        self.x1 , self.x2 = self._getroots(b, a)

    @classmethod
    def fromexpr(self, expr):
        result = Polynomial.fromexpr(expr)
        if (result.degree != 2):
            raise self.PolynominalError(f"Affectation of a Polynomial_degree2 can only be done with a degree of 2, not {result.degree}.")
        else:
            return self(result.coefs)
        
    def solve(self) -> str:
        res = str(self) + " = 0\n" + "delta : %f" % self.delta + "\n"
        
        if (self.delta > 0):
            res += "Delta is strictly positive, there are two real solutions :\n"
            res += ("x1 = %f" % self.x1) + " \n"
            res += ("x2 = %f" % self.x2) + " \n"
        elif (self.delta == 0):
            res += "Delta is zero, there is one real solution :\n"
            res += ("x = %f" % self.x1) + " \n"
        else:
            res += "Delta is strictly negative, there are two complex solutions :\n"
            res += ("z1 = %f + %fi" % (self.x1[0], self.x1[1])) + "\n"
            res += ("z2 = %f + %fi" % (self.x2[0], self.x2[1]))

        return res
    def _getroots(self, b, a):
        x1 = auto()
        x2 = auto()

        if (self.delta > 0):
            x1 = (-b - _sqrt(self.delta)) / (2 * a)
            x2 = (-b + _sqrt(self.delta)) / (2 * a)
        elif (self.delta == 0):
            x1 = -b / (2 * a)
            x2 = x1
        else:
            sqrt_delta = _sqrt(-self.delta)
            x1 = (-b/(2 * a), -sqrt_delta/(2 * a))
            x2 = (-b/(2 * a), sqrt_delta/(2 * a))
        
        return (x1, x2)
