import os
import sys
import asyncio
import selectors
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from TextEditor.TextEditor import TextEditor
from Computorv2.parser import parser

def print_txt_to_file(result, text):
	if result:
		with open('.computorv2_history_result', 'a') as f:
			f.write(f"{text} = {result}\n")

def main(prompt_session):

	if len(sys.argv) > 1:
		try:
			with open(sys.argv[1], 'r') as f:
				for line in f:
					print(f"> {line}", end='')
					line = line.strip()
					#print(f"Result: {parser(line)}")
					result = parser(line)
					if result:
						TextEditor.print_colored(result, TextEditor.COLORS['green'])
		except FileNotFoundError:
			TextEditor.print_colored(f"File not found: {sys.argv[1]}", TextEditor.COLORS['red'])
		except FileExistsError:
			TextEditor.print_colored(f"File exists: {sys.argv[1]}", TextEditor.COLORS['red'])
		except PermissionError:
			TextEditor.print_colored(f"Permission denied: {sys.argv[1]}", TextEditor.COLORS['red'])
		except Exception as e:
			TextEditor.print_colored(e, TextEditor.COLORS['red'])
	
	while True:
		try:
			text = prompt_session.prompt('> ')
		except KeyboardInterrupt:
			continue
		except EOFError:
			TextEditor.print_colored("Exiting...", TextEditor.COLORS['red'])
			break
		else:
			try:
				if (text):
					result = parser(text)
					print_txt_to_file(result, text)
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