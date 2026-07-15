import os
import json

from flask import Flask, request, jsonify

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
    """
    Telegram sends every update here.
    """

    update = request.get_json(silent=True)

    if not update:
        return jsonify({"ok": False}), 400

    try:

        # -----------------------------
        # Normal text message
        # -----------------------------
        if "message" in update:

            message = update["message"]

            chat_id = message["chat"]["id"]

            text = message.get("text", "")

            response = handle_message(chat_id, text)

            if response:
                send_message(
                    chat_id=chat_id,
                    **response
                )

        # -----------------------------
        # Inline keyboard callback
        # -----------------------------
        elif "callback_query" in update:

            callback = update["callback_query"]

            handle_callback(callback)

    except Exception as e:

        print(f"Webhook Error: {e}")

    return jsonify({"ok": True})


# Required by Vercel
app = app