import asyncio
import os
import threading
from flask import Flask
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# ================= CONFIG =================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

# ================= DATABASE =================
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo.bot_db
users_col = db.users

# ================= BOT =================
app = Client(
    "auto-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= FLASK =================
web = Flask(__name__)

@web.route("/")
def home():
    return "✅ Bot Running"

# ================= BOT HANDLER =================
@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user_id = message.from_user.id

    if not await users_col.find_one({"_id": user_id}):
        await users_col.insert_one({"_id": user_id, "msg_id": 72})

    await message.reply_text("👋 Bot active hai!")

# ================= AUTO LOOP =================
async def auto_send():
    while True:
        users = users_col.find({})
        async for user in users:
            try:
                msg_id = user.get("msg_id", 72)
                link = f"https://t.me/ggggtybb/{msg_id}"

                await app.send_message(user["_id"], link)

                await users_col.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"msg_id": msg_id + 1}}
                )

            except Exception as e:
                print(e)

        await asyncio.sleep(15)

# ================= BOT RUNNER =================
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def start_all():
        await app.start()
        print("🚀 Bot Started")
        await auto_send()

    loop.run_until_complete(start_all())

# ================= MAIN =================
if __name__ == "__main__":
    # Run bot in separate thread (fixed event loop issue)
    threading.Thread(target=run_bot).start()

    # Run Flask (Render needs this)
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)
