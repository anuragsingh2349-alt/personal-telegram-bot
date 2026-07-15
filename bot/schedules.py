from pathlib import Path
from datetime import datetime
import json

# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

COLLEGE_FILE = DATA_DIR / "college.json"
GYM_FILE = DATA_DIR / "gym.json"


def load_college_schedule() -> dict:
    """
    Load the complete college timetable.
    """
    with open(COLLEGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_gym_schedule() -> dict:
    """
    Load the complete gym schedule.
    """
    with open(GYM_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_today_name() -> str:
    """
    Returns:
        monday
        tuesday
        ...
    """
    return datetime.now().strftime("%A").lower()


def get_today_college_schedule():
    """
    Returns today's college schedule.

    Example:

    [
        {
            "time": "...",
            "subject": "...",
            "teacher": "...",
            "room": "..."
        }
    ]
    """

    timetable = load_college_schedule()

    return timetable.get(get_today_name(), [])


def get_today_gym_schedule():
    """
    Returns today's workout.

    Example:

    {
        "name": "Push A",
        "exercises": [...]
    }
    """

    workouts = load_gym_schedule()

    return workouts.get(get_today_name())


def format_college_schedule(schedule) -> str:
    """
    Convert today's classes into a Telegram-friendly message.
    """

    if not schedule:
        return (
            "🎉 *Today's College Schedule*\n\n"
            "No classes scheduled today."
        )

    message = "📚 *Today's College Schedule*\n\n"

    for lecture in schedule:
        message += (
            f"🕒 *{lecture['time']}*\n"
            f"📖 {lecture['subject']}\n"
            f"👨‍🏫 {lecture['teacher']}\n"
            f"🏫 {lecture['room']}\n\n"
        )

    return message.strip()


def format_gym_schedule(workout, completed=None) -> str:
    """
    Format today's workout while showing completed exercises.
    """

    if completed is None:
        completed = set()

    if workout is None:
        return (
            "😴 *Today's Gym Schedule*\n\n"
            "Rest Day!"
        )

    message = f"💪 *{workout['name']}*\n\n"

    for index, exercise in enumerate(workout["exercises"]):

        if index in completed:
            message += f"✅ {exercise}\n"
        else:
            message += f"⬜ {exercise}\n"

    return message.strip()