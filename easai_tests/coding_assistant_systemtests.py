import unittest
import shutil

from dotenv import load_dotenv

from easai.assistant.assistant import Assistant, get_user_prompt, run_assistant
from easai.assistant.tools.coding_tool import CodingTool

class CodingAssistantSystemTests(unittest.TestCase):
	def setUp(self):
		load_dotenv(override = True)
		self.test_folder = "output/coding_tool_system_test"
		shutil.rmtree(self.test_folder, ignore_errors=True)

	def test_assistant_with_coding_tool(self):
		coding_tools = CodingTool(self.test_folder, approve_execution = True).get_all_tools()
		coding_assistant = Assistant(tools = coding_tools)
		messages = [get_user_prompt("Create a python script that can print 'hello world'.")]
		messages = run_assistant(
			assistant = coding_assistant,
			messages = messages,
			assistant_message_callback = print,
			tool_message_callback = print)
		messages.append(get_user_prompt("Then edit it to print 'hello universe' instead."))
		messages = run_assistant(
			assistant = coding_assistant,
			messages = messages)
