import unittest

from easai.assistant.chat_console import run_chat_console

class ChatConsoleTests(unittest.TestCase):
	def test_run_chat_console(self):
		from dotenv import load_dotenv
		load_dotenv(override = True)
		run_chat_console()
