def build_gym_keyboard(workout: dict, completed: set | None = None) -> dict:
    """
    Build Telegram inline keyboard using raw JSON.

    Returns:
    {
        "inline_keyboard": [
            [
                {
                    "text": "☑️ Bench Press",
                    "callback_data": "gym:0"
                }
            ]
        ]
    }
    """

    if completed is None:
        completed = set()

    keyboard = []

    exercises = workout.get("exercises", [])

    for index, exercise in enumerate(exercises):

        if index in completed:
            button_text = f"✅ {exercise}"
        else:
            button_text = f"☑️ {exercise}"

        keyboard.append(
            [
                {
                    "text": button_text,
                    "callback_data": f"gym:{index}"
                }
            ]
        )

    return {
        "inline_keyboard": keyboard
    }