# SavageScheduler Bot 2.0 🤖

A sophisticated Telegram bot that combines task management with a unique personality - it roasts you when you miss deadlines! Built with modern Python technologies and natural language processing.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)

## 🌟 Features

### Task Management
- **Natural Language Understanding**: Add tasks using everyday language
  - "Remind me to buy groceries at 5 PM"
  - "Set a task to call mom tomorrow at 3"
  - "Add meeting with team on Friday 2 PM"
- **Smart Task Organization**
  - Priority-based task sorting
  - Due date tracking
  - Task categories and tags
  - Recurring tasks support

### Reminder System
- **Intelligent Notifications**
  - Customizable reminder intervals
  - Multiple reminder types (one-time, recurring)
  - Timezone-aware scheduling
  - Smart notification timing

### Roast System 🔥
- **Personality-Driven Feedback**
  - Multiple roast intensity levels
  - Context-aware roasting
  - Customizable roast frequency
  - Mute/Unmute functionality

### Analytics & Tracking
- **Performance Metrics**
  - Task completion streaks
  - Success rate tracking
  - Productivity insights
  - Historical performance data

## 🛠 Technical Stack

### Core Technologies
- **Python 3.8+**: Modern Python features and async support
- **python-telegram-bot 20.7**: Latest Telegram Bot API implementation
- **SQLAlchemy 2.0.23**: Advanced database ORM
- **asyncio**: Asynchronous programming support

### Natural Language Processing
- **spaCy 3.7.2**: State-of-the-art NLP library
  - Named Entity Recognition (NER)
  - Part-of-Speech (POS) tagging
  - Dependency parsing
  - Custom entity recognition for dates and times

### Database
- **SQLite**: Lightweight, serverless database
  - Efficient task storage
  - User data management
  - Analytics tracking
  - Streak system implementation

### Additional Libraries
- **python-dotenv**: Environment variable management
- **pytz**: Timezone handling
- **datetime**: Advanced date/time operations

## 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/harshgupta257/SavageScheduler_Bot_2.0.git
   cd SavageScheduler_Bot_2.0
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   - Create a `.env` file in the project root
   - Add your Telegram bot token:
     ```
     BOT_TOKEN=your_bot_token_here
     ```

5. **Initialize Database**
   ```bash
   python init_streak_table.py
   ```

6. **Run the Bot**
   ```bash
   python TELEBOT_main.py
   ```

## 📝 Usage Guide

### Basic Commands
- **Add Task**: "Remind me to buy groceries at 5 PM"
- **View Tasks**: "Show me all tasks"
- **Complete Task**: "Mark task 1 as done"
- **Delete Task**: "Delete task 2"

### Roast System
- **Mute Roasts**: "mute roasts"
- **Unmute Roasts**: "unmute roasts"
- **Check Roast Status**: "roast status"

### Task Management
- **Set Priority**: "Set high priority for task 1"
- **Add Tags**: "Tag task 2 as work"
- **View by Category**: "Show me all work tasks"

## 📁 Project Structure

```
SavageScheduler_Bot_2.0/
├── TELEBOT_main.py           # Main bot entry point
├── TELEBOT_intent_router.py  # Intent classification
├── TELEBOT_roaster.py        # Roast system implementation
├── TELEBOT_DB.py            # Database operations
├── TELEBOT_reminder.py      # Reminder system
├── telebot_nlp_step1.py     # NLP utilities
├── TELEBOT_training_intent.py # Intent training
├── init_streak_table.py     # Database initialization
└── requirements.txt         # Project dependencies
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write clear commit messages
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [spaCy](https://spacy.io/) for NLP capabilities
- [python-telegram-bot](https://python-telegram-bot.org/) library
- [SQLAlchemy](https://www.sqlalchemy.org/) for database operations

## 📞 Support

For support, please:
1. Check the [Issues](https://github.com/harshgupta257/SavageScheduler_Bot_2.0/issues) section
2. Create a new issue if your problem isn't already listed
3. Provide detailed information about your problem

---

Made with ❤️ by [Harsh Gupta](https://github.com/harshgupta257) 