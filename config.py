import os

class Config:
    # Telegram API
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "")

    # Log Channel
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", 0))

    # Bot Settings
    START_NUMBER = int(os.getenv("START_NUMBER", 72))
    DELAY = int(os.getenv("DELAY", 15))

    # Base Link
    BASE_LINK = os.getenv("BASE_LINK", "https://t.me/ggggtybb/{}")
