import unittest

from src.easai.utils.local_cache import LocalCache

class AssistantUnitTests(unittest.TestCase):

	def test_getOrAdd(self):
		import uuid
		cache = LocalCache("output/LocalCacheTest.db")
		key = "test-" + str(uuid.uuid4())
		class mock:
			def __init__(self):
				self.wasCalled = False
			def getValue(self):
				self.wasCalled = True
				return "42"
		
		myMock = mock()
		value = cache.get_or_add(key, myMock.getValue)
		self.assertEqual(value, "42")
		self.assertEqual(myMock.wasCalled, True)
		myMock = mock()
		value = cache.get_or_add(key, myMock.getValue)
		self.assertEqual(value, "42")
		self.assertEqual(myMock.wasCalled, False)

	def test_getOrAddWithLifetime(self):
		import time
		import uuid
		cache = LocalCache("output/LocalCacheTest.db")
		key = "test-" + str(uuid.uuid4())
		value = cache.get_or_add_with_lifetime(key, lambda: "1", 0.5)
		self.assertEqual(value, "1")
		value = cache.get_or_add_with_lifetime(key, lambda: "2", 0.5)
		self.assertEqual(value, "1")
		time.sleep(1)
		value = cache.get_or_add_with_lifetime(key, lambda: "2", 0.5)
		self.assertEqual(value, "2")
