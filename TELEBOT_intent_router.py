import spacy
import re
from difflib import get_close_matches
from telebot_nlp_step1 import extract_datetime_custom  # ✅ your datetime extractor
from TELEBOT_DB import (
    add_task, mark_task_complete, get_all_tasks, get_pending_tasks, 
    get_completed_tasks, delete_task, format_tasks, mute_user, 
    unmute_user, is_user_muted
)  # ✅ your DB functions
from datetime import datetime, timedelta



# Load trained intent model
nlp = spacy.load("intent_model")

# === Intent Handlers ===
def is_valid_task(text):
    return len(re.sub(r"[^\w\s]", "", text)) >= 5  # At least 5 alphanumeric chars

def handle_add_task(text, user_id=None, username=None):
    extracted_dt = extract_datetime_custom(text)
    if not is_valid_task(text):
        print("⚠️ Task text too short or invalid (emoji-only?). Skipping...")
        return

    formatted_time = extracted_dt.strftime('%Y-%m-%d %H:%M') if extracted_dt else None
    add_task(text, formatted_time, user_id, username)
    print(f"[add_task] → Task: '{text}' | ⏰ When: {formatted_time or 'Not found'} | 👤 User: {username or user_id}")

    reminder_status = ""
    if extracted_dt:
        now = datetime.now()
        if extracted_dt - now > timedelta(minutes=1):
            reminder_status = "🔔 Reminder will be sent 1 minute before deadline."
        else:
            reminder_status = "⏰ Reminder skipped (deadline too close)."


    return f"✅ Task added: *{text}*\n🕒 When: {formatted_time or 'Not found'}\n{reminder_status}"

def handle_view_tasks(text):
    tasks = get_all_tasks()
    if not tasks:
        return "📭 You have no tasks."
    return format_tasks(tasks, "All Tasks")

def handle_pending_tasks(text):
    tasks = get_pending_tasks()
    if not tasks:
        return "🎉 You have no pending tasks!"
    return format_tasks(tasks, "Pending Tasks")

def handle_complete_task(text):
     # Try extracting numeric ID from the message
    
    pending_tasks = get_pending_tasks()
    existing_ids = [t[0] for t in pending_tasks]  # t[0] = task_id

    match = re.search(r'\b(\d+)\b',text)
    if match:
        task_id = int(match.group(1))

        if task_id in existing_ids:
            mark_task_complete(task_id)
            return f"✅ Marked as completed with ID: *{task_id}*"
        else:
            return f"❌ Couldn't find a matching task ID."
    
    # Fallback to fuzzy match by task text

    task_texts = [t[1] for t in pending_tasks]  # t[1] = task_text
    best_match = get_close_matches(text, task_texts, n=1, cutoff=0.5)

    if best_match:
        mark_task_complete(best_match[0])
        return f"✅ Marked as completed: *{best_match[0]}*"
    else:
        return "❌ Couldn't find a matching task to mark as complete."


def handle_show_completed_tasks(text):
    tasks = get_completed_tasks()
    if not tasks:
        return "😎 No completed tasks yet!"
    return format_tasks(tasks, "Completed Tasks")

def handle_delete_task(text):
   # Try extracting numeric ID from the message
    
    all_tasks = get_all_tasks()
    existing_ids = [t[0] for t in all_tasks]  # t[0] = task_id

#----------------DEBUG LINES----------------------------
    #print("🧪 User input:", text)
    #print("📋 Existing task IDs:", existing_ids)

    match = re.search(r'\b(\d+)\b', text)
    if match:
        task_id = int(match.group(1))


        if task_id in existing_ids:
            delete_task(task_id)
            return f"🗑️ Deleted task with ID: *{task_id}*"
        else:
            return f"❌ Couldn't find a matching task ID to delete."

    # Fallback to fuzzy match by task text

    task_texts = [t[1] for t in all_tasks]  # t[1] = task_text

    best_match = get_close_matches(text, task_texts, n=1, cutoff=0.5)

    if best_match:
        delete_task(best_match[0])
        return f"🗑️ Deleted task: *{best_match[0]}*"
    else:
        return "❌ Couldn't find a matching task to delete."

def handle_mute_roasts(text, user_id=None):
    if not user_id:
        return "❌ User ID is required to mute roasts."
    
    mute_user(user_id)
    return "🔇 Roasts have been muted for you. You won't receive any roast notifications."

def handle_unmute_roasts(text, user_id=None):
    if not user_id:
        return "❌ User ID is required to unmute roasts."
    
    unmute_user(user_id)
    return "🔊 Roasts have been unmuted. You'll receive roast notifications again."

def handle_other(text):
    return f"🤖 I'm not sure what to do with: '{text}'"

# === Intent Router ===
def classify_intent_with_threshold(text, threshold=0.6):
    doc = nlp(text)
    if not doc.cats:
        return "other"

    top_intent = max(doc.cats, key=doc.cats.get)
    confidence = doc.cats[top_intent]

    # ✅ Add this line to see the intent and its confidence
    print(f"🔍 Predicted: {top_intent} (Confidence: {confidence:.2f})")

    if confidence < threshold:
        return "other"
    return top_intent

def route_intent(text, user_id=None, username=None):
    # Check for mute/unmute commands first
    if text.lower() in ["mute roasts", "mute roast", "stop roasts", "stop roast"]:
        return handle_mute_roasts(text, user_id)
    elif text.lower() in ["unmute roasts", "unmute roast", "enable roasts", "enable roast"]:
        return handle_unmute_roasts(text, user_id)

    intent = classify_intent_with_threshold(text)

    intent_map = {
        "add_task": handle_add_task,
        "view_tasks": handle_view_tasks,
        "pending_tasks": handle_pending_tasks,
        "complete_task": handle_complete_task,
        "show_completed_tasks": handle_show_completed_tasks,
        "delete_task": handle_delete_task,
        "other": handle_other
    }

    handler = intent_map.get(intent, handle_other)
    if intent == "add_task":
        return handler(text, user_id=user_id, username=username)
    else:
        return handler(text)

