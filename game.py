import tkinter as tk
import random

class QuestionGame:
    def __init__(self, questions_file='questions.txt'):
        # Main window setup
        self.root = tk.Tk()
        self.root.title(f"Sprint Retro Game")
        self.root.geometry("400x500")
        self.root.resizable(False,False)
        self.root.attributes(alpha=0.95)

        # Game Parameter
        self.questions = self._load_questions(questions_file)

        # Create UI elements
        self._create_title_buttons()

    def _load_questions(self, filename):
        """Load Questions from file into a dictionary."""
        questions = {}
        current_title = ''

        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#'):
                    current_title = line[1:].strip()
                    questions[current_title] = []
                elif line.startswith('-'):
                    questions[current_title].append(line[1:].strip())
        
        return questions
    
    def _create_welcome_label(self):
        """Cleanup and create welcome label."""
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Root grid config
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Display welcome message
        welcome_label = tk.Label(
            self.root,
            text=f"Hey there, team!",
            font=('San Francisco', 16, 'bold')
        )
        welcome_label.grid(row=0, column=0, pady=10, sticky='ew')
    
    def _create_title_buttons(self):
        """Create buttons for each question category."""
        # Cleanup and recreate welcome label
        self._create_welcome_label()

        # Create buttons for each title
        for idx, title in enumerate(self.questions.keys(), start=1):
            btn = tk.Button(
                self.root,
                text=title,
                command=lambda t=title: self._show_random_question(t, "")
            )
            btn.grid(row=idx, column=0, pady=5, padx=20, sticky='ew')

        # Exit button 
        exit_btn = tk.Button(
            self.root,
            text='Exit',
            command=self._exit_game
        )
        #Separate the exit buttom from the options
        exit_btn.grid(row=len(self.questions)+2, column=0, pady=50, padx=20, sticky='ews')

    def _show_random_question(self, selected_title, old_random_question):
        """Display a random question from the selected title."""
        # Cleanup and recreate welcome label
        self._create_welcome_label()

        # Header (fixed)
        header = tk.Frame(self.root)
        header.grid(row=0, column=0, sticky="ew", pady=10) # Overwrite welcome label
        header.grid_columnconfigure(0, weight=1)

        # Display title and random question
        title_label = tk.Label(
            header,
            text=f"CATEGORY: {selected_title}",
            font=('San Francisco', 14, 'bold')
        )
        title_label.grid(row=0, column=0)

        # Content (flexible)
        content = tk.Frame(self.root)
        content.grid(row=1, column=0, sticky="n", padx=20)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)

        random_question = random.choice(self.questions[selected_title])

        if old_random_question == random_question: # Make sure new question is not repeated
            random_question = random.choice(self.questions[selected_title])
            old_random_question = random_question

        question_label = tk.Label(
            content,
            text=random_question,
            wraplength=350,
            border=150,
            anchor="center",
            font=('San Francisco', 12)
        )
        question_label.grid(row=0, column=0, sticky='n')

        # Footer (fixed)
        footer = tk.Frame(self.root)
        footer.grid(row=2, column=0, sticky="ew", pady=10)
        footer.grid_columnconfigure((0, 1), weight=1)

        # Navigation buttons
        next_btn = tk.Button(
            footer,
            text='Next Question',
            command=lambda: self._show_random_question(selected_title, random_question)
        )
        next_btn.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        back_btn = tk.Button(
            footer,
            text='Back to Categories',
            command=self._create_title_buttons
        )
        back_btn.grid(row=0, column=1, padx=10, pady=10, sticky='e')

    def _exit_game(self):
        """Exit the game."""
        self.root.destroy()

    def run(self):
        """Start the game loop."""
        self.root.mainloop()

def main():
    game = QuestionGame()
    game.run()

if __name__ == '__main__':
    main()