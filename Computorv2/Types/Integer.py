from Digit import Digit

# production rules: <integer> : <digit>+

class Integer():
    pattern = f"{Digit.pattern}+"