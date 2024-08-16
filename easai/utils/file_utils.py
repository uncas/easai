from fnmatch import fnmatch
from pathlib import Path

def write_text(folder : str, file : str, text : str):
	write_or_append_text(folder, file, text, "w")

def append_text(folder, file, text):
	write_or_append_text(folder, file, text, "a")

def write_or_append_text(folder, file, text, mode):
	Path(folder).mkdir(parents = True, exist_ok = True)
	f = open(folder + "/" + file, mode)
	f.write(text)
	f.close()

def ignore_file(file, patterns_to_ignore: list[str]) -> bool:
	return any(fnmatch(file, pattern_to_ignore) for pattern_to_ignore in patterns_to_ignore)
