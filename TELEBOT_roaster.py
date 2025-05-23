# --- TELEBOT_roaster.py ---
import random
import json
from datetime import datetime, timedelta
from TELEBOT_DB import get_overdue_tasks, get_streak, increment_streak, is_user_muted, update_last_roast_time, get_last_roast_time

# Load roast tiers from JSON
with open("roasting_texts.json", "r", encoding="utf-8") as f:
    ROAST_TIERS = json.load(f)

def get_roast_level(hours_late, streak):
    if hours_late <= 3 and streak <= 1:
        return "mild"
    elif hours_late <= 24 and streak <= 2:
        return "medium"
    else:
        return "savage"

def should_send_roast(task_id, due_dt):
    now = datetime.now()
    last_roast = get_last_roast_time(task_id)
    
    print(f"\n🔍 Checking roast timing for task {task_id}:")
    print(f"Last roast time: {last_roast}")
    
    # If no roast has been sent yet, send within 10 seconds of deadline
    if not last_roast:
        time_since_due = (now - due_dt).total_seconds()
        print(f"First roast check - Time since due: {time_since_due:.2f} seconds")
        return time_since_due <= 10
    
    # For subsequent roasts, send every 10 minutes
    last_roast_dt = datetime.strptime(last_roast, "%Y-%m-%d %H:%M:%S")
    time_since_last_roast = (now - last_roast_dt).total_seconds()
    
    print(f"Subsequent roast check - Time since last roast: {time_since_last_roast:.2f} seconds")
    print(f"Should send roast: {time_since_last_roast >= 600}")
    
    # Only send if it's been at least 10 minutes since the last roast
    return time_since_last_roast >= 600  # 600 seconds = 10 minutes

def send_roasts():
    overdue_tasks = get_overdue_tasks()
    if not overdue_tasks:
        return []

    roasts = []
    for task in overdue_tasks:
        task_id, text, due, user_id, username = task
        if not due:
            continue

        # Skip if user is muted
        if is_user_muted(user_id):
            continue

        due_dt = datetime.strptime(due, "%Y-%m-%d %H:%M")
        
        # Check if we should send a roast based on timing
        if not should_send_roast(task_id, due_dt):
            continue

        hours_late = (datetime.now() - due_dt).total_seconds() / 3600
        streak = get_streak(user_id)
        increment_streak(user_id, task_id)

        tier = get_roast_level(hours_late, streak)
        templates = ROAST_TIERS.get(tier, [])
        if not templates:
            continue

        name = username or f"user_{user_id}"
        template = random.choice(templates)
        roast = template.replace("{username}", name).replace("{task}", text)

        message = (
            f"🔥 *Roast Alert for {name}*\n\n"
            f"💬 {roast}\n"
            f"⏰ Was Due: *{due}*"
        )
        
        print(f"\n📝 Sending roast for task {task_id}")
        # Update the last roast time for this task
        update_last_roast_time(task_id)
        roasts.append((user_id, message))

    return roasts
