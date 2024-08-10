class LocalCache:
	def __init__(self, cache_db_path = "output/local_cache.db"):
		import sqlite3
		self.db = sqlite3.connect(cache_db_path)

	def get_or_add(self, key, getValue):
		self.db.execute("CREATE TABLE IF NOT EXISTS Cache (key TEXT PRIMARY KEY, value TEXT)")
		existing_value = self.db.execute("SELECT value FROM Cache WHERE key = ?", (key,)).fetchone()
		if existing_value:
			return existing_value[0]
		
		value = getValue()
		self.db.execute("INSERT OR REPLACE INTO Cache (key, value) VALUES (?, ?)", (key, value))
		self.db.commit()
		return value
	
	def get_or_add_with_lifetime(self, key, getValue, lifetimeSeconds):
		import json, time
		now_timestamp = time.time()
		must_be_created_after_timestamp = now_timestamp - lifetimeSeconds
		self.db.execute("CREATE TABLE IF NOT EXISTS CacheWithLifetime (Key TEXT PRIMARY KEY, Value TEXT, Timestamp INTEGER)")
		existing_value = self.db.execute("SELECT Value FROM CacheWithLifetime WHERE Key = ? AND Timestamp > ?", (key,must_be_created_after_timestamp,)).fetchone()
		if existing_value:
			return json.loads(existing_value[0])
		
		value = getValue()
		self.db.execute(
			"INSERT OR REPLACE INTO CacheWithLifetime (Key, Value, Timestamp) VALUES (?, ?, ?)",
			(key, json.dumps(value), now_timestamp))
		self.db.commit()
		return value
