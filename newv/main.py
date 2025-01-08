import tkinter as tk
from tkinter import scrolledtext
from database import create_connection, ensure_tables_exist, seed_default_topics
from models import TopicsManager, QuizManager
from configWindow import ConfigWindow
import sys
import io
import webbrowser

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

        footer_content = tk.Frame(footer, bg="#0080FF")
        footer_content.pack(anchor="center")

        footer_text_label = tk.Label(footer_content, text="Created by ", bg="#0080FF", fg="white", font=("Arial", 10, "italic"))
        footer_text_label.pack(side=tk.LEFT, padx=5)

        creators = {
            "SMDEV": "https://github.com/SMDEV4U",
            "KYDEV": "https://github.com/KYASSDEV",
            "LIDEV": "https://github.com/LABBIHI"
        }

        for name, link in creators.items():
            link_label = tk.Label(footer_content, text=name, bg="#0080FF", fg="white", font=("Arial", 10, "italic", "underline"), cursor="hand2")
            link_label.pack(side=tk.LEFT, padx=5)
            link_label.bind("<Button-1>", lambda e, url=link: self.open_github(url))

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
        seed_default_topics(connection)

        topics_manager = TopicsManager(connection)
        quiz_manager = QuizManager(connection)
        root = tk.Tk()
        app = App(root, topics_manager, quiz_manager)
        root.mainloop()
        connection.close()
