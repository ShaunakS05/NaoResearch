import sys
import openai
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QGridLayout, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QFont

class TaskGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Define font sizes
        task_font = QFont('Arial', 14)
        sample_prompt_font = QFont('Arial', 12)
        button_font = QFont('Arial', 10)

        # Task Description Label
        self.task_description = QLabel('Task: Correct the errors in the paragraph below')
        self.task_description.setContentsMargins(0, 0, 0, 0)
        self.task_description.setFont(task_font)  # Set custom font size

        # Sample Prompt Label
        self.sample_prompt = QLabel(
            'Sample Prompt: "The dog runned down the street quickly, it\'s ears flopping in the wind. She seen a cat sitting under the tree and decides to chase it. The cat, who was tired, didn\'t moved at first, but then it ran up the tree before the dog could reached it. The dog barked loudly and jumped but could not reached the cat. After a few minutes, the dog give up and walks away sadly."'
        )
        self.sample_prompt.setWordWrap(True)
        self.sample_prompt.setContentsMargins(0, 0, 0, 0)
        self.sample_prompt.setFont(sample_prompt_font)  # Set custom font size

        # Textbox for user input
        self.user_input = QTextEdit(self)
        self.user_input.setPlaceholderText('Enter your answer here...')
        self.user_input.setFixedHeight(300)
        self.user_input.setFont(sample_prompt_font)  # Set the same font size as sample_prompt

        # Submit button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setFixedHeight(40)  # Custom height
        self.submit_button.setFixedWidth(100)   # Custom width
        self.submit_button.setFont(button_font)  # Set custom font size
        self.submit_button.clicked.connect(self.show_message)

        # Layout for the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add stretchable space to push button to the right
        button_layout.addWidget(self.submit_button)

        # Main layout using QGridLayout
        layout = QGridLayout()
        layout.setSpacing(0)  # Set spacing between widgets to 0
        layout.setContentsMargins(20, 10, 20, 20)  # Adjust margins as needed

        # Add widgets to layout
        layout.addWidget(self.task_description, 0, 0)
        layout.addWidget(self.sample_prompt, 1, 0)
        layout.addWidget(self.user_input, 2, 0)
        layout.addLayout(button_layout, 3, 0)  # Add button layout without alignment

        self.setLayout(layout)

        # Window settings
        self.setWindowTitle('Task Submission')
        self.setGeometry(100, 100, 1000, 600)

    def show_message(self):
        client = openai.OpenAI(api_key="")
        user_answer = self.user_input.toPlainText()

        prompt = (
            "Imagine you are a Nao Robot. You are assisting a human with a grammatical task. The human is to evaluate the paragraph: 'The dog runned down the street quickly, it\'s ears flopping in the wind. She seen a cat sitting under the tree and decides to chase it. The cat, who was tired, didn\'t moved at first, but then it ran up the tree before the dog could reached it. The dog barked loudly and jumped but could not reached the cat. After a few minutes, the dog give up and walks away sadly' and must fix the grammatical errors within it."
        )

        content = (
            "Please provide feedback for the task based on the human's response as a JSON. Here is their response: " + user_answer
        )

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            response_format={"type": "json_object"},
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
