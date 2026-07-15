from bot.schedules import (
    get_today_college_schedule,
    get_today_gym_schedule,
    format_college_schedule,
    format_gym_schedule,
)

from bot.keyboards import build_gym_keyboard

from bot.telegram import (
    edit_message,
    answer_callback,
)

# -------------------------------------------------------------------
# Temporary in-memory workout state.
#
# Structure:
# {
#     chat_id: {0, 2, 4}
# }
#
# Means exercises with index 0,2,4 are completed.
#
# NOTE:
# This resets whenever Vercel creates a new serverless instance.
# That's okay for the MVP.
# -------------------------------------------------------------------
WORKOUT_STATE = {}


def handle_message(chat_id: int, text: str):
    """
    Handle incoming Telegram messages.
    Returns a dictionary for send_message().
    """

    text = text.lower().strip()

    # ---------------------------------------------------------
    # College Schedule
    # ---------------------------------------------------------
    if (
        "/college" in text
        or "college" in text
        or "class" in text
        or "schedule" in text
    ) and "gym" not in text:

        schedule = get_today_college_schedule()

        return {
            "text": format_college_schedule(schedule)
        }

    # ---------------------------------------------------------
    # Gym Schedule
    # ---------------------------------------------------------
    if (
        "/gym" in text
        or "gym" in text
        or "workout" in text
        or "exercise" in text
    ):

        workout = get_today_gym_schedule()

        if (
            workout is None
            or "exercises" not in workout
            or not workout["exercises"]
        ):
            return {
                "text": "😴 *Today is your Rest Day!*\n\nEnjoy your recovery 💪"
            }

        completed = WORKOUT_STATE.get(chat_id, set())

        return {
            "text": format_gym_schedule(workout, completed),
            "reply_markup": build_gym_keyboard(
                workout,
                completed,
            ),
        }

    # ---------------------------------------------------------
    # Help Message
    # ---------------------------------------------------------
    return {
        "text": (
            "🤖 Personal Schedule Bot\n\n"
            "Available commands:\n\n"
            "📚 /college\n"
            "💪 /gym"
        )
    }


def handle_callback(callback: dict):
    """
    Handles button clicks.
    """

    callback_id = callback["id"]

    data = callback["data"]

    message = callback["message"]

    chat_id = message["chat"]["id"]

    message_id = message["message_id"]

    # Remove Telegram loading animation
    answer_callback(callback_id)

    # Ignore unrelated callbacks
    if not data.startswith("gym:"):
        return

    exercise_index = int(data.split(":")[1])

    completed = WORKOUT_STATE.setdefault(chat_id, set())

    # Toggle completion
    if exercise_index in completed:
        completed.remove(exercise_index)
    else:
        completed.add(exercise_index)

    workout = get_today_gym_schedule()

    if workout is None:
        return

    # ---------------------------------------------------------
    # Workout completed?
    # ---------------------------------------------------------
    exercises = workout.get("exercises", [])

    all_done = len(completed) == len(exercises)

    if all_done:

        message_text = (
            "🎉 *Workout Complete!*\n\n"
            "Excellent work today!\n"
            "See you tomorrow 💪"
        )

    else:

        message_text = format_gym_schedule(
            workout,
            completed,
        )

    edit_message(
        chat_id=chat_id,
        message_id=message_id,
        text=message_text,
        reply_markup=build_gym_keyboard(
            workout,
            completed,
        ),
    )