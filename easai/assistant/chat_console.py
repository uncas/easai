from easai.assistant.log import AiLogBase, LoggingAiLog
from easai.assistant.assistant import Assistant, run_assistant, get_system_prompt, get_user_prompt
from easai.utils.console_formatting import background, foreground, style

def run_chat_console(
		assistant: Assistant = None,
		your_name: str = "You",
		ai_logger: AiLogBase = LoggingAiLog()):
	assistant = assistant if assistant is not None else Assistant()
	messages = [get_system_prompt(assistant.system_prompt)]
	print_assistant_message("Hello! How can I help you?")
	while True:
		prompt = input(background.BLUE + foreground.WHITE + get_role_console_line(your_name) + " ")
		print()
		if prompt == "bye":
			print_assistant_message("Good bye!", skip_bye_info = True)
			return
		messages.append(get_user_prompt(prompt))
		messages = run_assistant(
			assistant = assistant,
			messages = messages,
			assistant_message_callback = print_assistant_message,
			tool_message_callback = print_tool_message,
			ai_logger = ai_logger)

def get_role_console_line(role : str):
	return "  " + role.ljust(11) + style.RESET_ALL + " : "

def print_assistant_message(content, skip_bye_info = False):
	bye_info = " (Enter 'bye' to quit.)" if not skip_bye_info else ""
	print(background.GREEN + foreground.WHITE + get_role_console_line("Assistant"), content, bye_info)
	print()

def print_tool_message(content):
	print(background.YELLOW + foreground.WHITE + get_role_console_line("Tool"), content)
	print()
