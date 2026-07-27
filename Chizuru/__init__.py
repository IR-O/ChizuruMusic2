import asyncio
import logging
from pyrogram import Client
from pytgcalls import GroupCallFactory  # <-- idle hata diya
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

# Group Call Factory (v3)
group_call_factory = GroupCallFactory(userbot)
group_call = group_call_factory.get_group_call()

async def chizuru_music():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await Chizuru.start()
    await userbot.start()
    getme = await Chizuru.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = getme.first_name + (" " + getme.last_name if getme.last_name else "")
    logging.info(f"Bot started as @{BOT_USERNAME} (ID: {BOT_ID})")
    
    # Voice chat join (example, chat_id aap set karein)
    # await group_call.join(-100123456789)  # <-- Apni GROUP_ID daalein
    logging.info("Bot is ready. Use /play to start music.")
    
    # Keep bot running (idle ka alternative)
    await asyncio.Event().wait()  # <-- Infinite wait

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chizuru_music())
