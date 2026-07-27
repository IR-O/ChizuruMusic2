import os
import random
import re
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Chizuru import Chizuru, userbot
from Chizuru.core.admin_func import authorized_users
from Chizuru.core import utils as rq
from Chizuru.core.utils import DurationLimitError, get_audio_stream, get_video_stream
from Chizuru.core.thumb_func import generate_cover
from youtube_search import YoutubeSearch
from pyrogram.errors import UserAlreadyParticipant
from pytgcalls import Update
from pytgcalls.types import AudioPiped, AudioVideoPiped, AudioQuality, AudioParameters

# ============ Constants ============

DURATION_LIMIT = 300
que = {}
chat_id = None
useer = "NaN"

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(" ᴄʟᴏsᴇ ", callback_data="close_data")]
])

local_thumb = [
    "https://te.legra.ph/file/96773cc6d6b818a1942b3.jpg",
    "https://te.legra.ph/file/96773cc6d6b818a1942b3.jpg",
    "https://te.legra.ph/file/96773cc6d6b818a1942b3.jpg",
    "https://te.legra.ph/file/96773cc6d6b818a1942b3.jpg",
]

# ============ Helper Functions ============

async def join_assistant(chat_id, msg):
    """Helper to join assistant to group"""
    try:
        user = await userbot.get_me()
        await Chizuru.get_chat_member(chat_id, user.id)
    except:
        try:
            invitelink = await Chizuru.export_chat_invite_link(chat_id)
        except Exception:
            await msg.edit_text("**» ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғɪʀsᴛ.**")
            return False
        try:
            await userbot.join_chat(invitelink)
            await userbot.send_message(chat_id, text="** ✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        except UserAlreadyParticipant:
            pass
        except Exception:
            await msg.edit_text("**ᴘʟᴇᴀsᴇ ᴍᴀɴᴜᴀʟʟʏ ᴀᴅᴅ ᴀssɪsᴛᴀɴᴛ.**")
            return False
    return True

# ============ Play Command ============

@Chizuru.on_message(filters.command(["play"], prefixes=["/", "."]))
async def play(_, message: Message):
    global que
    chat_id = message.chat.id
    user_name = message.from_user.mention
    msg = await message.reply("🕊️")

    if not await join_assistant(chat_id, msg):
        return

    audio = ((message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(f"** sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**")

        file_path = await message.reply_to_message.download()
        title = audio.file_name
        link = "https://t.me/ChizuruMusicBot"
        thumbnail = random.choice(local_thumb)
        duration = round(audio.duration / 60)
        views = "Locally added"
        await generate_cover(user_name, title, views, duration, thumbnail)

    else:
        if len(message.command) < 2:
            await msg.edit_text("💌 **ᴜsᴀɢᴇ: /ᴘʟᴀʏ ɢɪᴠᴇ ᴀ ᴛɪᴛʟᴇ sᴏɴɢ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
            return
        else:
            await msg.edit_text("▓▓▓▓▓▓▓▓▓▓▓100%\n\n**⇆ ᴘʀᴏᴄᴇssɪɴɢ...**")

        query = message.text.split(None, 1)[1]

        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            views = results[0]["views"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception:
            await msg.edit("**sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ, ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ sᴏɴɢ ɴᴀᴍᴇ.**")
            return

        if (dur / 60) > DURATION_LIMIT:
            await msg.edit(f"**sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**")
            return

        await generate_cover(user_name, title, views, duration, thumbnail)
        file_path = await get_audio_stream(link)

    ACTV_CALLS = []
    for x in Chizuru.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))

    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n**​🏷️ ɴᴀᴍᴇ :**[{title[:15]}]({link})\n⏰** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏᴇ : **{user_name}",
            reply_markup=keyboard,
        )
    else:
        await Chizuru.pytgcalls.join_group_call(
            chat_id,
            AudioPiped(
                file_path,
                AudioParameters.from_quality(AudioQuality.STUDIO),
            ),
        )
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({link})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{user_name}\n",
        )

    os.remove("final.png")
    return await msg.delete()

# ============ Video Play Command ============

@Chizuru.on_message(filters.command(["vplay"], prefixes=["/", "."]))
async def vplay(_, message: Message):
    global que
    chat_id = message.chat.id
    user_name = message.from_user.mention
    msg = await message.reply("🕊️")

    if not await join_assistant(chat_id, msg):
        return

    video = (message.reply_to_message.video if message.reply_to_message else None)

    if video:
        if round(video.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(f"** sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**")

        file_path = await message.reply_to_message.download()
        title = video.file_name
        link = "https://t.me/ChizuruMusicBot"
        thumbnail = random.choice(local_thumb)
        duration = round(video.duration / 60)
        views = "Locally added"
        await generate_cover(user_name, title, views, duration, thumbnail)

    else:
        if len(message.command) < 2:
            await msg.edit_text("💌 **ᴜsᴀɢᴇ: /vᴘʟᴀʏ ɢɪᴠᴇ ᴀ ᴛɪᴛʟᴇ sᴏɴɢ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
            return
        else:
            await msg.edit_text("▓▓▓▓▓▓▓▓▓▓▓100%\n\n**⇆ ᴘʀᴏᴄᴇssɪɴɢ...**")

        query = message.text.split(None, 1)[1]

        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            views = results[0]["views"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception:
            await msg.edit("**sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ, ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ sᴏɴɢ ɴᴀᴍᴇ.**")
            return

        if (dur / 60) > DURATION_LIMIT:
            await msg.edit(f"**sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**")
            return

        await generate_cover(user_name, title, views, duration, thumbnail)
        file_path = await get_video_stream(link)

    ACTV_CALLS = []
    for x in Chizuru.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))

    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n**​🏷️ ɴᴀᴍᴇ :**[{title[:15]}]({link})\n⏰** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏᴇ : **{user_name}",
            reply_markup=keyboard,
        )
    else:
        await Chizuru.pytgcalls.join_group_call(
            chat_id,
            AudioVideoPiped(file_path)
        )
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({link})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{user_name}\n",
        )

    os.remove("final.png")
    return await msg.delete()

