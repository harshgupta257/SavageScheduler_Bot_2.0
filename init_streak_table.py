import sqlite3

DB_FILE = 'tasks.db'  # Update path if needed

def init_streak_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if streaks table exists
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='streaks';
    """)
    result = cursor.fetchone()

    if result:
        print("✅ 'streaks' table already exists.")
    else:
        # Create it if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                user_id INTEGER PRIMARY KEY,
                streak_count INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        print("✅ 'streaks' table created successfully.")

    conn.close()

if __name__ == "__main__":
    init_streak_table()
