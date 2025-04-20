# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Alert(BaseModel):
    temperature: float
    message: str

@app.post("/send-alert")
async def send_alert(alert: Alert):
    email = EmailMessage()
    email["From"] = os.getenv("EMAIL_USER")
    email["To"] = os.getenv("EMAIL_TO")
    email["Subject"] = "Fridge Temperature Alert"
    email.set_content(f"{alert.message} Current temp: {alert.temperature}°F")

    try:
        await aiosmtplib.send(
            email,
            hostname=os.getenv("EMAIL_HOST"),
            port=int(os.getenv("EMAIL_PORT")),
            username=os.getenv("EMAIL_USER"),
            password=os.getenv("EMAIL_PASSWORD"),
            start_tls=True,
        )
        return {"status": "sent"}
    except Exception as e:
        return {"status": "error", "details": str(e)}