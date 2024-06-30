# Maya-AI-Assistant
Maya AI Assistant is a versatile AI companion with voice and text interaction. Available in both terminal and GUI versions, it performs tasks like weather updates, news briefings, and Wikipedia searches. Features include wake word detection, continuous conversation, and text-to-speech responses, making it a handy digital assistant for daily use.

Maya is an intelligent AI assistant capable of understanding voice commands and providing responses through text-to-speech. It offers a range of features and can engage in continuous conversations. The project includes both a terminal-based version and a graphical user interface.

## Features

- Voice and text input for user interactions
- Text-to-speech responses
- Continuous conversation mode
- Task execution for various commands (weather, news, calculations, etc.)
- Conversation history
- Wake word detection ("Hey Maya")
- GUI version with dark mode toggle and ability to interrupt speech output

## Requirements

- Python 3.7+
- SpeechRecognition
- pyttsx3
- requests
- wikipedia
- python-dotenv
- PyQt5 (for GUI version)

## Installation

1. Clone the repository:
git clone https://github.com/Sharma12321/maya-ai-assistant.git
cd maya-ai-assistant



2. Install the required packages:
pip install -r requirements.txt



3. Set up your environment variables:
Add all your API keys in the 'config.py' file:
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key
GEMINI_API_KEY=your_gemini_api_key



## Usage

### Terminal Version

Run the main script to start Maya in the terminal:
python main.py



- Say "Hey Maya" to wake up the assistant.
- Speak your commands or type them when prompted.
- Say "goodbye" or "stop" to end the conversation.
- Say "shutdown" to exit the program.

### GUI Version

Run the GUI application to start Maya with a graphical interface:
python maya_app.py



- Click "Wake Maya" or say "Hey Maya" to start interacting.
- Speak your commands or type them in the input field.
- Use the "Stop Speaking" button to interrupt Maya's speech.
- Toggle between light and dark modes using the "Change Mode" button.

## Project Structure

- `main.py`: Terminal-based Maya application
- `maya_app.py`: GUI-based Maya application
- `core/`: Contains core functionality modules
- `features/`: Individual feature implementations (weather, news, etc.)
- `utils/`: Utility functions and classes
- `config.py`: Configuration settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [MIT LICENSE](LICENSE) file for details.

## Acknowledgments

- Gemini AI for the GPT model used in generating responses
- OpenWeatherMap for weather data
- NewsAPI for news headlines
- Wikipedia API for information retrieval

## Contact

sreehari sharma - sreeharisharma@outlook.com

Project Link: https://github.com/Sharma12321/maya-ai-assistant
