import datetime
import logging
import unittest

from easai.utils.sqlite_logging_handler import SQLiteLoggingHandler

class SQLiteLoggingHandlerTests(unittest.TestCase):
	def test_logger(self):
		sqlite_handler = SQLiteLoggingHandler(db = "output/log.db")
		sqlite_handler.setLevel(logging.DEBUG)
		logger = logging.getLogger()
		logger.addHandler(sqlite_handler)
		log_message = "testing: " + str(datetime.datetime.now())

		logger.error(log_message)

		last = sqlite_handler.get_last_message()
		self.assertEqual(last[0], log_message)
