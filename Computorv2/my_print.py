from .exceptions import ComputerV2Exception
import re

def _print(params: str):
    from .globals import user_defined_variables, builtin_functions, computorv_commands
    from .executor import evaluate_expression_str
    tokens = map(str.strip, params.split(","))
    for t in tokens:
        if (t[0] == "$"):
            try:
                computorv_commands[t[1:].lower()]()
            except KeyError:
                raise ChildProcessError(f"special variable '{t}' not found")
        elif m := re.fullmatch(r"[\"'](.+)[\"']", t):
            print(m.group(1), end=" ")
        else:
            print(evaluate_expression_str(t), end=" ")
    print()
