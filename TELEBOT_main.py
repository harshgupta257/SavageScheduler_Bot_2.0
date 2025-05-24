#TELEBOT_main.py
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
from TELEBOT_intent_router import route_intent
from TELEBOT_roaster import send_roasts  #✅ Import your roast function
from TELEBOT_reminder import get_due_reminders  # Import reminder system
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables. Please set it in .env file")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Welcome to SavageScheduler 2.0!\n\n"
        "I'm your AI-powered task manager with attitude! 🤖\n\n"
        "Just talk to me naturally:\n"
        "• 'Remind me to buy groceries at 5 PM'\n"
        "• 'Show me all tasks'\n"
        "• 'Mark task 1 as done'\n"
        "• 'Delete task 2'\n\n"
        "Type /help for more examples!"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "🤖 Here's how to talk to me:\n\n"
        "📝 Adding Tasks:\n"
        "• 'Remind me to call mom tomorrow at 3'\n"
        "• 'Add task: team meeting on Friday 2 PM'\n"
        "• 'Schedule a dentist appointment for next Monday'\n\n"
        "📋 Viewing Tasks:\n"
        "• 'Show me all tasks'\n"
        "• 'What tasks do I have?'\n"
        "• 'List my pending tasks'\n\n"
        "✅ Completing Tasks:\n"
        "• 'Mark task 1 as done'\n"
        "• 'Complete the meeting task'\n"
        "• 'Task 2 is finished'\n\n"
        "🗑️ Deleting Tasks:\n"
        "• 'Delete task 1'\n"
        "• 'Remove the meeting task'\n"
        "• 'Cancel task 2'\n\n"
        "🔥 Roast System:\n"
        "• 'mute roasts' - Stop getting roasted\n"
        "• 'unmute roasts' - Enable roasts again\n\n"
        "Just talk to me naturally, and I'll understand!"
    )
    await update.message.reply_text(help_message)

async def periodic_roast_job(app):
    while True:
        roasts = send_roasts()
        for user_id, message in roasts:
            try:
                await app.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
            except Exception as e:
                print(f"❌ Failed to send roast to user {user_id}: {e}")
        
        # Check every 5 seconds to catch the 10-second window for first roasts
        await asyncio.sleep(5)

async def periodic_reminder_job(app):
    while True:
        # ⏰ Send reminders
        reminders = get_due_reminders()
        for user_id, message in reminders:
            try:
                await app.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
            except Exception as e:
                print(f"❌ Failed to send reminder to user {user_id}: {e}")
        
        # Check reminders every minute
        await asyncio.sleep(60)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # Route and get the result back
    user_id = update.effective_user.id
    username = update.effective_user.username
    response = route_intent(user_input, user_id=user_id, username=username)

    # Send the response back to user
    await update.message.reply_text(response or "✅ Received. Task processed!")

#✅ Post-init function that runs after bot starts
async def post_init(app):
    app.create_task(periodic_roast_job(app))
    app.create_task(periodic_reminder_job(app))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running with roasting system and reminders enabled!")
    app.run_polling()

if __name__ == "__main__":
    main()
