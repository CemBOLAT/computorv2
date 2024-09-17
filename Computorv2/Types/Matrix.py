from ..exceptions import ComputerV2Exception
from .AType import AType
from .Complex import Real
from ..executor import evaluate_expression_str

class Matrix(AType):
    pattern = (r"\[\[.*?\]\]")

    def __init__(self, body) -> None:
        if type(body) is list and type(body[0]) is list:
            self.body = body
        elif type(body) is str:
            rows = body[1:-1].split(";")
            self.body = []
            prev = -1
            for r in rows:
                row = []
                nums = r[1:-1].split(",")
                for n in nums:
                    row.append(evaluate_expression_str(n))
                if prev != -1 and prev != len(row):
                    raise ComputerV2Exception("Inconsistent number of elements in matrix rows")
                prev = len(row)
                self.body.append(row)
        else:
            raise ComputerV2Exception("Invalid matrix format.")
        
    def __str__(self) -> str:
        res = ""
        for e in self.body:
            res += str([str(n) for n in e]) + "\n"
        return res.strip()
    
    def __mul__(self, other):
        if (isinstance(other, Real)):
            res = []
            for r in self.body:
                row = []
                for e in r:
                    row.append(e * other)
                res.append(row)
            return Matrix(res)
        elif (isinstance(other, Matrix)):
            if (len(self.body[0]) != len(other.body)):
                raise ComputerV2Exception("Incompatible matrices.")
            res = []
            for i in range(len(self.body)):
                row = []
                for j in range(len(other.body[0])):
                    s = 0
                    for k in range(len(self.body[0])):
                        s += self.body[i][k] * other.body[k][j]
                    row.append(s)
                res.append(row)
            return Matrix(res)
        else:
            raise ComputerV2Exception("Invalid matrix multiplication.")
        
    def __add__(self, other):
        if (isinstance(other, Matrix)):
            if (len(self.body) != len(other.body) or len(self.body[0]) != len(other.body[0])):
                raise ComputerV2Exception("Incompatible matrices.")
            res = []
            for i in range(len(self.body)):
                row = []
                for j in range(len(self.body[0])):
                    row.append(self.body[i][j] + other.body[i][j])
                res.append(row)
            return Matrix(res)
        else:
            raise ComputerV2Exception("Invalid matrix addition.")
        
    def __sub__(self, other):
        if (isinstance(other, Matrix)):
            if (len(self.body) != len(other.body) or len(self.body[0]) != len(other.body[0])):
                raise ComputerV2Exception("Incompatible matrices.")
            res = []
            for i in range(len(self.body)):
                row = []
                for j in range(len(self.body[0])):
                    row.append(self.body[i][j] - other.body[i][j])
                res.append(row)
            return Matrix(res)
        else:
            raise ComputerV2Exception("Invalid matrix subtraction.")
        
    @property
    def cols(self):
        return len(self.body[0])

    @property
    def rows(self):
        return len(self.body)


class Vector(Matrix):
    pattern = r"\[.*?\]"