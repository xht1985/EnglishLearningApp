import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Database

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("英语学习软件")
        self.root.geometry("800x600")
        self.db = Database()

        self.create_widgets()

    def create_widgets(self):
        # 创建标签
        tk.Label(self.root, text="问题：").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="选项A：").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.root, text="选项B：").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.root, text="选项C：").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self.root, text="选项D：").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self.root, text="答案：").grid(row=5, column=0, padx=10, pady=10)

        # 创建输入框
        self.question_entry = tk.Entry(self.root, width=50)
        self.question_entry.grid(row=0, column=1, padx=10, pady=10)
        self.option_a_entry = tk.Entry(self.root, width=50)
        self.option_a_entry.grid(row=1, column=1, padx=10, pady=10)
        self.option_b_entry = tk.Entry(self.root, width=50)
        self.option_b_entry.grid(row=2, column=1, padx=10, pady=10)
        self.option_c_entry = tk.Entry(self.root, width=50)
        self.option_c_entry.grid(row=3, column=1, padx=10, pady=10)
        self.option_d_entry = tk.Entry(self.root, width=50)
        self.option_d_entry.grid(row=4, column=1, padx=10, pady=10)
        self.answer_entry = tk.Entry(self.root, width=50)
        self.answer_entry.grid(row=5, column=1, padx=10, pady=10)

        # 创建按钮
        tk.Button(self.root, text="添加到题库", command=self.add_question).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="浏览题库", command=self.view_questions).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="随机出题", command=self.random_question).grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="错题回顾", command=self.view_wrong_questions).grid(row=9, column=0, columnspan=2, pady=10)

        # 创建文本框用于显示题目
        self.text_area = tk.Text(self.root, height=10, width=70)
        self.text_area.grid(row=10, column=0, columnspan=2, pady=10)

    def add_question(self):
        question = self.question_entry.get()
        option_a = self.option_a_entry.get()
        option_b = self.option_b_entry.get()
        option_c = self.option_c_entry.get()
        option_d = self.option_d_entry.get()
        answer = self.answer_entry.get()

        if not all([question, option_a, option_b, option_c, option_d, answer]):
            messagebox.showwarning("警告", "所有字段都必须填写！")
            return

        self.db.add_question(question, option_a, option_b, option_c, option_d, answer)
        messagebox.showinfo("成功", "题目已成功添加到题库！")
        self.clear_fields()

    def clear_fields(self):
        self.question_entry.delete(0, tk.END)
        self.option_a_entry.delete(0, tk.END)
        self.option_b_entry.delete(0, tk.END)
        self.option_c_entry.delete(0, tk.END)
        self.option_d_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)

    def view_questions(self):
        questions = self.db.get_all_questions()
        self.text_area.delete(1.0, tk.END)
        for question in questions:
            self.text_area.insert(tk.END, f"ID: {question[0]}\n")
            self.text_area.insert(tk.END, f"问题: {question[1]}\n")
            self.text_area.insert(tk.END, f"A: {question[2]}\n")
            self.text_area.insert(tk.END, f"B: {question[3]}\n")
            self.text_area.insert(tk.END, f"C: {question[4]}\n")
            self.text_area.insert(tk.END, f"D: {question[5]}\n")
            self.text_area.insert(tk.END, "-" * 40 + "\n")

    def random_question(self):
        question = self.db.get_random_question()
        if question:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"问题: {question[1]}\n")
            self.text_area.insert(tk.END, f"A: {question[2]}\n")
            self.text_area.insert(tk.END, f"B: {question[3]}\n")
            self.text_area.insert(tk.END, f"C: {question[4]}\n")
            self.text_area.insert(tk.END, f"D: {question[5]}\n")

            user_answer = simpledialog.askstring("答题", "请输入你的答案 (A/B/C/D):")
            if user_answer and user_answer.upper() == question[6]:
                messagebox.showinfo("结果", "回答正确！")
            else:
                messagebox.showinfo("结果", f"回答错误！正确答案是 {question[6]}")
                self.db.record_wrong_answer(question[0], user_answer)
        else:
            messagebox.showinfo("提示", "题库为空！")

    def view_wrong_questions(self):
        questions = self.db.get_wrong_questions()
        self.text_area.delete(1.0, tk.END)
        for question in questions:
            self.text_area.insert(tk.END, f"ID: {question[0]}\n")
            self.text_area.insert(tk.END, f"问题: {question[1]}\n")
            self.text_area.insert(tk.END, f"A: {question[2]}\n")
            self.text_area.insert(tk.END, f"B: {question[3]}\n")
            self.text_area.insert(tk.END, f"C: {question[4]}\n")
            self.text_area.insert(tk.END, f"D: {question[5]}\n")
            self.text_area.insert(tk.END, f"答案: {question[6]}\n")
            self.text_area.insert(tk.END, "-" * 40 + "\n")

    def close(self):
        self.db.close()