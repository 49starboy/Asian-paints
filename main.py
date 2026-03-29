import asyncio
import os
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Fix for Python 3.11+
asyncio.set_event_loop(asyncio.new_event_loop())

# ENV VARIABLES
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

START_NUMBER = int(os.getenv("START_NUMBER", "72"))
DELAY = int(os.getenv("DELAY", "15"))
BASE_LINK = os.getenv("BASE_LINK", "https://t.me/ggggtybb/{}")

# APP
app = Client(
    "auto-link-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# START (PRIVATE)
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    bot = await client.get_me()

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{bot.username}?startgroup=true")]
    ])

    await message.reply_text(
        "👋 Hello!\n\n👉 Mujhe group me add karo, main automatic links bhejunga 🔥",
        reply_markup=buttons
    )


# BOT ADDED IN GROUP
@app.on_message(filters.new_chat_members)
async def added(client, message):
    bot = await client.get_me()

    for user in message.new_chat_members:
        if user.id == bot.id:
            await message.reply_text("✅ Bot activated in this group 🚀")

            # start auto sending
            asyncio.create_task(auto_send(message.chat.id))


# AUTO SEND FUNCTION
async def auto_send(chat_id):
    number = START_NUMBER

    while True:
        try:
            link = BASE_LINK.format(number)
            await app.send_message(chat_id, link)
            number += 1
            await asyncio.sleep(DELAY)
        except Exception as e:
            print(e)
            break


# RUN
async def main():
    await app.start()
    print("Bot Started Successfully 🚀")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
