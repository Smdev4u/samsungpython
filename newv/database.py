import mysql.connector
from mysql.connector import Error

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
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )""")
        connection.commit()
    except Error as e:
        print("Error ensuring tables exist:", e)

# Function to seed default topics into the database
def seed_default_topics(connection):
    default_topics = {
        "À propos du projet": {
            "description": "Ce projet est conçu dans le cadre du programme Samsung Innovation Campus, qui vise à enseigner les bases de la programmation en Python aux apprenants.\nEn suivant ce programme, les participants acquerront des compétences fondamentales en programmation, qui leur permettront de comprendre et de développer des applications logicielles simples.\nIls seront initiés à des concepts de base comme les variables, les types de données, les structures de contrôle, et les fonctions.",
            "example": "print(\"Bienvenue au programme Samsung Innovation Campus!\")"
        },
        "Introduction": {
            "description": "Python est un langage de programmation polyvalent et puissant, reconnu pour sa simplicité et sa lisibilité.\nIl est idéal pour les débutants car il utilise une syntaxe claire et compréhensible qui facilite l'apprentissage.\nPython est largement utilisé dans divers domaines comme le développement web, l'analyse de données, l'intelligence artificielle et plus encore.",
            "example": "print(\"Bonjour, Python!\")\nprint(\"2 + 2 =\", 2 + 2)"
        },
        "Variables": {
            "description": "Les variables en Python sont des conteneurs qui permettent de stocker des valeurs pour les utiliser plus tard dans un programme.\nChaque variable possède un nom unique, et peut contenir des types de données différents comme des nombres, des chaînes de caractères, ou même des objets plus complexes.\nLes variables peuvent changer de valeur au cours de l'exécution du programme.",
            "example": "x = 10\ny = 20\nprint(\"x + y =\", x + y)\n\nx = 15  # Réassignation de x\nprint(\"Nouvelle valeur de x:\", x)"
        },
        "Types de Données": {
            "description": "Python supporte différents types de données pour représenter des informations.\nLes types de données les plus courants sont :\n- Entier (`int`) : Représente des nombres entiers (ex : 1, 42, -5).\n- Flottant (`float`) : Représente des nombres à virgule (ex : 3.14, -0.001).\n- Chaîne de caractères (`str`) : Représente du texte (ex : \"Bonjour\", \"Python\").\n- Booléen (`bool`) : Représente des valeurs de vérité (True ou False).\nCes types de données sont fondamentaux pour le traitement de diverses formes d’informations dans les programmes.",
            "example": "nombre = 42\ntexte = \"Bonjour\"\nbooleen = True\nprint(\"Type de nombre:\", type(nombre))\nprint(\"Type de texte:\", type(texte))\nprint(\"Type de booleen:\", type(booleen))"
        },
        "Conditions": {
            "description": "Les structures de contrôle conditionnelles permettent d'exécuter différentes instructions en fonction de critères définis.\nEn Python, les conditions sont gérées à l'aide des mots-clés `if`, `elif` (else if) et `else`, qui permettent de vérifier plusieurs cas.\nCela est particulièrement utile pour prendre des décisions dans le programme, comme vérifier l'âge d'une personne pour déterminer son statut.\n\nPrincipales opérations de conditions :\n- `if` : Vérifie si une condition est vraie et exécute le code associé.\n- `elif` : Vérifie d'autres conditions si la condition initiale est fausse.\n- `else` : Exécute le code si aucune des conditions précédentes n'est vraie.",
            "example": "age = 18\nif age < 18:\n    print(\"Mineur\")\nelif age == 18:\n    print(\"Juste majeur\")\nelse:\n    print(\"Adulte\")"
        },
        "Boucles": {
            "description": "Les boucles permettent de répéter une série d'instructions tant qu'une condition est remplie ou pour un nombre défini d'itérations.\nPython propose deux types principaux de boucles : `for` et `while`.\n\n- Boucle `for` : Utilisée pour parcourir une séquence comme une liste ou une plage de nombres, en répétant le bloc de code pour chaque élément.\n- Boucle `while` : Répète le bloc de code tant qu'une condition est vraie, très utile pour des boucles où le nombre d'itérations n'est pas déterminé à l'avance.\n\nLes boucles permettent de gérer des tâches répétitives de manière efficace, comme imprimer une séquence de nombres ou traiter des éléments d'une liste.",
            "example": "for i in range(5):\n    print(\"Itération\", i)\n\nx = 0\nwhile x < 3:\n    print(\"x est\", x)\n    x += 1"
        },
        "Fonctions": {
            "description": "Les fonctions en Python permettent de regrouper du code dans des blocs réutilisables, définis avec le mot-clé `def`.\nLes fonctions facilitent l'organisation et la modularité du code, en permettant d'éviter la répétition et d'effectuer des opérations complexes à partir de simples appels de fonction.\n\n- Définition d'une fonction : Utilisation de `def` suivi du nom de la fonction et des paramètres entre parenthèses.\n- Appel d'une fonction : Utilisation du nom de la fonction avec des valeurs pour les paramètres, si nécessaire.\n\nLes fonctions peuvent également retourner des valeurs, qui peuvent être stockées dans des variables ou utilisées dans d'autres opérations.",
            "example": "def salut(nom):\n    return f\"Bonjour, {nom}!\"\n\nprint(salut(\"Samsung\"))"
        },
        "Manipulations de Listes": {
        "description": "En Python, plusieurs structures de données permettent de stocker et de manipuler des collections d'éléments.\nLes types de collections les plus courants sont les listes, dictionnaires, tuples, et ensembles. Chaque structure a des caractéristiques et des usages spécifiques :\n\n1. Listes :\n   - Ce sont des collections ordonnées et modifiables qui peuvent contenir des éléments de n'importe quel type.\n   - Les listes sont utiles pour stocker des ensembles d'éléments susceptibles de changer, comme des listes de noms, d'objets ou de résultats.\n   - Opérations courantes :\n     - Ajouter : `append()` pour ajouter un élément à la fin de la liste.\n     - Accéder : les éléments sont accessibles par index, le premier élément ayant l'index 0.\n     - Supprimer : `remove()` ou `pop()` pour supprimer un élément.\n\n2. Dictionnaires :\n   - Ce sont des collections non ordonnées de paires clé-valeur où chaque clé est unique.\n   - Les dictionnaires sont parfaits pour des associations, par exemple pour relier un nom à une information spécifique.\n   - Opérations courantes :\n     - Ajouter ou mettre à jour : `dict[clé] = valeur`.\n     - Accéder : récupérer des valeurs via leurs clés.\n     - Supprimer : `pop(clé)` pour supprimer une paire clé-valeur.\n\n3. Tuples :\n   - Ce sont des collections ordonnées et immuables. Les éléments ne peuvent être modifiés après leur création.\n   - Les tuples sont utilisés pour des données constantes qui ne changeront pas, comme des coordonnées ou des noms de jours.\n   - Opérations courantes :\n     - Accéder : les éléments peuvent être accédés par leur index.\n     - Immuabilité : assure que les données restent inchangées après création.\n\n4. Ensembles :\n   - Ce sont des collections non ordonnées d'éléments uniques (sans doublons).\n   - Les ensembles sont utiles pour stocker des éléments uniques et pour effectuer des opérations ensemblistes comme l'union ou l'intersection.\n   - Opérations courantes :\n     - Ajouter : `add()` pour inclure un élément.\n     - Supprimer : `remove()` pour retirer un élément.\n\nCes structures de données offrent des moyens variés de gérer et d’organiser les informations en Python, en fonction des besoins spécifiques de manipulation des données.",
        
        "example": "profs = [\"Prof. Moussaoui\", \"Prof. Koujdami\", \"Prof. Labbihi\"]\nprofs.append(\"Prof. El Amrani\")  # Ajout d'un nouveau professeur\n\n# Affichage de la liste des professeurs\nfor prof in profs:\n    print(prof)\n\nprint(\"\\n-------------------------\\n\")\n\n# Dictionnaire avec les professeurs et leurs matières\nprofs_subjects_dict = {\n    \"Prof. Moussaoui\": \"Algorithmique\",\n    \"Prof. Koujdami\": \"Programmation\",\n    \"Prof. Labbihi\": \"Bases de données\",\n    \"Prof. El Amrani\": \"Intelligence Artificielle\",\n    \"Prof. Boulmalf\": \"Cybersécurité\"\n}\nprofs_subjects_dict[\"Prof. Talbi\"] = \"Réseaux\"  # Ajout d'un nouveau professeur et matière\nprint(\"Dictionnaire des professeurs et leurs matières:\")\nfor prof, subject in profs_subjects_dict.items():\n    print(f\"{prof}: {subject}\")\n\nprint(\"\\n-------------------------\\n\")\n\n# Tuple des domaines d'expertise des professeurs\nexpertise_tuple = (\"Machine Learning\", \"Développement Web\", \"Analyse de données\", \"Réseaux\", \"Sécurité Informatique\")\nprint(\"Tuple des domaines d'expertise des professeurs:\")\nfor expertise in expertise_tuple:\n    print(expertise)\n\nprint(\"\\n-------------------------\\n\")\n\n# Ensemble des compétences uniques abordées dans la formation\nskills_set = {\"Python\", \"SQL\", \"Linux\", \"Sécurité Réseau\", \"Analyse de données\"}\nskills_set.add(\"DevOps\")  # Ajout d'une compétence unique\nprint(\"Ensemble des compétences uniques abordées dans la formation:\")\nfor skill in skills_set:\n    print(skill)"
    },
    "Classes (POO)": {
        "description": "La Programmation Orientée Objet (POO) en Python permet de structurer le code en utilisant des objets et des classes.\nLes classes servent de modèle pour créer des objets et permettent d'organiser les données et les comportements associés en un seul endroit.\n\nPrincipaux concepts :\n- Classe : définit un modèle pour un objet, avec des attributs et des méthodes.\n- Objet : une instance d'une classe, représentant un élément spécifique avec des propriétés définies.\n- Attributs : des variables associées à une classe qui décrivent les propriétés de l'objet.\n- Méthodes : des fonctions associées à une classe qui définissent les comportements de l'objet.\n\nDans cet exemple, la classe `Etudiant` est utilisée pour représenter des étudiants avec leurs notes, permettant de calculer des statistiques comme la moyenne et d'attribuer des mentions.",
        
        "example": "class Etudiant:\n    def __init__(self, massar, nom, prenom):\n        self.massar = massar\n        self.nom = nom\n        self.prenom = prenom\n        self.matieres = []\n        self.moyenne = 0\n        self.min_note = float('inf')\n        self.max_note = float('-inf')\n        self.remarque = \"\"\n\n    def ajouter_matiere(self, titre, cf, note):\n        self.matieres.append({\"titre\": titre, \"cf\": cf, \"note\": note})\n\n    def calculer_statistiques(self):\n        if self.matieres:\n            total_coef = sum(m[\"cf\"] for m in self.matieres)\n            total_notes = sum(m[\"note\"] * m[\"cf\"] for m in self.matieres)\n            if total_coef > 0:\n                self.moyenne = total_notes / total_coef\n                self.min_note = min(m[\"note\"] for m in self.matieres)\n                self.max_note = max(m[\"note\"] for m in self.matieres)\n                self.remarque = self.determiner_mention()\n\n    def determiner_mention(self):\n        if self.moyenne < 10:\n            return \"Faible\"\n        elif self.moyenne < 12:\n            return \"Passable\"\n        elif self.moyenne < 14:\n            return \"Assez bien\"\n        elif self.moyenne < 16:\n            return \"Bien\"\n        elif self.moyenne < 18:\n            return \"Très bien\"\n        elif self.moyenne <= 20:\n            return \"Excellent\"\n\n    def afficher_details(self):\n        details = f\"Massar: {self.massar}\\nNom: {self.nom}\\nPrénom: {self.prenom}\\nMoyenne: {self.moyenne:.2f}\\nNote Minimum: {self.min_note}\\nNote Maximum: {self.max_note}\\nRemarque: {self.remarque}\\nMatières:\"\n        for matiere in self.matieres:\n            details += f\"\\n  - {matiere['titre']}: Note = {matiere['note']}, Coefficient = {matiere['cf']}\"\n        return details\n\netudiant1 = Etudiant(\"E001\", \"Moussaoui\", \"Said\")\netudiant2 = Etudiant(\"E002\", \"Koujdami\", \"Yassine\")\netudiant3 = Etudiant(\"E003\", \"Labbihi\", \"Ismayl\")\n\netudiant1.ajouter_matiere(\"Math\", 2, 15)\netudiant1.ajouter_matiere(\"Physique\", 3, 17)\netudiant1.calculer_statistiques()\n\netudiant2.ajouter_matiere(\"Informatique\", 4, 12)\netudiant2.ajouter_matiere(\"Chimie\", 2, 11)\netudiant2.calculer_statistiques()\n\netudiant3.ajouter_matiere(\"Biologie\", 3, 10)\netudiant3.ajouter_matiere(\"Histoire\", 2, 14)\netudiant3.calculer_statistiques()\n\nprint(\"Détails de l'Étudiant 1:\\n\", etudiant1.afficher_details())\nprint(\"\\nDétails de l'Étudiant 2:\\n\", etudiant2.afficher_details())\nprint(\"\\nDétails de l'Étudiant 3:\\n\", etudiant3.afficher_details())"
    },
"GUI avec Tkinter": {
        "description": "Tkinter est une bibliothèque standard de Python utilisée pour créer des interfaces graphiques (GUI).\nElle permet de créer des fenêtres interactives avec des widgets tels que des boutons, des champs de saisie, des cases à cocher, et bien plus encore.\n\nDans cet exemple, nous allons construire une interface utilisateur avec plusieurs widgets pour démontrer les fonctionnalités de base de Tkinter, tout en intégrant une image de fond pour un design plus attrayant.\n\nExplication des widgets utilisés :\n- Label : Utilisé pour afficher du texte ou des images dans la fenêtre.\n- Entry : Un champ de saisie pour entrer du texte sur une seule ligne.\n- Text : Une zone de texte multi-ligne pour des entrées plus longues.\n- Checkbox : Permet à l'utilisateur de sélectionner ou de désélectionner une option.\n- Radio Button : Utilisé pour des options exclusives, où une seule peut être sélectionnée.\n- OptionMenu : Un menu déroulant qui permet de sélectionner une option parmi plusieurs.\n- Button : Un bouton cliquable qui peut déclencher une fonction spécifique.\n\nExplication de l'intégration de l'image de fond :\nL'image de fond (par exemple un logo Samsung) est chargée au début et placée comme arrière-plan en utilisant un `Label`. Il est important de s'assurer que l'image est disponible dans le répertoire de travail ou de spécifier son chemin complet.\n\nLe code ci-dessous illustre l'utilisation de ces widgets dans une interface avec une image de fond et des couleurs personnalisées pour améliorer l'expérience visuelle.",
        
        "example": "import tkinter as tk\nfrom tkinter import messagebox\nfrom tkinter import PhotoImage\n\nfenetre = tk.Tk()\nfenetre.title(\"Interface avec Tkinter\")\nfenetre.geometry(\"700x500\")\n\ntry:\n    bg_image = PhotoImage(file=\"samsung_logo.png\")\n    bg_label = tk.Label(fenetre, image=bg_image)\n    bg_label.place(relwidth=1, relheight=1)\nexcept:\n    print(\"L'image de fond n'a pas pu être chargée. Assurez-vous que 'samsung_logo.png' est dans le même répertoire.\")\n\n\ndef afficher_message():\n    messagebox.showinfo(\"Information\", \"Bouton Cliqué!\")\n\nlabel = tk.Label(fenetre, text=\"Bienvenue dans le programme Samsung Innovation Campus!\", font=(\"Arial\", 14), bg=\"#FFFFFF\", relief=tk.SOLID)\nlabel.pack(pady=10)\n\nentry_label = tk.Label(fenetre, text=\"Entrez votre nom:\", font=(\"Arial\", 12), bg=\"#FFFFFF\")\nentry_label.pack(pady=5)\nentry = tk.Entry(fenetre, width=30)\nentry.pack(pady=5)\n\ntext_label = tk.Label(fenetre, text=\"Entrez un commentaire:\", font=(\"Arial\", 12), bg=\"#FFFFFF\")\ntext_label.pack(pady=5)\ntext_box = tk.Text(fenetre, height=5, width=30)\ntext_box.pack(pady=5)\n\ncheckbox_var = tk.BooleanVar()\ncheckbox = tk.Checkbutton(fenetre, text=\"Accepter les termes et conditions\", variable=checkbox_var, bg=\"#FFFFFF\")\ncheckbox.pack(pady=5)\n\nradio_var = tk.StringVar(value=\"Option1\")\nradio1 = tk.Radiobutton(fenetre, text=\"Option 1\", variable=radio_var, value=\"Option1\", bg=\"#FFFFFF\")\nradio2 = tk.Radiobutton(fenetre, text=\"Option 2\", variable=radio_var, value=\"Option2\", bg=\"#FFFFFF\")\nradio1.pack(pady=2)\nradio2.pack(pady=2)\n\noptions = [\"Python\", \"Java\", \"C++\", \"JavaScript\"]\nselected_option = tk.StringVar(value=options[0])\ndropdown = tk.OptionMenu(fenetre, selected_option, *options)\ndropdown.config(bg=\"#FFFFFF\")\ndropdown.pack(pady=10)\n\nbutton = tk.Button(fenetre, text=\"Cliquer ici\", command=afficher_message, bg=\"#0048BA\", fg=\"#FFFFFF\")\nbutton.pack(pady=20)\n\nfenetre.mainloop()"
    }
    }

    try:
        cursor = connection.cursor()
        for name, content in default_topics.items():
            cursor.execute(
                "INSERT INTO topics (name, description, example) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE description=VALUES(description), example=VALUES(example)",
                (name, content["description"], content["example"])
            )
        connection.commit()
    except Error as e:
        print("Error seeding default topics:", e)
