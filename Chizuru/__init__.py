import asyncio
import logging
from pyrogram import Client
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

# Logging setup
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

# Bot Client
Chizuru = Client(
    ":Chizuru:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Userbot Client
userbot = Client(
    ":userbot:",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

# PyTgCalls (v2 compatible)
pytgcalls = PyTgCalls(userbot)

async def chizuru_music():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await Chizuru.start()
    await userbot.start()
    await pytgcalls.start()
    getme = await Chizuru.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = getme.first_name + (" " + getme.last_name if getme.last_name else "")
    logging.info(f"Bot started as @{BOT_USERNAME} (ID: {BOT_ID})")
    
    # Keep bot running
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chizuru_music())
