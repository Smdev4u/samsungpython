import tkinter as tk
from tkinter import scrolledtext, messagebox
import json

# Configuration Management Interface
class ConfigWindow:
    def __init__(self, parent, connection):
        self.window = tk.Toplevel(parent)
        self.window.title("Configuration Management")
        self.window.geometry("600x400")
        self.connection = connection
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for topic name
        tk.Label(self.window, text="Topic Name:").grid(row=0, column=0, padx=10, pady=10)
        self.topic_name_entry = tk.Entry(self.window, width=40)
        self.topic_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Label and Text for description
        tk.Label(self.window, text="Description:").grid(row=1, column=0, padx=10, pady=10)
        self.description_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=40, height=5)
        self.description_text.grid(row=1, column=1, padx=10, pady=10)

        # Label and Text for example
        tk.Label(self.window, text="Example:").grid(row=2, column=0, padx=10, pady=10)
        self.example_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=40, height=5)
        self.example_text.grid(row=2, column=1, padx=10, pady=10)

        # Buttons for adding topics
        self.add_topic_button = tk.Button(self.window, text="Add Topic", command=self.add_topic)
        self.add_topic_button.grid(row=3, column=1, sticky="e", padx=10, pady=10)

        # Label and Entry for quiz question
        tk.Label(self.window, text="Quiz Question:").grid(row=4, column=0, padx=10, pady=10)
        self.quiz_question_entry = tk.Entry(self.window, width=40)
        self.quiz_question_entry.grid(row=4, column=1, padx=10, pady=10)

        # Label and Entry for quiz options
        tk.Label(self.window, text="Quiz Options (comma separated):").grid(row=5, column=0, padx=10, pady=10)
        self.quiz_options_entry = tk.Entry(self.window, width=40)
        self.quiz_options_entry.grid(row=5, column=1, padx=10, pady=10)

        # Label and Entry for quiz answer
        tk.Label(self.window, text="Quiz Answer:").grid(row=6, column=0, padx=10, pady=10)
        self.quiz_answer_entry = tk.Entry(self.window, width=40)
        self.quiz_answer_entry.grid(row=6, column=1, padx=10, pady=10)

        # Buttons for adding quiz question
        self.add_quiz_button = tk.Button(self.window, text="Add Quiz Question", command=self.add_quiz_question)
        self.add_quiz_button.grid(row=7, column=1, sticky="e", padx=10, pady=10)

    def add_topic(self):
        topic_name = self.topic_name_entry.get()
        description = self.description_text.get(1.0, tk.END).strip()
        example = self.example_text.get(1.0, tk.END).strip()

        if topic_name and description and example:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO topics (name, description, example) VALUES (%s, %s, %s)", (topic_name, description, example))
            self.connection.commit()
            messagebox.showinfo("Success", "Topic added successfully!")
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def add_quiz_question(self):
        question = self.quiz_question_entry.get()
        options = self.quiz_options_entry.get()
        answer = self.quiz_answer_entry.get()

        if question and options and answer:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO quiz_content (question, options, answer) VALUES (%s, %s, %s)", (question, json.dumps(options.split(",")), answer))
            self.connection.commit()
            messagebox.showinfo("Success", "Quiz question added successfully!")
        else:
            messagebox.showerror("Error", "All fields must be filled!")
