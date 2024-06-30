import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
                             QHBoxLayout, QTextEdit, QLineEdit, QStatusBar, QScrollArea)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

import speech_recognition as sr
from main import Maya

class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)
    listening = pyqtSignal(bool)

    def __init__(self, maya):
        super().__init__()
        self.maya = maya
        self.listening_flag = False

    def run(self):
        self.listening_flag = True
        self.listening.emit(self.listening_flag)
        while self.listening_flag:
            command = self.maya.listen_for_command()
            if command:
                self.recognized_text.emit(command)

    def stop_listening(self):
        self.listening_flag = False
        self.listening.emit(self.listening_flag)

class MayaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.maya = Maya()
        self.speech_thread = SpeechRecognitionThread(self.maya)
        self.speech_thread.recognized_text.connect(self.process_command)
        self.speech_thread.listening.connect(self.update_listening_status)
        self.dark_mode = False
        self.continuous_interaction = True

    def initUI(self):
        self.setWindowTitle("Maya")
        self.setGeometry(100, 100, 600, 800)
        self.setStyleSheet("QMainWindow { background-color: #F0F0F0; }")

        app_icon = QIcon("maya_icon.ico")
        QApplication.setWindowIcon(app_icon)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # History view
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setFont(QFont("Open Sans", 12))
        self.history_text.setStyleSheet("background-color: #FFFFFF; padding: 10px; border-radius: 10px; margin: 10px;")
        main_layout.addWidget(self.history_text)

        # Output label
        self.output_label = QLabel()
        self.output_label.setFont(QFont("Open Sans", 14))
        self.output_label.setWordWrap(True)
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setStyleSheet("background-color: #FFFFFF; padding: 10px; border-radius: 10px; margin: 10px;")
        main_layout.addWidget(self.output_label)

        # Input field
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Open Sans", 12))
        self.input_field.setStyleSheet("background-color: #FFFFFF; padding: 5px; border-radius: 5px; margin: 10px;")
        self.input_field.returnPressed.connect(self.process_text_input)
        main_layout.addWidget(self.input_field)

        # Buttons
        button_layout = QHBoxLayout()
        
        wake_button = QPushButton("Wake Maya")
        wake_button.setStyleSheet(self.get_button_style("#4CAF50"))
        wake_button.clicked.connect(self.wake_maya)
        button_layout.addWidget(wake_button)

        self.stop_listening_button = QPushButton("Stop Listening")
        self.stop_listening_button.setEnabled(False)
        self.stop_listening_button.setStyleSheet(self.get_button_style("#f44336"))
        self.stop_listening_button.clicked.connect(self.stop_listening)
        button_layout.addWidget(self.stop_listening_button)

        stop_speaking_button = QPushButton("Stop Speaking")
        stop_speaking_button.setStyleSheet(self.get_button_style("#FF9800"))
        stop_speaking_button.clicked.connect(self.stop_speaking)
        button_layout.addWidget(stop_speaking_button)

        dark_mode_button = QPushButton("Change Mode")
        dark_mode_button.setStyleSheet(self.get_button_style("#2196F3"))
        dark_mode_button.clicked.connect(self.toggle_dark_mode)
        button_layout.addWidget(dark_mode_button)

        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color}; 
                color: white; 
                padding: 10px; 
                border-radius: 5px;
                margin-right: 5px;
            }}
            QPushButton:pressed {{
                background-color: {self.get_darker_color(color)};
            }}
        """

    def get_darker_color(self, color):
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        factor = 0.8
        return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"

    def wake_maya(self):
        self.maya.tts.speak("Hello! I'm Maya, your AI assistant. How can I help you?", self.maya.stop_speaking_event)
        self.update_listening_status(True)
        self.speech_thread.start()
        self.stop_listening_button.setEnabled(True)
        self.continuous_interaction = True

    def stop_listening(self):
        self.speech_thread.stop_listening()
        self.stop_listening_button.setEnabled(False)
        self.update_listening_status(False)
        self.continuous_interaction = False

    def stop_speaking(self):
        self.maya.stop_speaking_event.set()
        self.maya.tts.stop_speaking()
        self.statusBar.showMessage("Speech interrupted")

    def update_listening_status(self, listening):
        if listening:
            self.output_label.setText("Maya is listening...")
            self.statusBar.showMessage("Listening...")
        else:
            self.output_label.setText("Maya is not listening.")
            self.statusBar.showMessage("Ready")

    def process_command(self, command):
        self.statusBar.showMessage("Processing...")
        response = self.maya.process_command(command)
        self.output_label.setText(response)
        self.history_text.append(f"You: {command}\nMaya: {response}\n")
        self.statusBar.showMessage("Ready")
        
        # Speak the response
        self.maya.tts.speak(response, self.maya.stop_speaking_event)
        
        # Ask for further assistance
        QTimer.singleShot(1000, self.ask_for_more)

    def ask_for_more(self):
        if self.continuous_interaction:
            follow_up = "Is there anything else I can help you with?"
            self.maya.tts.speak(follow_up, self.maya.stop_speaking_event)
            self.output_label.setText(follow_up)
            self.history_text.append(f"Maya: {follow_up}\n")

    def process_text_input(self):
        command = self.input_field.text()
        self.input_field.clear()
        self.process_command(command)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("QMainWindow { background-color: #2C2C2C; color: #FFFFFF; }")
            self.history_text.setStyleSheet("background-color: #3C3C3C; color: #FFFFFF; padding: 10px; border-radius: 10px; margin: 10px;")
            self.output_label.setStyleSheet("background-color: #3C3C3C; color: #FFFFFF; padding: 10px; border-radius: 10px; margin: 10px;")
            self.input_field.setStyleSheet("background-color: #3C3C3C; color: #FFFFFF; padding: 5px; border-radius: 5px; margin: 10px;")
            self.statusBar.setStyleSheet("background-color: #2C2C2C; color: #FFFFFF;")
        else:
            self.setStyleSheet("QMainWindow { background-color: #F0F0F0; color: #000000; }")
            self.history_text.setStyleSheet("background-color: #FFFFFF; color: #000000; padding: 10px; border-radius: 10px; margin: 10px;")
            self.output_label.setStyleSheet("background-color: #FFFFFF; color: #000000; padding: 10px; border-radius: 10px; margin: 10px;")
            self.input_field.setStyleSheet("background-color: #FFFFFF; color: #000000; padding: 5px; border-radius: 5px; margin: 10px;")
            self.statusBar.setStyleSheet("")

        # Update button styles
        for button in self.findChildren(QPushButton):
            if button.text() == "Wake Maya":
                button.setStyleSheet(self.get_button_style("#4CAF50"))
            elif button.text() == "Stop Listening":
                button.setStyleSheet(self.get_button_style("#f44336"))
            elif button.text() == "Stop Speaking":
                button.setStyleSheet(self.get_button_style("#FF9800"))
            elif button.text() == "Change Mode":
                button.setStyleSheet(self.get_button_style("#2196F3"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    maya_app = MayaApp()
    maya_app.show()
    sys.exit(app.exec_())