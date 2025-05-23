# TELEBOT - AI-Powered Task Management Bot

A smart Telegram bot that helps you manage tasks with a unique twist - it roasts you when you miss deadlines! Built with Python, NLP, and Telegram Bot API.

## Features

- 🤖 **Natural Language Understanding**: Add tasks using everyday language
- ⏰ **Smart Reminders**: Get notified before task deadlines
- 🔥 **Roast System**: Get roasted (with different intensity levels) when you miss deadlines
- 📊 **Streak Tracking**: Keep track of your task completion streaks
- 🔇 **Mute/Unmute**: Control when you want to receive roasts
- 📝 **Task Management**: Add, complete, delete, and view tasks easily

## Technical Stack

- Python 3.x
- Telegram Bot API
- spaCy (for NLP)
- SQLite (Database)
- asyncio (Asynchronous Programming)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/telebot.git
cd telebot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Telegram Bot:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot and get your API token
   - Create a `.env` file in the project root and add your token:
     ```
     BOT_TOKEN=your_bot_token_here
     ```

4. Initialize the database:
```bash
python init_streak_table.py
```

5. Run the bot:
```bash
python TELEBOT_main.py
```

## Usage

### Basic Commands
- Add task: "Remind me to buy groceries at 5 PM"
- View tasks: "Show me all tasks"
- Complete task: "Mark task 1 as done"
- Delete task: "Delete task 2"

### Roast System
- Mute roasts: "mute roasts"
- Unmute roasts: "unmute roasts"

## Project Structure

- `TELEBOT_main.py`: Main bot file
- `TELEBOT_intent_router.py`: Handles user intent classification
- `TELEBOT_roaster.py`: Manages the roast system
- `TELEBOT_DB.py`: Database operations
- `TELEBOT_reminder.py`: Handles task reminders
- `telebot_nlp_step1.py`: NLP utilities
- `TELEBOT_training_intent.py`: Intent training module

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Telegram Bot API
- spaCy for NLP capabilities
- Python asyncio library 