import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set.")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(
    chat_id: int,
    text: str,
    reply_markup: dict | None = None,
    parse_mode: str = "Markdown",
):
    """
    Send a new message to Telegram.
    """

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    response = requests.post(
        f"{BASE_URL}/sendMessage",
        json=payload,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def edit_message(
    chat_id: int,
    message_id: int,
    text: str,
    reply_markup: dict | None = None,
    parse_mode: str = "Markdown",
):
    """
    Edit an existing Telegram message.
    """

    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    response = requests.post(
        f"{BASE_URL}/editMessageText",
        json=payload,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def answer_callback(callback_query_id: str, text: str = ""):
    """
    Removes the loading animation after a button click.
    """

    payload = {
        "callback_query_id": callback_query_id,
        "text": text,
    }

    response = requests.post(
        f"{BASE_URL}/answerCallbackQuery",
        json=payload,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def set_webhook(webhook_url: str):
    """
    Register Telegram webhook.
    Run this once after deployment.
    """

    payload = {
        "url": webhook_url,
    }

    response = requests.post(
        f"{BASE_URL}/setWebhook",
        json=payload,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def delete_webhook():
    """
    Remove Telegram webhook.
    Useful during testing.
    """

    response = requests.post(
        f"{BASE_URL}/deleteWebhook",
        timeout=15,
    )

    response.raise_for_status()

    return response.json()