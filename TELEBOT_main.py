#TELEBOT_main.py
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
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

    # Register handlers...
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running with roasting system and reminders enabled!")
    app.run_polling()

if __name__ == "__main__":
    main()
