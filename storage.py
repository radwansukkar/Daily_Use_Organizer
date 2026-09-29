import json
import os
from datetime import date

APP_DATA_DIR = os.path.join(os.environ["LOCALAPPDATA"], "DigitalDetoxEnforcer")
os.makedirs(APP_DATA_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(APP_DATA_DIR, "config.json")
DATA_FILE = os.path.join(APP_DATA_DIR, "usage_data.json")

DEFAULT_CONFIG = {
    "monitored_apps": {
        "notepad.exe": 1
    },
    "poll_interval_sec": 5
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_usage_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_usage_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_today_key():
    return str(date.today())