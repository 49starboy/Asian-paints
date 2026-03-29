import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient

# ================= CONFIG =================
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

MONGO_URI = os.getenv("MONGO_URI", "")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-100xxxxxxxxxx"))

START_LINK = "https://t.me/ggggtybb/72"

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

# ================= START =================
@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user_id = message.from_user.id

    # Save user
    if not await users_col.find_one({"_id": user_id}):
        await users_col.insert_one({"_id": user_id, "msg_id": 72})

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("Help ⚙️", callback_data="help"),
         InlineKeyboardButton("About ❤️", callback_data="about")]
    ])

    await message.reply_text(
        "👋 Hello!\n\n🤖 Main auto message bot hoon.\n📌 Mujhe group me add karo.",
        reply_markup=btn
    )

# ================= GROUP ADD =================
@app.on_message(filters.group & filters.new_chat_members)
async def bot_added(client, message):
    for user in message.new_chat_members:
        if user.is_self:
            await message.reply_text(
                "✅ Thanks for adding me!\n\nI will auto send messages every 15 sec 🚀"
            )

# ================= AUTO LOOP =================
async def auto_send():
    await app.start()
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

                await app.send_message(LOG_CHANNEL, f"✅ Sent {link} to {user['_id']}")

            except Exception as e:
                print(e)

        await asyncio.sleep(15)

# ================= MAIN =================
async def main():
    await auto_send()

if __name__ == "__main__":
    asyncio.run(main())
