import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

app = Client(
    "bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# START COMMAND
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    bot = await client.get_me()
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{bot.username}?startgroup=true")]
    ])

    await message.reply_text(
        "👋 Mujhe group me add karo 🔥",
        reply_markup=buttons
    )


# BOT ADDED IN GROUP
@app.on_message(filters.new_chat_members)
async def added(client, message):
    bot = await client.get_me()

    for user in message.new_chat_members:
        if user.id == bot.id:
            await message.reply_text("✅ Bot started in group 🚀")
            asyncio.create_task(auto_send(message.chat.id))


# AUTO SEND
async def auto_send(chat_id):
    number = Config.START_NUMBER

    while True:
        try:
            link = Config.BASE_LINK.format(number)
            await app.send_message(chat_id, link)
            number += 1
            await asyncio.sleep(Config.DELAY)
        except Exception as e:
            print(e)
            break


# RUN
async def main():
    await app.start()
    print("Bot Started ✅")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
