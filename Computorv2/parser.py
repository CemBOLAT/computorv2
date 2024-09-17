from .exceptions import ComputerV2Exception
import re
from .globals import command_list
from .executor import evaluate_expression_str, evaluate_expression_wih_qm, evaluate_equation, evaluate_assignment

def eval_command(text: str) -> None:
    cmd_match = re.match(r":(.+?)\b", text)
    if not cmd_match:
        raise ComputerV2Exception("Invalid command")
    try:
        for command in command_list:
            if command["name"] == cmd_match.group(1).lower():
                if command["needs_params"]:
                    params = re.sub(r":[a-zA-Z]+", "", text)
                    if not params:
                        raise ComputerV2Exception(f"Command '{cmd_match.group(1)}' needs parameters")
                    command["function"](params)
                else:
                    command["function"]()
                return None
        raise ComputerV2Exception(f"Command '{cmd_match.group(1)}' not found")
    except Exception as e:
        raise ComputerV2Exception(f"Invalid command panel usage: {e}")
    
def parser(text: str) -> str:
    text = text.strip()
    if (len(text) == 0):
        return text
    if (text[0] == ":"):
        eval_command(text)
        return ""
    if "=" in text:
        if text.count("=") > 1:
            raise ComputerV2Exception(f"Invalid number of equal signs in expression: {text}")
        text = re.sub(r"\s+", "", text)
        if (text[-1] == "?"):
            if text[-2] == "=":
                return evaluate_expression_wih_qm(text)
            return evaluate_equation(text)
        else:
            return evaluate_assignment(text)
    else:
        return evaluate_expression_str(text)

