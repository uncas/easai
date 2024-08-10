import json
import logging

from openai import OpenAI

from easai.assistant.tool import AssistantTool
from easai.assistant.log import AiLogBase, LoggingAiLog

class AssistantLoop:
	def __init__(self, client: OpenAI = None, model: str = "gpt-4o-mini", 
			  system_prompt: str = "You are a helpful assistant.",
			  tools: list[AssistantTool] = [], max_iterations: int = 10):
		self.client: OpenAI = client if client is not None else OpenAI()
		self.model: str = model
		self.system_prompt: str = system_prompt
		self.tools: list[AssistantTool] = tools
		self.max_iterations: int = max_iterations

def run_assistant_loop(
		messages: list = [],
		assistant_loop: AssistantLoop = None,
		assistant_message_callback = None,
		tool_message_callback = None,
		ai_logger: AiLogBase = LoggingAiLog()) -> list:
	"""Run assistant tool loop, calling tools until the assistant is satisfied.

	Args:
		assistant_loop (AssistantLoop): Assistant loop
		messages (list): List of messages
		assistant_message_callback (function, optional): Function to call when the assistant message is received. Defaults to None.
	"""
	assistant_loop = assistant_loop if assistant_loop is not None else AssistantLoop()
	client_tools = [tool.map_to_open_ai_tool() for tool in assistant_loop.tools]
	tool_methods = {tool.name: tool.method for tool in assistant_loop.tools}
	messages.insert(0, get_system_prompt(assistant_loop.system_prompt))
	message_count_at_last_log = len(messages) - 1
	for _ in range(assistant_loop.max_iterations):
		chat_completion = assistant_loop.client.chat.completions.create(
			messages = messages,
			model = assistant_loop.model,
			tools = client_tools if len(client_tools) > 0 else None
		)
		choice = chat_completion.choices[0]
		finish_reason = choice.finish_reason
		message = choice.message
		messages.append(message)
		ai_logger.log(assistant_loop.model, chat_completion.usage.prompt_tokens, chat_completion.usage.completion_tokens, messages[message_count_at_last_log:])
		message_count_at_last_log = len(messages)
		if finish_reason == "stop":
			if assistant_message_callback:
				assistant_message_callback(message.content)
			return messages
		elif finish_reason == "tool_calls":
			for tool_call in message.tool_calls:
				call_function = tool_call.function
				if call_function.name in tool_methods:
					function_name = call_function.name
					function_args = json.loads(call_function.arguments)
					function_response = None
					tool_method = tool_methods[function_name]
					if function_args:
						if tool_message_callback:
							tool_message_callback("Calling function " + function_name + " with " + str(function_args))
						function_response = tool_method(**function_args)
					else:
						if tool_message_callback:
							tool_message_callback("Calling function " + function_name)
						function_response = tool_method()
					messages.append({
						"role": "tool",
						"name": function_name,
						"tool_call_id": tool_call.id,
						"content": get_limited_message_content(json.dumps(function_response))
					})
	logger = logging.getLogger(__name__)
	logger.error("ERROR: Tool loop exited without stop reason, most likely due to too many iterations.")
	return messages

def get_limited_message_content(content, max_message_content_length = 100 * 1000):
	if len(content) <= max_message_content_length:
		return content

	logger = logging.getLogger(__name__)
	logger.warning(
		"Message content %s was too long, truncating to %d characters.",
		content[:50] + " ... " + content[-50:],
		max_message_content_length)
	return content[:max_message_content_length] + "..."

def get_system_prompt(content, max_message_content_length = 100 * 1000):
	return get_prompt("system", content, max_message_content_length)

def get_user_prompt(content, max_message_content_length = 100 * 1000):
	return get_prompt("user", content, max_message_content_length)

def get_prompt(role, content, max_message_content_length = 100 * 1000):
	return { "role": role, "content": get_limited_message_content(content, max_message_content_length) }
