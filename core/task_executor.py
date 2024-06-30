from features.weather import WeatherService
from features.news import NewsService
from features.calculator import Calculator
from features.wikipedia_search import WikipediaSearch
from features.jokes import JokeService
from features.daily_quote import DailyQuote
from features.reminder import ReminderService
from features.todo_list import TodoList

class TaskExecutor:
    def __init__(self, tts_engine):
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.calculator = Calculator()
        self.wikipedia_search = WikipediaSearch()
        self.joke_service = JokeService()
        self.daily_quote = DailyQuote()
        self.reminder_service = ReminderService(tts_engine)
        self.todo_list = TodoList()

    def parse_task(self, ai_response):
        # Implement logic to parse AI response and determine task type
        # This is a simplified version and should be expanded based on your needs
        if "weather" in ai_response.lower():
            return {"type": "weather", "location": "default_location"}
        elif "news" in ai_response.lower():
            return {"type": "news", "category": "general"}
        elif "calculate" in ai_response.lower():
            return {"type": "calculate", "expression": ai_response.split("calculate")[1].strip()}
        elif "wikipedia" in ai_response.lower():
            return {"type": "wikipedia", "query": ai_response.split("wikipedia")[1].strip()}
        elif "joke" in ai_response.lower():
            return {"type": "joke"}
        elif "quote" in ai_response.lower():
            return {"type": "daily_quote"}
        elif "remind" in ai_response.lower():
            # This is a simplification. You'd need more sophisticated parsing for reminders.
            return {"type": "set_reminder", "reminder_task": ai_response, "minutes": 5}
        elif "todo" in ai_response.lower():
            if "add" in ai_response.lower():
                return {"type": "add_todo", "task": ai_response.split("add")[1].strip()}
            elif "remove" in ai_response.lower():
                return {"type": "remove_todo", "task": ai_response.split("remove")[1].strip()}
            else:
                return {"type": "list_todo"}
        else:
            return {"type": "general", "response": ai_response}

    def execute_task(self, task):
        task_type = task['type']
        if task_type == "weather":
            return self.weather_service.get_weather(task['location'])
        elif task_type == "news":
            return self.news_service.get_top_headlines(task.get('category', 'general'))
        elif task_type == "calculate":
            return self.calculator.calculate(task['expression'])
        elif task_type == "wikipedia":
            return self.wikipedia_search.search(task['query'])
        elif task_type == "joke":
            return self.joke_service.get_joke()
        elif task_type == "daily_quote":
            return self.daily_quote.get_quote()
        elif task_type == "set_reminder":
            return self.reminder_service.set_reminder(task['reminder_task'], task['minutes'])
        elif task_type == "list_reminders":
            return self.reminder_service.list_reminders()
        elif task_type == "add_todo":
            return self.todo_list.add_task(task['task'])
        elif task_type == "remove_todo":
            return self.todo_list.remove_task(task['task'])
        elif task_type == "list_todo":
            return self.todo_list.list_tasks()
        elif task_type == "general":
            return task['response']
        else:
            return "I'm sorry, I don't know how to handle that task."