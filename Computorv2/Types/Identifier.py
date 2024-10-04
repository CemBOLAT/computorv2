from Letter import Letter
# production rules: <id> : <letter> <letter>*

class Identifier():
    pattern = f"{Letter.pattern}{Letter.pattern}*"