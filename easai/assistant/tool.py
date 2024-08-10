from typing import Callable

class AssistantToolParameter:
	def __init__(self, name: str, description: str, type: str = "string", enum: list[str] = None):
		self.name = name
		self.description = description
		self.type = type
		self.enum = enum
	
	def get_open_ai_tool_properties(self) -> dict:
		value = {
			"type": self.type,
			"description": self.description
		}
		if self.enum:
			value["enum"] = self.enum
		return value

class AssistantTool:
	def __init__(self, method: Callable, description: str, parameters: list[AssistantToolParameter] = [], name: str = None):
		self.parameters: list[AssistantToolParameter] = parameters
		self.description = description
		self.method: Callable = method
		self.name = name if name else method.__name__
	
	def map_to_open_ai_tool(self) -> dict:
		properties = {}
		for parameter in self.parameters:
			properties[parameter.name] = parameter.get_open_ai_tool_properties()
		return {
			"type": "function",
			"function": {
				"name": self.name,
				"description": self.description,
				"parameters": {
					"type": "object",
					"properties": properties
				}
			}
		}

def create_tool_from_method(method: Callable) -> AssistantTool:
	method_documentation = method.__doc__
	description = method_documentation.split("\n")[0] if method_documentation else method.__name__
	parameter_docs = method_documentation.split("\n")[1:] if method_documentation else []
	method_parameters = method.__code__.co_varnames

	def get_parameter_description(parameter_name: str) -> tuple:
		for parameter_doc in parameter_docs:
			if parameter_name in parameter_doc:
				parameter_description = parameter_doc.split(":")[1].strip()
				parameter_type = "integer" if "(int)" in parameter_doc else "string"
				return parameter_name, parameter_description, parameter_type
		return parameter_name, parameter_name, "string"

	parameter_descriptions = [get_parameter_description(name) for name in method_parameters if name != "self"]
	parameters = [AssistantToolParameter(
		name = parameter_description[0], description = parameter_description[1], type = parameter_description[2]) for parameter_description in parameter_descriptions]
	return AssistantTool(
		method = method,
		description = description,
		parameters = parameters
	)
