import os
import json

from flask import Flask, request, jsonify

import traceback

from bot.telegram import send_message
from bot.handlers import handle_message, handle_callback

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Health check endpoint.
    """
    return jsonify(
        {
            "status": "running",
            "service": "Personal Telegram Bot"
        }
    )


@app.route("/webhook", methods=["POST"])
def webhook():

    print("=" * 60)
    print("WEBHOOK RECEIVED")
    print(request.json)
    print("=" * 60)

    try:

        update = request.get_json()

        if "message" in update:

            message = update["message"]

            chat_id = message["chat"]["id"]

            text = message.get("text", "")

            print("Message:", text)

            response = handle_message(chat_id, text)

            print("Response:", response)

            if response:

                send_message(
                    chat_id=chat_id,
                    **response
                )

        elif "callback_query" in update:

            handle_callback(update["callback_query"])

        return jsonify({"ok": True})

    except Exception:

        traceback.print_exc()

        return jsonify({"ok": False}), 500


# Required by Vercel
app = app