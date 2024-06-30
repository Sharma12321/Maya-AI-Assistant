import requests
from config import NEWS_API_KEY

class NewsService:
    def get_top_headlines(self, category):
        base_url = "https://newsapi.org/v2/top-headlines?"
        complete_url = f"{base_url}country=us&category={category}&apiKey={NEWS_API_KEY}"
        try:
            response = requests.get(complete_url)
            news_data = response.json()
            if news_data['status'] == 'ok':
                articles = news_data['articles'][:5]  # Get top 5 articles
                headlines = [f"{i+1}. {article['title']}" for i, article in enumerate(articles)]
                return "Top news headlines:\n" + "\n".join(headlines)
            else:
                return "Sorry, I couldn't fetch the news."
        except Exception as e:
            return f"An error occurred while fetching the news: {str(e)}"