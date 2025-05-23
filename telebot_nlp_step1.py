import re
from datetime import datetime, timedelta
import dateparser
from dateparser.search import search_dates

def extract_relative_date(text):
    now = datetime.now()
    
    # Handle specific relative expressions
    if "day after tomorrow" in text.lower():
        return now + timedelta(days=2)
    if "tomorrow" in text.lower():
        return now + timedelta(days=1)
    if "yesterday" in text.lower():
        return now - timedelta(days=1)
    if "today" in text.lower():
        return now

    # Handle patterns like "in X days"
    match = re.search(r'in\s+(\d+)\s+days', text, re.IGNORECASE)
    if match:
        days = int(match.group(1))
        return now + timedelta(days=days)

    # Handle patterns like "in X weeks"
    match = re.search(r'in\s+(\d+)\s+weeks', text, re.IGNORECASE)
    if match:
        weeks = int(match.group(1))
        return now + timedelta(weeks=weeks)

    return None

def extract_datetime_custom(text):
    now = datetime.now()

    # First, try regex-based relative extraction (for "in X days/weeks", "tomorrow", etc.)
    relative_date = extract_relative_date(text)
    if relative_date:
        # Check if a specific time is mentioned using regex (e.g., "at 5 AM")
        time_match = re.search(r'at\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)', text, re.IGNORECASE)
        if time_match:
            time_str = time_match.group(1)
            parsed_time = dateparser.parse(time_str)
            if parsed_time:
                return datetime.combine(relative_date.date(), parsed_time.time())
        return datetime.combine(relative_date.date(), datetime.min.time().replace(hour=12))  # Default to 12 PM

    # Handle "next Monday", "next Tuesday", etc.
    match = re.search(r'next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', text, re.IGNORECASE)
    if match:
        day_name = match.group(1).capitalize()
        days_ahead = (list_days.index(day_name) - now.weekday() + 7) % 7# Always picks the nearest upcoming occurrence
        if days_ahead == 0: # If today is the same day, pick next week
            days_ahead=7
        next_week_day = now + timedelta(days=days_ahead)
        
        # Extract time if mentioned
        time_match = re.search(r'at\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)', text, re.IGNORECASE)
        if time_match:
            time_str = time_match.group(1)
            parsed_time = dateparser.parse(time_str)
            if parsed_time:
                return datetime.combine(next_week_day.date(), parsed_time.time())
        
        return datetime.combine(next_week_day.date(), datetime.min.time().replace(hour=12))  # Default to 12 PM

    # Fallback: use search_dates to scan the whole text for date/time expressions
    results = search_dates(text, settings={
        'PREFER_DATES_FROM': 'future',
        'RELATIVE_BASE': now,
        'RETURN_AS_TIMEZONE_AWARE': False
    })
    
    if results:
        extracted_date = results[0][1]
        if extracted_date.time() == datetime.min.time():
            extracted_date = extracted_date.replace(hour=12)  # Default to 12 PM if no time is given
        return extracted_date

    return None

# List of weekdays for lookup
list_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


if __name__ == "__main__":
    # Test cases
    messages = [
        "Remind me to call John day after tomorrow at 5 PM",
        "I have a meeting next wednesday at 2:30 PM",
    ]

    for message in messages:
        result = extract_datetime_custom(message)
        print(f"Input: {message}")
        print(f"Extracted: {result.strftime(r'%Y-%m-%d %H:%M') if result else 'None'}\n")
