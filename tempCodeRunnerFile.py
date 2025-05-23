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