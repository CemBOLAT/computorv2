from Digit import Digit

# production rules <float> : <digit>+ '.' <digit>*
class Float():
    pattern = f"{Digit.pattern}+\\.{Digit.pattern}*"