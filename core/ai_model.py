import google.generativeai as genai
from config import GEMINI_API_KEY

class AIModel:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def process(self, command):
        try:
            response = self.model.generate_content(command)
            return response.text
        except Exception as e:
            print(f"Error in AI processing: {str(e)}")
            return "I'm sorry, I encountered an error while processing your request."