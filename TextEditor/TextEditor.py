class TextEditor:
    @staticmethod
    def print_colored(text, color="\033[37m"):
        """Print text with the given foreground color (default: white)"""
        print(f"{color}{text}\033[0m")

    # ANSI color codes for foreground
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
    }
