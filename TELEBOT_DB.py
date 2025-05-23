import sqlite3
from datetime import datetime

DB_FILE = "tasks.db"

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT NOT NULL,
            due_datetime TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            username TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streak_tasks (
            task_id INTEGER PRIMARY KEY,
            user_id TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS muted_users (
            user_id INTEGER PRIMARY KEY,
            muted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS last_roast_times (
            task_id INTEGER PRIMARY KEY,
            last_roast_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    conn.commit()
    conn.close()

from datetime import datetime

def format_tasks(tasks, title="Tasks"):
    if not tasks:
        return f"📭 No {title.lower()} found."

    lines = [f"📋 **{title}**"]
    for task in tasks:
        task_id, text, due, status = task
        status_icon = "✅" if status == "completed" else "🕗"

        # Format due date
        if due:
            try:
                dt = datetime.strptime(due, "%Y-%m-%d %H:%M:%S")  # If stored with seconds
            except ValueError:
                try:
                    dt = datetime.strptime(due, "%Y-%m-%d %H:%M")  # If stored without seconds
                except ValueError:
                    dt = None
            due_str = dt.strftime('%d %b %Y, %I:%M %p') if dt else "N/A"
        else:
            due_str = "N/A"

        lines.append(f"🔹 ID: {task_id} | {status_icon} {text.strip()} | Due: {due_str}")
    return "\n".join(lines)

def add_task(task_text, due_datetime=None, user_id=None, username=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task_text, due_datetime, user_id, username) VALUES (?, ?, ?, ?)', (task_text, due_datetime, user_id, username))
    conn.commit()
    conn.close()

def mark_task_complete(task_text_or_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if str(task_text_or_id).isdigit():
        cursor.execute('UPDATE tasks SET status = "completed" WHERE id = ?', (task_text_or_id,))
    else:
        cursor.execute('UPDATE tasks SET status = "completed" WHERE task_text = ?', (task_text_or_id,))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, task_text, due_datetime, status FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks



def get_pending_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, task_text, due_datetime, status FROM tasks WHERE status = "pending"')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_pending_tasks_with_user_info():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, task_text, due_datetime, user_id, username FROM tasks WHERE status = "pending"')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_completed_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, task_text, due_datetime, status FROM tasks WHERE status = "completed"')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_text_or_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if str(task_text_or_id).isdigit():
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_text_or_id,))
    else:
        cursor.execute('DELETE FROM tasks WHERE task_text = ?', (task_text_or_id,))
    conn.commit()
    conn.close()

def get_overdue_tasks():
    
    conn = sqlite3.connect(DB_FILE)
    cursor= conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        SELECT id, task_text, due_datetime, user_id, username 
        FROM tasks
        WHERE status = "pending" AND due_datetime IS NOT NULL AND due_datetime < ?
    ''', (now,))
    overdue_tasks = cursor.fetchall()
    conn.close()
    return overdue_tasks

def increment_streak(user_id, task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if this task was already counted in streak
    cursor.execute("SELECT 1 FROM streak_tasks WHERE task_id = ?", (task_id,))
    if cursor.fetchone():
        conn.close()
        return  # Already counted, don't increment again

    # Add to streak_tasks so we don't double count
    cursor.execute("INSERT INTO streak_tasks (task_id, user_id) VALUES (?, ?)", (task_id, user_id))

    # Now increment streak
    cursor.execute("SELECT streak_count FROM streaks WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE streaks SET streak_count = streak_count + 1 WHERE user_id = ?", (user_id,))
    else:
        cursor.execute("INSERT INTO streaks (user_id, streak_count) VALUES (?, ?)", (user_id, 1))

    conn.commit()
    conn.close()

def get_streak(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT streak_count FROM streaks WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def reset_streak(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM streaks WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def is_user_muted(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM muted_users WHERE user_id = ?', (user_id,))
    is_muted = cursor.fetchone() is not None
    conn.close()
    return is_muted

def mute_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO muted_users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def unmute_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM muted_users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def update_last_roast_time(task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n💾 Updating last roast time for task {task_id} to {current_time}")
    cursor.execute('''
        INSERT OR REPLACE INTO last_roast_times (task_id, last_roast_at)
        VALUES (?, ?)
    ''', (task_id, current_time))
    conn.commit()
    conn.close()

def get_last_roast_time(task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT last_roast_at FROM last_roast_times WHERE task_id = ?', (task_id,))
    row = cursor.fetchone()
    last_roast = row[0] if row else None
    print(f"\n📊 Retrieved last roast time for task {task_id}: {last_roast}")
    conn.close()
    return last_roast

create_table()
