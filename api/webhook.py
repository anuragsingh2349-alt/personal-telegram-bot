import os
import json
import datetime
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, "data", "college.json")) as f:
    COLLEGE = json.load(f)

with open(os.path.join(BASE_DIR, "data", "gym.json")) as f:
    GYM = json.load(f)


def send(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )


def college_today():

    today = datetime.datetime.now().strftime("%A").lower()

    schedule = COLLEGE.get(today, [])

    if not schedule:
        return "🎉 No classes today."

    message = "📚 Today's College Schedule\n\n"

    for subject in schedule:

        message += (
            f"🕒 {subject['time']}\n"
            f"📖 {subject['subject']}\n"
            f"👨‍🏫 {subject['teacher']}\n"
            f"🏫 {subject['room']}\n\n"
        )

    return message


def gym_today():

    today = datetime.datetime.now().strftime("%A").lower()

    workout = GYM.get(today)

    if not workout:
        return "💤 Rest Day"

    return f"💪 Today's Workout\n\n{workout}"


def today():

    return college_today() + "\n----------------------\n\n" + gym_today()


def handler(request):

    if request.method != "POST":
        return {
            "statusCode": 200,
            "body": "Telegram Bot Running"
        }

    data = request.get_json()

    message = data["message"]

    chat_id = message["chat"]["id"]

    text = message["text"].lower()

    if "college" in text:

        send(chat_id, college_today())

    elif "gym" in text:

        send(chat_id, gym_today())

    elif "today" in text:

        send(chat_id, today())

    else:

        send(
            chat_id,
            "Commands:\n\ncollege\ngym\ntoday"
        )

    return {
        "statusCode": 200
    }