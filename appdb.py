import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
import sys
import io
import webbrowser
import json

# Ensure tkinter is installed
try:
    import tkinter
except ModuleNotFoundError:
    print("Error: tkinter is not available. Please ensure it is installed.")
    sys.exit(1)

# Database connection setup
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="pylearningdb"
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS pylearningdb")
        connection.database = "pylearningdb"
        return connection
    except Error as e:
        print("Database Error:", e)
        sys.exit(1)

# Function to ensure tables exist
def ensure_tables_exist(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            example TEXT NOT NULL
        )""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_content (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            answer VARCHAR(255) NOT NULL
        )""")
        connection.commit()
    except Error as e:
        print("Error ensuring tables exist:", e)

# Class to manage topics from the database
class TopicsManager:
    def __init__(self, connection):
        self.connection = connection
        self.topics = self.load_topics()

    def load_topics(self):
        topics = {}
        if self.connection:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM topics")
            rows = cursor.fetchall()
            for row in rows:
                topics[row['name']] = {
                    "description": row['description'],
                    "example": row['example']
                }
            cursor.close()
        return topics

    def get_topic(self, topic_name):
        return self.topics.get(topic_name, {"description": "Topic not found", "example": ""})

# Class to manage quiz content from the database
class QuizManager:
    def __init__(self, connection):
        self.connection = connection
        self.quiz_content = self.load_quiz_content()

    def load_quiz_content(self):
        quiz_content = []
        if self.connection:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM quiz_content")
            rows = cursor.fetchall()
            for row in rows:
                quiz_content.append({
                    "question": row['question'],
                    "options": json.loads(row['options']),
                    "answer": row['answer']
                })
            cursor.close()
        return quiz_content

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

# Main application class
class App:
    def __init__(self, root, topics_manager, quiz_manager):
        self.root = root
        self.root.title("Samsung Innovation Campus - Apprentissage Python")
        self.root.geometry("1100x670")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.topics_manager = topics_manager
        self.quiz_manager = quiz_manager
        self.quiz_content = quiz_manager.quiz_content
        self.user_answers = [""] * len(self.quiz_content)
        self.quiz_index = 0
        self.option_var = tk.StringVar(value="")
        self.create_widgets()
        first_topic = next(iter(self.topics_manager.topics)) if self.topics_manager.topics else None
        if first_topic:
            self.load_topic(first_topic)

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#0080FF", height=60)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_label = tk.Label(header, text="Samsung Innovation Campus - Apprentissage Python", bg="#0080FF", fg="white", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        nav_frame = tk.Frame(self.root, bg="lightgrey", width=150)
        nav_frame.grid(row=1, column=0, sticky="ns")
        self.create_nav_buttons(nav_frame)

        self.content_frame = tk.Frame(self.root, padx=10, pady=10)
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.description_text = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, height=8, font=("Arial", 12), padx=10, pady=10, bg="#f0f0f0")
        self.description_text.grid(row=1, column=0, sticky="nsew", pady=5)
        self.code_text = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, height=8, font=("Consolas", 12), padx=10, pady=10)
        self.code_text.grid(row=3, column=0, sticky="nsew", pady=5)
        self.run_button = tk.Button(self.content_frame, text="Exécuter l'Exemple", font=("Arial", 12), command=lambda: self.run_example(self.code_text.get(1.0, tk.END)))
        self.run_button.grid(row=4, column=0, pady=10)

        # Footer setup, fixed at the bottom
        footer = tk.Frame(self.root, bg="#0080FF", height=30)
        footer.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Frame to hold both the "Created by" text and the creator links in the center
        footer_content = tk.Frame(footer, bg="#0080FF")
        footer_content.pack(anchor="center")

        # "Created by" text
        footer_text_label = tk.Label(footer_content, text="Created by ", bg="#0080FF", fg="white", font=("Arial", 10, "italic"))
        footer_text_label.pack(side=tk.LEFT, padx=5)

        # Creators dictionary with GitHub links
        creators = {
            "SMDEV": "https://github.com/SMDEV4U",
            "KYDEV": "https://github.com/KYASSDEV",
            "LIDEV": "https://github.com/LABBIHI"
        }

        # Create clickable labels for each creator
        for name, link in creators.items():
            link_label = tk.Label(footer_content, text=name, bg="#0080FF", fg="white", font=("Arial", 10, "italic", "underline"), cursor="hand2")
            link_label.pack(side=tk.LEFT, padx=5)
            link_label.bind("<Button-1>", lambda e, url=link: self.open_github(url))

        # Config Button to open ConfigWindow
        self.config_button = tk.Button(nav_frame, text="Config", font=("Arial", 12, "bold"), bg="#FF8000", fg="white", command=lambda: ConfigWindow(self.root, self.topics_manager.connection))
        self.config_button.pack(fill=tk.X, pady=5)

    def create_nav_buttons(self, nav_frame):
        button_style = {"font": ("Arial", 12, "bold"), "bg": "#0080FF", "fg": "white", "bd": 0, "relief": tk.FLAT}
        for topic in self.topics_manager.topics.keys():
            tk.Button(nav_frame, text=topic, command=lambda t=topic: self.load_topic(t), **button_style).pack(fill=tk.X, pady=2)

    def load_topic(self, topic_name):
        topic = self.topics_manager.get_topic(topic_name)
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, topic["description"])
        self.description_text.config(state=tk.DISABLED)
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, topic["example"])

    def run_example(self, code):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            exec(code, {})
            output = new_stdout.getvalue()
        except Exception as e:
            output = f"Erreur : {str(e)}"
        sys.stdout = old_stdout
        self.show_output(output)

    def show_output(self, output):
        output_window = tk.Toplevel(self.root)
        output_window.title("Output")
        output_text = scrolledtext.ScrolledText(output_window, wrap=tk.WORD, font=("Arial", 12), padx=10, pady=10)
        output_text.pack(fill=tk.BOTH, expand=True)
        output_text.insert(tk.END, output)
        output_text.config(state=tk.DISABLED)

    def open_github(self, url):
        webbrowser.open_new(url)

# Main execution
if __name__ == "__main__":
    connection = create_connection()
    if connection:
        ensure_tables_exist(connection)
        topics_manager = TopicsManager(connection)
        quiz_manager = QuizManager(connection)
        root = tk.Tk()
        app = App(root, topics_manager, quiz_manager)
        root.mainloop()
        connection.close()
