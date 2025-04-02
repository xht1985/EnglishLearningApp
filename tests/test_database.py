# test_database.py
import unittest
from src.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("test_english_learning.db")
        self.db.cursor.execute("DELETE FROM questions")  # 清空测试数据库
        self.db.conn.commit()

    def tearDown(self):
        self.db.close()

    def test_add_question(self):
        self.db.add_question("What is the capital of France?", "Paris", "London", "Berlin", "Madrid", "Paris")
        self.db.cursor.execute("SELECT * FROM questions")
        result = self.db.cursor.fetchall()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "What is the capital of France?")

if __name__ == "__main__":
    unittest.main()