class Equation:
    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr
    
    def __repr__(self):
        return f"{self.left_expr} = {self.right_expr}"
