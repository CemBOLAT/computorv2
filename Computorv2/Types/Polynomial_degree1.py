from .Polynomial import Polynomial

class Polynomial_degree1(Polynomial):
    def __init__(self, coefs):
        super().__init__(coefs)
        if (len(self.coefs) != 2):
            raise self.PolynominalError("Polynomial_degree1 can only be created with a degree of 1.")
        
    def solve(self) -> str:
        res = ""
        b, a = self.coefs
        res += (str(self) + " = 0\n")
        res += ("a first degree equation with one solution :") + "\n"
        res += ("x = %f" % (-b / a))
        return res
    
    @classmethod
    def fromexpr(self, expr):
        result = Polynomial.fromexpr(expr)
        if (result.degree != 1):
            raise self.PolynominalError("Polynomial_degree1 can only be created with a degree of 1.")
        return Polynomial_degree1(result.coefs)