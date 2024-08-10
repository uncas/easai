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
	def __init__(self, method, description: str, parameters: list[AssistantToolParameter] = [], name: str = None):
		self.parameters: list[AssistantToolParameter] = parameters
		self.description = description
		self.method = method
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