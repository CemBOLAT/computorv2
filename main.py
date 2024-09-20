import os
import sys
import asyncio
import selectors
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from TextEditor.TextEditor import TextEditor
from Computorv2.parser import parser
import traceback

def main(prompt_session):

	if len(sys.argv) > 1:
		for fileName in sys.argv[1:]:
			try:
				with open(fileName, 'r') as f:
					for line in f:
						print(f"> {line}", end='')
						result = parser(line)
						if result:
							TextEditor.print_colored(result, TextEditor.COLORS['green'])
			except FileNotFoundError:
				TextEditor.print_colored(f"File not found: {fileName}", TextEditor.COLORS['red'])
			except FileExistsError:
				TextEditor.print_colored(f"File exists: {fileName}", TextEditor.COLORS['red'])
			except PermissionError:
				TextEditor.print_colored(f"Permission denied: {fileName}", TextEditor.COLORS['red'])
			except Exception as e:
				TextEditor.print_colored(e, TextEditor.COLORS['red'])
				traceback.print_exc()

	
	while True:
		try:
			text = prompt_session.prompt('> ')
		except KeyboardInterrupt:
			continue
		except EOFError:
			break
		else:
			try:
				if (text):
				    # computorv.eval_input(l)
					# print(res)
					result = parser(text)
					if result:
						TextEditor.print_colored(result, TextEditor.COLORS['green'])

					#TextEditor.print_colored(text, TextEditor.COLORS['green'])
			except Exception as e:
				TextEditor.print_colored(e, TextEditor.COLORS['red'])

if __name__ == '__main__':
	selector = selectors.SelectSelector()
	loop = asyncio.SelectorEventLoop(selector)
	asyncio.set_event_loop(loop)
	prompt_session = PromptSession(history=FileHistory(os.path.expanduser('.computorv2_history')))
	main(prompt_session)