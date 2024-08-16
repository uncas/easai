import unittest

from easai.utils.file_utils import ignore_file

class FileUtilsUnitTests(unittest.TestCase):

	def test_ignore_file(self):
		patterns_to_ignore = ["output/*"]
		self.assertFalse(ignore_file("hello_world", patterns_to_ignore))
		self.assertFalse(ignore_file("outpat/hello_world", patterns_to_ignore))
		self.assertTrue(ignore_file("output/hello_world", patterns_to_ignore))
