from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from typing import Optional

from telegram_async import send_telegram_message
from telegram_updates import get_latest_chat_info
from templates import amen_gym_payment_message
from retry import retry_async

app = FastAPI(title="Amen Gym Telegram Messaging API")

# -----------------------------
# Models
# -----------------------------

class TelegramRequest(BaseModel):
    chat_id: str

class TelegramResponse(BaseModel):
    status: str
    response_time_ms: float

class ChatInfoResponse(BaseModel):
    chat_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

# -----------------------------
# Send Reminder Endpoint
# -----------------------------

@app.post("/send-amen-gym-reminder", response_model=TelegramResponse)
async def send_reminder(payload: TelegramRequest):
    start = time.time()
    message = amen_gym_payment_message()

    try:
        await retry_async(
            lambda: send_telegram_message(
                chat_id=payload.chat_id,
                text=message
            ),
            retries=3,
            base_delay=2
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed after retries: {str(e)}"
        )

    return {
        "status": "Message sent successfully",
        "response_time_ms": round((time.time() - start) * 1000, 2)
    }

# -----------------------------
# Get Latest Chat ID (Registration)
# -----------------------------

@app.get("/telegram/latest-chat", response_model=ChatInfoResponse)
async def get_latest_chat():
    chat_info = await get_latest_chat_info()

    if not chat_info:
        raise HTTPException(
            status_code=404,
            detail="No Telegram chat found. User must click /start first."
        )

    return chat_info
