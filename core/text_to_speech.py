import pyttsx3
import re
import threading

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Female voice
        self.engine.setProperty('rate', 150)
        self.speaking_thread = None

    def speak(self, text, stop_event):
        clean_text = re.sub(r'\*.*?\*', '', text)
        clean_text = clean_text.replace('*', '')
        clean_text = ' '.join(clean_text.split())
        
        print(f"Maya: {clean_text}")
        
        def run_speech():
            for sentence in clean_text.split('.'):
                if stop_event.is_set():
                    break
                self.engine.say(sentence.strip())
                self.engine.runAndWait()
                if self.engine._inLoop:
                    self.engine.endLoop()

        self.speaking_thread = threading.Thread(target=run_speech)
        self.speaking_thread.start()

    def stop_speaking(self):
        if self.speaking_thread and self.speaking_thread.is_alive():
            self.engine.stop()
            if self.engine._inLoop:
                self.engine.endLoop()
            self.speaking_thread.join()

    def set_speed(self, speed):
        self.engine.setProperty('rate', speed)