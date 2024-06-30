import wikipedia

class WikipediaSearch:
    def search(self, query, sentences=2):
        try:
            result = wikipedia.summary(query, sentences=sentences)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Your query '{query}' may refer to multiple topics. Please be more specific. Possible matches: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return f"Sorry, I couldn't find any information on '{query}'"
        except Exception as e:
            return f"An error occurred while searching Wikipedia: {str(e)}"