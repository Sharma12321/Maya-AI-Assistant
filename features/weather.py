import requests
from config import WEATHER_API_KEY

class WeatherService:
    def get_weather(self, location):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={location}&appid={WEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(complete_url)
            weather_data = response.json()
            if weather_data['cod'] == 200:
                main = weather_data['main']
                temperature = main['temp']
                humidity = main['humidity']
                description = weather_data['weather'][0]['description']
                return f"The current temperature in {location} is {temperature}°C with {description}. The humidity is {humidity}%."
            else:
                return "Sorry, I couldn't find the weather for that location."
        except Exception as e:
            return f"An error occurred while fetching the weather data: {str(e)}"