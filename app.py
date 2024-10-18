import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import sys
import io
import os

# Obtenez le répertoire du fichier exécutable
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
# Chemin vers les fichiers JSON
filepath = os.path.join(BASE_DIR, 'topics.json')
quizpath = os.path.join(BASE_DIR, 'quiz_content.json')



class TopicsManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.topics = self.load_topics()

    def load_topics(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier de sujets est introuvable.")
            return {}

    def get_topic(self, topic_name):
        return self.topics.get(topic_name, {"description": "Topic not found", "example": ""})

class App:
    def __init__(self, root, topics_manager):
        self.root = root
        self.root.title("Samsung Innovation Campus - Apprentissage Python")
        self.root.geometry("1100x670")
        self.root.rowconfigure(1, weight=1)  
        self.root.columnconfigure(1, weight=1)
        self.quiz_content = self.load_quiz_content(quizpath)
        self.user_answers = [""] * len(self.quiz_content)
        self.quiz_index = 0
        self.option_var = tk.StringVar(value="")
        self.topics_manager = topics_manager
        
        self.create_widgets()
        # Automatically load the first topic on startup
        first_topic = next(iter(self.topics_manager.topics))  # Get the first topic name
        self.load_topic(first_topic)  # Display the first topic content
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#0080FF", height=60)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_label = tk.Label(header, text="Samsung Innovation Campus - Apprentissage Python", bg="#0080FF", fg="white", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Navigation Menu
        nav_frame = tk.Frame(self.root, bg="lightgrey", width=150)
        nav_frame.grid(row=1, column=0, sticky="ns")
        self.create_nav_buttons(nav_frame)
        
        # Content Frame for Topics
        self.content_frame = tk.Frame(self.root, padx=10, pady=10)
        self.content_frame.grid(row=1, column=1, sticky="nsew")

        self.description_text = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, height=8, font=("Arial", 12), padx=10, pady=10, bg="#f0f0f0")
        self.description_text.grid(row=1, column=0, sticky="nsew", pady=5)
        self.code_text = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, height=8, font=("Consolas", 12), padx=10, pady=10)
        self.code_text.grid(row=3, column=0, sticky="nsew", pady=5)
        self.output_text = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, height=6, font=("Arial", 12), padx=10, pady=10, bg="#f0f0f0")
        self.output_text.grid(row=5, column=0, sticky="nsew", pady=5)
        self.run_button = tk.Button(self.content_frame, text="Exécuter l'Exemple", font=("Arial", 12), command=lambda: self.run_example(self.code_text.get(1.0, tk.END)))
        self.run_button.grid(row=6, column=0, pady=10)
        
        # Quiz Frame for Quiz Content
        self.quiz_frame = tk.Frame(self.root, padx=10, pady=10)
        self.quiz_frame.grid(row=1, column=1, sticky="nsew")
        self.quiz_frame.columnconfigure(0, weight=1)
        self.quiz_frame.columnconfigure(2, weight=1)

        # Display Question Label, aligned with Previous button
        self.question_label = tk.Label(self.quiz_frame, text="", font=("Arial", 14, "bold"), anchor="w")
        self.question_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="w")
        # Radio buttons for quiz options
        self.quiz_options = []
        for i in range(4):
            radio_button = tk.Radiobutton(
                self.quiz_frame, 
                variable=self.option_var, 
                value=f"option_{i}",  # Assign a unique value to each option
                font=("Arial", 12), 
                anchor="w"
            )
            radio_button.grid(row=i+1, column=0, columnspan=3, sticky="w")
            self.quiz_options.append(radio_button)

        # Navigation Buttons (aligned with Previous button)
        button_frame = tk.Frame(self.quiz_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")
        self.prev_button = tk.Button(button_frame, text="Précédent", command=self.prev_question)
        self.next_button = tk.Button(button_frame, text="Suivant", command=self.next_question)
        self.submit_button = tk.Button(button_frame, text="Valider", command=self.submit_quiz)
        
        self.prev_button.pack(side=tk.LEFT, padx=10)
        self.next_button.pack(side=tk.RIGHT, padx=10)
        self.submit_button.pack(side=tk.RIGHT, padx=10)
        self.submit_button.pack_forget()

        # Footer setup, fixed at the bottom
        footer = tk.Frame(self.root, bg="#0080FF", height=30)
        footer.grid(row=2, column=0, columnspan=2, sticky="ew")
        footer_label = tk.Label(footer, text="Created By SMDEV & KYDEV & ", bg="#0080FF", fg="white", font=("Arial", 10, "italic"))
        footer_label.pack(pady=5)

    def load_quiz_content(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier de quiz est introuvable.")
            return []

    def display_question(self, index):
        question_data = self.quiz_content[index]
        self.question_label.config(text=question_data["question"])
        self.option_var.set(None)  # Clear any pre-selected option
        for i, option in enumerate(question_data["options"]):
            self.quiz_options[i].config(text=option, value=option)

        # Control button visibility
        if self.quiz_index == len(self.quiz_content) - 1:  # Last question
            self.next_button.pack_forget()
            self.submit_button.pack(side=tk.RIGHT, padx=10)
        else:
            self.submit_button.pack_forget()
            self.next_button.pack(side=tk.RIGHT, padx=10)
        self.prev_button.config(state="normal" if self.quiz_index > 0 else "disabled")

    def next_question(self):
        self.user_answers[self.quiz_index] = self.option_var.get()
        if self.quiz_index < len(self.quiz_content) - 1:
            self.quiz_index += 1
            self.display_question(self.quiz_index)

    def prev_question(self):
        self.user_answers[self.quiz_index] = self.option_var.get()
        if self.quiz_index > 0:
            self.quiz_index -= 1
            self.display_question(self.quiz_index)

    def submit_quiz(self):
        score = sum(1 for i, q in enumerate(self.quiz_content) if self.user_answers[i] == q["answer"])
        messagebox.showinfo("Resultat", f"Votre score : {score} / {len(self.quiz_content)}")
    
    def create_nav_buttons(self, nav_frame):
        button_style = {"font": ("Arial", 12, "bold"), "bg": "#0080FF", "fg": "white", "bd": 0, "relief": tk.FLAT}
        for topic in self.topics_manager.topics.keys():
            tk.Button(nav_frame, text=topic, command=lambda t=topic: self.load_topic(t), **button_style).pack(fill=tk.X, pady=2)
        tk.Button(nav_frame, text="Python Quiz", command=self.load_quiz, **button_style).pack(fill=tk.X, pady=2)

    def load_topic(self, topic_name):
        self.quiz_frame.grid_forget()
        self.content_frame.grid(row=1, column=1, sticky="nsew")

        topic = self.topics_manager.get_topic(topic_name)
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, topic["description"])
        self.description_text.config(state=tk.DISABLED)
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, topic["example"])
        self.output_text.delete(1.0, tk.END)

    def load_quiz(self):
        self.content_frame.grid_forget()
        self.quiz_frame.grid(row=1, column=1, sticky="nsew")
        self.display_question(self.quiz_index)

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
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)
        self.output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    topics_manager = TopicsManager(filepath)
    root = tk.Tk()
    app = App(root, topics_manager)
    root.mainloop()
