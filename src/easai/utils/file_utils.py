def write_text(folder : str, file : str, text : str):
	write_or_append_text(folder, file, text, "w")

def append_text(folder, file, text):
	write_or_append_text(folder, file, text, "a")

def write_or_append_text(folder, file, text, mode):
	from pathlib import Path
	Path(folder).mkdir(parents = True, exist_ok = True)
	f = open(folder + "/" + file, mode)
	f.write(text)
	f.close()

def get_file_path(pathRelativeToSourceFolder):
	import os
	thisPath = os.path.realpath(__file__)
	sourcePath = os.path.join(os.path.dirname(thisPath), "..")
	return os.path.join(sourcePath, pathRelativeToSourceFolder)
