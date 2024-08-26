import sys
import openai
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QTextEdit

class TaskGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Task Description Label
        self.task_description = QLabel('Task: Correct the errors in the paragraph below')
        
        # Sample Prompt Label
        self.sample_prompt = QLabel('Sample Prompt: "The dog runned down the street quickly, it\'s ears flopping in the wind. She seen a cat sitting under the tree and decides to chase it. The cat, who was tired, didn\'t moved at first, but then it ran up the tree before the dog could reached it. The dog barked loudly and jumped but could not reached the cat. After a few minutes, the dog give up and walks away sadly"')
        self.sample_prompt.setWordWrap(True)

        # Textbox for user input
        self.user_input = QTextEdit(self)
        self.user_input.setPlaceholderText('Enter your answer here...')
        self.user_input.setFixedHeight(150)

        # Submit button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.show_message)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.task_description)
        layout.addWidget(self.sample_prompt)
        layout.addWidget(self.user_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # Window settings
        self.setWindowTitle('Task Submission')
        self.setGeometry(100, 100, 400, 200)

    def show_message(self):
        client = openai.OpenAI(api_key= "")
        user_answer = self.user_input.toPlainText()

        prompt = (
            "Imagine you are a Nao Robot. You are assisting a human with a grammatical task. The human is to evaluate the paragraph: 'The dog runned down the street quickly, it\'s ears flopping in the wind. She seen a cat sitting under the tree and decides to chase it. The cat, who was tired, didn\'t moved at first, but then it ran up the tree before the dog could reached it. The dog barked loudly and jumped but could not reached the cat. After a few minutes, the dog give up and walks away sadly' and must fix the grammatical erros within it."
        )

        content = (
            "Please provide feedback for the task based on the humans response as a json. Here is their response: " + user_answer
        )

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            response_format={"type":"json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ]
        )

        print(response.choices[0].message.content)
        QMessageBox.information(self, 'Submission Received', f'Your answer: "{user_answer}" has been submitted.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskGUI()
    window.show()
    sys.exit(app.exec())
