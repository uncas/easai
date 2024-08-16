import unittest
import shutil

from easai.assistant.tools.coding_tool import CodingTool

class CodingToolIntegrationTests(unittest.TestCase):
	def setUp(self):
		self.test_folder = "output/coding_tool_test"
		shutil.rmtree(self.test_folder, ignore_errors = True)

	def test_coding_tool(self):
		coding_tool = CodingTool(self.test_folder, approve_execution = False)
		coding_tool.save_code([
			{"folder_path": "", "file_name": "test.py", "code": "print('testing 1')"},
			{"folder_path": "", "file_name": "test2.py", "code": "print('testing 2')"},
			{"folder_path": "lib", "file_name": "test3.py", "code": "print('testing 3')"}
		])
		self.assertEqual(coding_tool.list_files(), ["test.py", "test2.py", "lib/test3.py"])
		self.assertEqual(
			coding_tool.read_code(["test.py", "lib/test3.py"]),
			[{"file": "test.py", "code": "print('testing 1')"}, {"file": "lib/test3.py", "code": "print('testing 3')"}])
		result = coding_tool.run_code("python test2.py")
		self.assertEqual(result["output"], "testing 2\n")
		self.assertEqual(result["return_code"], 0)
		self.assertEqual(result["error"], "")

	def test_delete_file(self):
		coding_tool = CodingTool(self.test_folder, approve_execution = False)
		coding_tool.save_code([
			{"folder_path": "", "file_name": "test.py", "code": ""},
			{"folder_path": "", "file_name": "test2.py", "code": ""}
		])
		self.assertEqual(coding_tool.list_files(), ["test.py", "test2.py"])
		
		coding_tool.delete_files(["test2.py"])
		
		self.assertEqual(coding_tool.list_files(), ["test.py"])

	def test_list_files_ignore(self):
		coding_tool = CodingTool(self.test_folder)
		coding_tool.save_code([
			{"folder_path": "", "file_name": ".gitignore", "code": "output/*"},
			{"folder_path": "", "file_name": "test.py", "code": "print('testing')"},
			{"folder_path": "output", "file_name": "output.txt", "code": "lorem ipsum"}
		])

		files = coding_tool.list_files()

		self.assertCountEqual(files, [".gitignore", "test.py"])
