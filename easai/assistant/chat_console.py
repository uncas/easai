from openai import OpenAI

from easai.assistant.log import AiLogBase, LoggingAiLog
from easai.assistant.loop import run_tool_loop, get_system_prompt, get_user_prompt
from easai.assistant.tool import AssistantTool
from easai.utils.console_formatting import background, foreground, style

def run_chat_console(
		client: OpenAI,
		model: str = "gpt-4o-mini",
		system_prompt: str = "You are a helpful assistant.",
		your_name: str = "You",
		tools: list[AssistantTool] = [],
		ai_logger: AiLogBase = LoggingAiLog()):
	messages = [get_system_prompt(system_prompt)]
	print_assistant_message("Hello! How can I help you?")
	while True:
		prompt = input(background.BLUE + foreground.WHITE + get_role_console_line(your_name) + " ")
		print()
		if prompt == "bye":
			print_assistant_message("Good bye!", skip_bye_info = True)
			return
		messages.append(get_user_prompt(prompt))
		messages = run_tool_loop(
			client = client,
			tools = tools,
			messages = messages,
			model = model,
			max_iterations = 10,
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
