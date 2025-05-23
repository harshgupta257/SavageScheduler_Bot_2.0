import sqlite3

DB_FILE = "tasks.db"

def create_missing_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Ensure streaks table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streaks (
            user_id TEXT PRIMARY KEY,
            streak_count INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Ensured 'streaks' table exists.")

def patch_incomplete_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check how many tasks need patching
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE user_id IS NULL OR username IS NULL')
    count = cursor.fetchone()[0]

    if count == 0:
        print("✅ All tasks are already complete.")
        conn.close()
        return

    # Patch incomplete rows with dummy values
    cursor.execute('''
        UPDATE tasks
        SET user_id = 99999, username = 'test_user'
        WHERE user_id IS NULL OR username IS NULL
    ''')

    conn.commit()
    conn.close()
    print(f"🔧 Patched {count} incomplete task(s) with dummy user_id and username.")

def main():
    print("🔁 Starting database fix...")
    create_missing_tables()
    patch_incomplete_tasks()
    print("🎉 All done. You can now safely rerun your bot.")

if __name__ == "__main__":
    main()
