import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask
from threading import Thread

# ================= CONFIG =================
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", 0))

BASE_LINK = "https://t.me/ggggtybb/{}"

# ================= BOT =================
app = Client(
    "auto_link_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= DATABASE =================
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo["auto_bot"]
col = db["users"]

# ================= WEB SERVER =================
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running 🚀"

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

# ================= BUTTONS =================
def start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Help ⚙️", callback_data="help"),
            InlineKeyboardButton("About ❤️", callback_data="about")
        ],
        [
            InlineKeyboardButton("Premium 💳", callback_data="premium"),
            InlineKeyboardButton("Refer 🪙", callback_data="refer")
        ]
    ])

# ================= BOT LOGIC =================
running_users = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    await col.update_one(
        {"_id": user_id},
        {"$set": {"number": 72}},
        upsert=True
    )

    running_users[user_id] = True

    text = f"""
**HEY {name}, Welcome 👋**

I AM AUTO LINK SENDER BOT 🤖  
I WILL SEND LINKS EVERY 15 SEC ⏱️  

😍
🌿 **MAINTAINED BY : STAR BOY**
"""

    await message.reply_text(text, reply_markup=start_buttons())

    await client.send_message(LOG_CHANNEL, f"🟢 User Started: {user_id}")

    # AUTO LINK LOOP
    while running_users.get(user_id):
        data = await col.find_one({"_id": user_id})
        num = data.get("number", 72)

        link = BASE_LINK.format(num)

        try:
            await message.reply_text(f"📩 {link}")
        except:
            break

        await col.update_one(
            {"_id": user_id},
            {"$set": {"number": num + 1}}
        )

        await asyncio.sleep(15)

@app.on_message(filters.command("stop"))
async def stop(client, message):
    user_id = message.from_user.id
    running_users[user_id] = False

    await message.reply_text("❌ Stopped!")
    await client.send_message(LOG_CHANNEL, f"🔴 User Stopped: {user_id}")

# ================= CALLBACK BUTTONS =================
@app.on_callback_query()
async def callbacks(client, query):
    data = query.data

    if data == "help":
        await query.message.edit_text("⚙️ Help:\n/start = Start\n/stop = Stop")

    elif data == "about":
        await query.message.edit_text("❤️ About:\nAuto Link Sender Bot")

    elif data == "premium":
        await query.message.edit_text("💳 Premium:\nContact Admin")

    elif data == "refer":
        await query.message.edit_text("🪙 Refer:\nInvite friends")

# ================= START =================
def run_bot():
    app.run()

if __name__ == "__main__":
    Thread(target=run_web).start()
    run_bot()
