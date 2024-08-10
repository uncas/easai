def fetch_json_key_value(file_name, key, defaultValue = None):
	import json
	import os.path
	if not os.path.isfile(file_name):
		return defaultValue
	with open(file_name) as settingsFile:
		settings = json.load(settingsFile)
		return settings.get(key, defaultValue)
