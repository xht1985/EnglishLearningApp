import sqlite3
import random

class Database:
    def __init__(self, db_name="english_learning.db"):
        self.conn = sqlite3.connect(f"../data/{db_name}")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS wrong_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                user_answer TEXT NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        """)
        self.conn.commit()

    def add_question(self, question, option_a, option_b, option_c, option_d, answer):
        self.cursor.execute("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (question, option_a, option_b, option_c, option_d, answer))
        self.conn.commit()

    def get_all_questions(self):
        self.cursor.execute("SELECT * FROM questions")
        return self.cursor.fetchall()

    def get_question_by_id(self, question_id):
        self.cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        return self.cursor.fetchone()

    def update_question(self, question_id, question, option_a, option_b, option_c, option_d, answer):
        self.cursor.execute("""
            UPDATE questions
            SET question = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?, answer = ?
            WHERE id = ?
        """, (question, option_a, option_b, option_c, option_d, answer, question_id))
        self.conn.commit()

    def delete_question(self, question_id):
        self.cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        self.cursor.execute("DELETE FROM wrong_answers WHERE question_id = ?", (question_id,))
        self.conn.commit()

    def get_random_question(self):
        self.cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
        return self.cursor.fetchone()

    def record_wrong_answer(self, question_id, user_answer):
        self.cursor.execute("""
            INSERT INTO wrong_answers (question_id, user_answer)
            VALUES (?, ?)
        """, (question_id, user_answer))
        self.conn.commit()

    def get_wrong_questions(self):
        self.cursor.execute("""
            SELECT q.id, q.question, q.option_a, q.option_b, q.option_c, q.option_d, q.answer
            FROM questions q
            JOIN wrong_answers wa ON q.id = wa.question_id
            GROUP BY q.id
        """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()