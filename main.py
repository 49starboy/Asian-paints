import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from motor.motor_asyncio import AsyncIOMotorClient

app = Client(
    "auto-link-bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

mongo = AsyncIOMotorClient(Config.MONGO_URI)
db = mongo.bot
users = db.users


# START COMMAND (PRIVATE)
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("Help ⚙️", callback_data="help")]
    ])

    await message.reply_text(
        "👋 Hello!\n\n👉 Mujhe group me add karo aur main automatic links send karunga 🔥",
        reply_markup=buttons
    )


# BOT ADDED IN GROUP
@app.on_message(filters.new_chat_members)
async def bot_added(client, message):
    for member in message.new_chat_members:
        if member.id == (await client.get_me()).id:
            await message.reply_text(
                "✅ Thanks for adding me!\n\n🚀 Auto link system start ho gaya!"
            )

            # Start auto sending
            asyncio.create_task(auto_send(message.chat.id))


# AUTO SEND FUNCTION
async def auto_send(chat_id):
    number = Config.START_NUMBER

    while True:
        link = Config.BASE_LINK.format(number)

        try:
            await app.send_message(chat_id, link)
            number += 1
            await asyncio.sleep(Config.DELAY)
        except Exception as e:
            print(e)
            break


# RUN BOT
app.run()
