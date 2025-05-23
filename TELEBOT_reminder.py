# --- TELEBOT_reminder.py ---
from datetime import datetime
from TELEBOT_DB import get_pending_tasks, get_pending_tasks_with_user_info

def get_due_reminders():
    pending_tasks = get_pending_tasks_with_user_info()
    reminders = []

    for task in pending_tasks:
        id, task_text, due_datetime, user_id, username = task
        if not due_datetime:
            continue

        try:
            deadline = datetime.strptime(due_datetime, "%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"[Reminder Parse Error] Task ID {id} deadline invalid: {e}")
            continue

        now = datetime.now()
        minutes_to_go = (deadline - now).total_seconds() / 60

        if 0 <= minutes_to_go <= 1:  # between 4 and 5 minutes left
            name = username or f"user_{user_id}"
            message = f"⏰ *Reminder for {name}*\n\n_Task_: _{task_text}_\n📌 Due at: *{deadline.strftime('%H:%M')}*"
            reminders.append((user_id, message))

    return reminders