# ============ Skip Command ============

@Chizuru.on_message(filters.command(["skip", "next"], prefixes=["/", "!"]))
async def skip(_, message: Message):
    chat_id = message.chat.id
    ACTV_CALLS = [int(x.chat_id) for x in Chizuru.pytgcalls.active_calls]

    if chat_id not in ACTV_CALLS:
        await message.reply_text("**ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ᴛᴏ sᴋɪᴘ.**")
    else:
        rq.task_done(chat_id)
        if rq.is_empty(chat_id):
            await Chizuru.pytgcalls.leave_group_call(chat_id)
        else:
            await Chizuru.pytgcalls.change_stream(
                chat_id,
                AudioPiped(rq.get(chat_id)["file"]),
            )
            await message.reply_text("**ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴋɪᴘᴘᴇᴅ ᴛʜᴇ sᴏɴɢ.**")

# ============ Stream End Handler ============

@Chizuru.pytgcalls.on_stream_end()
async def on_stream_end(_, update: Update) -> None:
    chat_id = update.chat_id
    rq.task_done(chat_id)
    if rq.is_empty(chat_id):
        await Chizuru.pytgcalls.leave_group_call(chat_id)
    else:
        await Chizuru.pytgcalls.change_stream(
            chat_id,
            AudioPiped(rq.get(chat_id)["file"]),
        )

# ============ Join Command ============

@Chizuru.on_message(filters.command("join"))
@authorized_users
async def join_userbot(_, msg):
    chat_id = msg.chat.id
    invitelink = await Chizuru.export_chat_invite_link(chat_id)
    await userbot.join_chat(invitelink)
    await msg.reply("**ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴ.**")

# ============ Pause Command ============

@Chizuru.on_message(filters.command(["pause"], prefixes=["/", "!"]))
@authorized_users
async def pause(_, msg):
    chat_id = msg.chat.id
    if str(chat_id) in str(Chizuru.pytgcalls.active_calls):
        await Chizuru.pytgcalls.pause_stream(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴘᴀᴜsᴇᴅ\nᴘᴀᴜsᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ᴘᴀᴜsᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇʀᴇ ɪs ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")

# ============ Resume Command ============

@Chizuru.on_message(filters.command(["resume"], prefixes=["/", "!"]))
@authorized_users
async def resume(_, msg):
    chat_id = msg.chat.id
    if str(chat_id) in str(Chizuru.pytgcalls.active_calls):
        await Chizuru.pytgcalls.resume_stream(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴜᴍᴇ\nʀᴇsᴜᴍᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ʀᴇsᴜᴍᴇ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇʀᴇ ɪs ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")

# ============ End Command ============

@Chizuru.on_message(filters.command(["end"], prefixes=["/", "!"]))
@authorized_users
async def stop(_, msg):
    chat_id = msg.chat.id
    if str(chat_id) in str(Chizuru.pytgcalls.active_calls):
        await Chizuru.pytgcalls.leave_group_call(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴅᴇᴅ sᴏɴɢ\nᴇɴᴅᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ᴇɴᴅ ᴍᴜsɪᴄ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")

# ============ Leave VC Command ============

@Chizuru.on_message(filters.command(["leavevc"], prefixes=["/", "!"]))
@authorized_users
async def leavevc(_, msg):
    chat_id = msg.chat.id
    await Chizuru.pytgcalls.leave_group_call(chat_id)
    await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇᴀᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\nʟᴇᴀᴠᴇᴅ ʙʏ {msg.from_user.mention}")

# ============ Volume Command ============

@Chizuru.on_message(filters.command("volume", prefixes="/"))
@authorized_users
async def change_volume(client, message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) == 2 and args[1].isdigit():
        volume = int(args[1])
        await Chizuru.pytgcalls.change_volume_call(chat_id, volume)
        await message.reply(f"ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ {volume}%")
    else:
        await message.reply("ᴜsᴀɢᴇ: /volume [0-200]")
