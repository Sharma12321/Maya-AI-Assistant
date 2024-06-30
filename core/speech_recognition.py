import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                return audio
            except sr.WaitTimeoutError:
                print("Listening timed out. Please try again.")
                return None

    def recognize(self, audio):
        if audio is None:
            return "I didn't hear anything. Could you please repeat?"
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "I didn't understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."