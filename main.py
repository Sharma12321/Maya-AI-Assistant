import speech_recognition as sr
from core.speech_recognition import SpeechRecognizer
from core.text_to_speech import TextToSpeech
from core.task_executor import TaskExecutor
from core.ai_model import AIModel
from utils.logger import setup_logger
from utils.database import Database
from utils.time_utils import get_greeting
from config import WAKE_WORD
import threading
import time

class Maya:
    def __init__(self):
        self.logger = setup_logger()
        self.speech_recognizer = SpeechRecognizer()
        self.tts = TextToSpeech()
        self.db = Database()
        self.ai_model = AIModel()
        self.task_executor = TaskExecutor(self.tts)
        self.is_speaking = False
        self.wake_word_detected = threading.Event()
        self.stop_listening = False
        self.stop_speaking_event = threading.Event()

    def listen_for_wake_word(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            while not self.wake_word_detected.is_set():
                try:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    text = recognizer.recognize_google(audio).lower()
                    if WAKE_WORD.lower() in text:
                        self.wake_word_detected.set()
                        if self.is_speaking:
                            self.tts.stop_speaking()
                        return True
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    self.logger.error("Could not request results from speech recognition service")
                time.sleep(0.1)  # Small pause to reduce CPU usage
        return False

    def listen_for_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = self.speech_recognizer.recognize(audio)
                return command
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return "I didn't understand that."
            except sr.RequestError:
                self.logger.error("Could not request results from speech recognition service")
                return None

    def process_command(self, command):
        # Check if the command is related to Maya's creator
        creator_phrases = ["who created you", "who made you", "who is your creator"]
        if any(phrase in command.lower() for phrase in creator_phrases):
            response = "I was created by Sreehari."
        else:
            response = self.ai_model.process(command)
            if response is None or response == "":
                response = "I'm sorry, I couldn't process that request. Can I help you with something else?"

        self.db.log_interaction(command, response)
        return response

    def run(self):
        self.tts.speak("Hello! I'm Maya, your AI assistant. Say 'Hey Maya' when you need me!", self.stop_speaking_event)
        while True:
            self.wake_word_detected.clear()
            if self.listen_for_wake_word():
                greeting = get_greeting()
                self.tts.speak(f"{greeting}! How can I help you?", self.stop_speaking_event)

                while True:
                    command = self.listen_for_command()
                    if command is None:
                        break

                    if command.lower() in ["goodbye", "bye", "stop"]:
                        self.tts.speak("Goodbye! Say 'Hey Maya' when you need me again.", self.stop_speaking_event)
                        break

                    self.logger.info(f"Recognized command: {command}")
                    response = self.process_command(command)
                    self.tts.speak(response, self.stop_speaking_event)

                    # Ask for further assistance
                    follow_up = "Is there anything else I can help you with?"
                    self.tts.speak(follow_up, self.stop_speaking_event)

                    if self.stop_listening:
                        break

            if self.stop_listening:
                self.stop_listening = False
                continue

if __name__ == '__main__':
    maya = Maya()
    maya.run()