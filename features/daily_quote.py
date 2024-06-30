import requests

class DailyQuote:
    def get_quote(self):
        try:
            response = requests.get("https://api.quotable.io/random")
            if response.status_code == 200:
                quote_data = response.json()
                return f'"{quote_data["content"]}" - {quote_data["author"]}'
            else:
                return "Sorry, I couldn't fetch a quote right now."
        except Exception as e:
            return f"An error occurred while fetching a quote: {str(e)}"