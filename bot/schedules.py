from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

COLLEGE_FILE = DATA_DIR / "college.json"
GYM_FILE = DATA_DIR / "gym.json"

IST = ZoneInfo("Asia/Kolkata")

DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def load_college_schedule():
    with open(COLLEGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_gym_schedule():
    with open(GYM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_today_name():
    return datetime.now(IST).strftime("%A").lower()


def get_college_schedule(day):
    return load_college_schedule().get(day.lower(), [])


def get_gym_schedule(day):
    return load_gym_schedule().get(day.lower())


def get_today_college_schedule():
    return get_college_schedule(get_today_name())


def get_today_gym_schedule():
    return get_gym_schedule(get_today_name())


def format_college_schedule(schedule, title="📚 *College Schedule*"):
    if not schedule:
        return (
            f"{title}\n\n"
            "🎉 No classes scheduled."
        )

    message = f"{title}\n\n"

    for lecture in schedule:
        message += (
            f"🕒 *{lecture['time']}*\n"
            f"📖 {lecture['subject']}\n"
            f"👨‍🏫 {lecture['teacher']}\n"
            f"🏫 {lecture['room']}\n\n"
        )

    return message.strip()


def format_gym_schedule(workout, completed=None, title=None):

    if completed is None:
        completed = set()

    if workout is None:
        return (
            f"{title or '💪 Workout'}\n\n"
            "😴 Rest Day\n\n"
            "Enjoy your recovery 💪"
        )

    exercises = workout.get("exercises", [])

    if not exercises:
        return (
            f"{title or '💪 Workout'}\n\n"
            "😴 Rest Day\n\n"
            "Enjoy your recovery 💪"
        )

    header = title if title else f"💪 *{workout['name']}*"

    message = header + "\n\n"

    for index, exercise in enumerate(exercises):
        if index in completed:
            message += f"✅ {exercise}\n"
        else:
            message += f"⬜ {exercise}\n"

    return message.strip()