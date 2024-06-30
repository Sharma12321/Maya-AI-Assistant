import threading
import time

class ReminderService:
    def __init__(self, tts_engine):
        self.reminders = []
        self.tts_engine = tts_engine

    def set_reminder(self, task, minutes):
        timer = threading.Timer(minutes * 60, self._reminder_callback, [task])
        timer.start()
        self.reminders.append((task, timer))
        return f"Okay, I'll remind you to {task} in {minutes} minutes."

    def _reminder_callback(self, task):
        self.tts_engine.speak(f"Reminder: It's time to {task}")
        self.reminders = [r for r in self.reminders if r[0] != task]

    def list_reminders(self):
        if not self.reminders:
            return "You have no active reminders."
        return "Your active reminders are: " + ", ".join(task for task, _ in self.reminders)