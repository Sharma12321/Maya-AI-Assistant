import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('maya_interactions.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             command TEXT,
             response TEXT,
             timestamp DATETIME)
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             preference_name TEXT UNIQUE,
             preference_value TEXT)
        ''')
        self.conn.commit()

    def log_interaction(self, command, response):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO interactions (command, response, timestamp) VALUES (?, ?, ?)",
                       (command, response, timestamp))
        self.conn.commit()

    def get_recent_interactions(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM interactions ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

    def set_preference(self, name, value):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO user_preferences (preference_name, preference_value) VALUES (?, ?)",
                       (name, value))
        self.conn.commit()

    def get_preference(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT preference_value FROM user_preferences WHERE preference_name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()