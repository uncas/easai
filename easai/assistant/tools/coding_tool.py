import os
import subprocess
from pathlib import Path

from easai.assistant.tool import AssistantTool, AssistantToolParameter
from easai.utils.file_utils import write_text

class CodingTool:
	def __init__(self, root_path: str, name: str = "Coding Tool", approve_execution: bool = False):
		self.root_path = root_path
		self.name = name
		self.approve_execution = approve_execution

	def save_code(self, code_files: list[dict[str, str]]):
		for code_file in code_files:
			code: str = code_file["code"]
			folder_path: str = code_file["folder_path"]
			file_name: str = code_file["file_name"]
			full_folder_path = os.path.join(self.root_path, folder_path)
			write_text(full_folder_path, file_name, code)

	def list_files(self) -> list[str]:
		result = list(Path(self.root_path).rglob("*"))
		return [str(path.relative_to(self.root_path)) for path in result if path.is_file()]

	def read_code(self, files: list[str]) -> list[dict[str, str]]:
		codes = []
		for file in files:
			file_path = os.path.join(self.root_path, file)
			with open(file_path, "r") as file_stream:
				code = file_stream.read()
				codes.append({"file": file, "code": code})
		return codes

	def run_code(self, command_line: str) -> str:
		if self.approve_execution:
			confirmation = input(f"Are you sure you want to run the command '{command_line}' in '{self.root_path}'? (y/n) ")
			if confirmation.lower() != "y":
				return

		result = subprocess.run(command_line, cwd = self.root_path, 
			shell = True, stderr = subprocess.PIPE, stdout = subprocess.PIPE)
		return {
			"output": result.stdout.decode("utf-8"), 
			"error": result.stderr.decode("utf-8"), 
			"return_code": result.returncode
		}

	def save_code_tool(self) -> AssistantTool:
		parameter_value = {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"folder_path": { "type": "string" },
					"file_name": { "type": "string" },
					"code": { "type": "string" }
				}
			}
		}
		
		return AssistantTool(self.save_code, "Save code", [
			AssistantToolParameter("code_files", "The files with the code", value = parameter_value)
		])

	def list_files_tool(self) -> AssistantTool:
		return AssistantTool(self.list_files, "List all files in the code base")

	def read_code_tool(self) -> AssistantTool:
		parameter = AssistantToolParameter(
			name = "files", 
			value = {
				"type": "array"
			}
		)
		return AssistantTool(self.read_code, "Read code", parameters = [parameter])

	def run_code_tool(self) -> AssistantTool:
		return AssistantTool(self.run_code, "Run code", [
			AssistantToolParameter("command_line", "The command-line command that runs the code")
		])
