import requests
import time
import json
import os
import re
import html
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

LOGIN_URL = "https://placement.iitk.ac.in/api/auth/login"
NOTICE_URL = "https://placement.iitk.ac.in/api/student/rc/14/notice"

USERNAME = os.getenv("EMAIL", "Harsh")
PASSWORD = os.getenv("PASSWORD", "Baid")
SERVER_NAME = os.getenv("SERVER_NAME", "iitk-placement-2025")

def login():
    res = requests.post(LOGIN_URL, json={"user_id": USERNAME, "password": PASSWORD})
    return res.json()["token"]

def get_notices(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(NOTICE_URL, headers=headers)
    return res.json()

def clean_html_text(text):
    if not text:
        return ""
    
    try:
        decoded = text.encode().decode('unicode_escape')
        
        cleaned = html.unescape(decoded)
        
        cleaned = re.sub(r'<br\s*/?>', '\n', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'</p>', '\n\n', cleaned)
        cleaned = re.sub(r'<p[^>]*>', '', cleaned)
        
        cleaned = re.sub(r'<[^>]+>', '', cleaned)
        
        cleaned = re.sub(r'[ \t]+', ' ', cleaned) 
        cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned) 
        cleaned = cleaned.strip()
        
        return cleaned
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return text

def format_timestamp(timestamp_str):
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        formatted = dt.strftime("%b %d, %Y at %I:%M %p")
        return formatted
    except Exception as e:
        print(f"Error formatting timestamp {timestamp_str}: {e}")
        return timestamp_str

def notify(msg):
    requests.post(f"https://ntfy.sh/{os.getenv('SERVER_NAME')}", data=msg.encode())

def is_recent_notice(updated_at_str, minutes=35):
    try:
        updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
        now = datetime.now(updated_at.tzinfo)
        time_diff = now - updated_at
        return time_diff <= timedelta(minutes=minutes)
    except Exception as e:
        print(f"Error parsing date {updated_at_str}: {e}")
        return False

def main():
    token = login()
    seen_ids = set()

    if os.path.exists("seen.json"):
        seen_ids = set(json.load(open("seen.json")))

    while True:
        try:
            notices = get_notices(token)
            recent_notices = [n for n in notices if is_recent_notice(n.get("UpdatedAt", ""))]
            new_recent = [n for n in recent_notices if n["ID"] not in seen_ids]

            for n in new_recent:
                clean_desc = clean_html_text(n.get('description', ''))
                readable_time = format_timestamp(n['UpdatedAt'])
                msg = f"📢 New Notice: {n['title']}\n\n{clean_desc}\n\nReceived at: {readable_time}"
                notify(msg)
                seen_ids.add(n["ID"])

            json.dump(list(seen_ids), open("seen.json", "w"))
            time.sleep(30 * 60)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
