import unittest

from easai.assistant.tool import create_tool_from_method

class AssistantToolUnitTests(unittest.TestCase):

	def test_create_tool_from_method(self):
		def my_method(param1, param2):
			"""This is my method documentation
			Args:
				param1 (int): The first parameter
				param2 (str): The second parameter
			"""
			pass

		tool = create_tool_from_method(my_method)

		self.assertEqual(tool.name, "my_method")
		self.assertEqual(tool.description, "This is my method documentation")
		self.assertEqual(tool.parameters[0].name, "param1")
		self.assertEqual(tool.parameters[0].description, "The first parameter")
		self.assertEqual(tool.parameters[0].type, "integer")
		self.assertEqual(tool.parameters[1].name, "param2")
		self.assertEqual(tool.parameters[1].description, "The second parameter")
		self.assertEqual(tool.parameters[1].type, "string")

	def test_create_tool_from_method_without_docs(self):
		def my_method(param1, param2):
			pass

		tool = create_tool_from_method(my_method)

		self.assertEqual(tool.name, "my_method")
		self.assertEqual(tool.description, "my_method")
		self.assertEqual(tool.parameters[0].name, "param1")
		self.assertEqual(tool.parameters[0].description, "param1")
		self.assertEqual(tool.parameters[0].type, "string")
		self.assertEqual(tool.parameters[1].name, "param2")
		self.assertEqual(tool.parameters[1].description, "param2")
		self.assertEqual(tool.parameters[1].type, "string")
