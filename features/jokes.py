import requests

class JokeService:
    def get_joke(self):
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            if response.status_code == 200:
                joke_data = response.json()
                return f"{joke_data['setup']} ... {joke_data['punchline']}"
            else:
                return "Sorry, I couldn't fetch a joke right now."
        except Exception as e:
            return f"An error occurred while fetching a joke: {str(e)}"