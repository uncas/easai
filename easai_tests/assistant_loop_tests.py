import unittest

from openai import OpenAI

from easai.assistant.loop import get_system_prompt, get_user_prompt, run_tool_loop
from easai.assistant.tool import AssistantTool

class AssistantUnitTests(unittest.TestCase):
	def test_run_tool_loop(self):
		from dotenv import load_dotenv
		load_dotenv(override = True)
		messages = [get_system_prompt("You are a helpful assistant.")]
		messages.append(get_user_prompt("How is the weather?"))
		self.tool_called = False
		def get_weather():
			return "sunny"
		def assert_tool_call(message):
			self.tool_called = True
			self.assertEqual(message, "Calling function get_weather")
		tools = [
			AssistantTool(
				method = get_weather,
				description = "Retrieve the current weather")
		]
		client = OpenAI()
		
		result = run_tool_loop(
			client = client,
			tools = tools,
			messages = messages,
			model = "gpt-4o-mini",
			tool_message_callback = assert_tool_call)
		
		self.assertIn("sunny", result[-1].content)
		self.assertTrue(self.tool_called)
