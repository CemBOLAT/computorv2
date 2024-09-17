from .Types.Complex import Real

def _abs(x):
    return x if x >= 0 else -x

def _pow(x, n):
    if n == 0:
        return 1
    if n == 1:
        return x
    if n > 0:
        while n > 1:
            x *= x
            n -= 1
        return x
    else:
        while n < -1:
            x /= x
            n += 1
        return 1 / x

def _sqrt(number):
    tolerance = 1e-15
    if number < 0:
        raise ValueError("Cannot compute the square root of a negative number.")

    guess = number / 2.0  # Initial guess
    while True:
        new_guess = (guess + number / guess) / 2.0
        if _abs(new_guess - guess) < tolerance:
            return new_guess
        guess = new_guess


def ft_sqrt(x: Real):
    return Real(_sqrt(x.re))


def _max(a: Real, b: Real):
    return (a if a > b else b)


def _min(a: Real, b: Real):
    return (a if a < b else b)

def _delta(a: Real, b: Real, c: Real):
    return _pow(b.re, 2) - 4 * a.re * c.re
