import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def get_latest_chat_info():
    url = f"{BASE_URL}/getUpdates"

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    if not data.get("ok") or not data.get("result"):
        return None

    last_update = data["result"][-1]
    message = last_update.get("message")

    if not message:
        return None

    chat = message.get("chat", {})
    user = message.get("from", {})

    return {
        "chat_id": chat.get("id"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "username": user.get("username")
    }
