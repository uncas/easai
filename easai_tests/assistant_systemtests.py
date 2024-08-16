import unittest

from easai.assistant.assistant import Assistant, get_user_prompt, run_assistant
from easai.assistant.tool import AssistantTool, AssistantToolParameter
from dotenv import load_dotenv

class AssistantSystemTests(unittest.TestCase):

	def setUp(self):
		load_dotenv(override = True)

	def test_run_assistant(self):
		messages = [get_user_prompt("How is the weather in Italy?")]
		self.tool_called = False
		def get_weather(country: str):
			return "sunny in " + country
		def assert_tool_call(message):
			self.tool_called = True
			self.assertEqual(message, "Calling function get_weather with {'country': 'Italy'}")
		tools = [
			AssistantTool(
				method = get_weather,
				description = "Retrieve the current weather",
				parameters = [
					AssistantToolParameter(name = "country", description = "The country")
				])
		]
		
		result = run_assistant(
			assistant = Assistant(tools = tools),
			messages = messages,
			tool_message_callback = assert_tool_call)
		
		self.assertIn("sunny", result[-1].content)
		self.assertTrue(self.tool_called)

	def test_run_assistant_tools_with_array(self):
		messages = [get_user_prompt("How long are the files a.py and b.py?")]
		def get_lengths_of_files(files: list[str]):
			return [len(file) for file in files]
		tools = [
			AssistantTool(
				method = get_lengths_of_files,
				description = "Retrieve the lengths of the provided files",
				parameters = [
					AssistantToolParameter(name = "files", value = {
						"type": "array",
						"items": {
							"type": "string",
							"enum": [
								"a.py",
								"b.py",
								"c.py"
							]
						}
					})
				])
		]
		
		result = run_assistant(
			assistant = Assistant(tools = tools),
			messages = messages)
		
		self.assertIn("a.py", result[-1].content)

	def test_run_assistant_without_tools(self):
		messages = [get_user_prompt("Explain the sun")]
		
		result = run_assistant(messages = messages)
		
		self.assertIn("sun", str.lower(result[-1].content))
