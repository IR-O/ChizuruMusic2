import os
import asyncio
import requests
import wget
import yt_dlp
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru

# ============ Video Download ============

ydl_opts_video = {
    "format": "best",
    "keepvideo": True,
    "prefer_ffmpeg": False,
    "geo_bypass": True,
    "outtmpl": "%(title)s.%(ext)s",
    "quiet": True,
}

@Chizuru.on_message(filters.command("video"))
async def vsong(client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("💌 **ᴜsᴀɢᴇ: /ᴠɪᴅᴇᴏ [ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴏʀ sᴏɴɢ ɴᴀᴍᴇ]**")
        return

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
        user_mention = message.from_user.mention
    except Exception as e:
        print(e)
        await message.reply_text("**⚠️ ɴᴏ ʀᴇsᴜʟᴛs ᴡᴇʀᴇ ғᴏᴜɴᴅ. ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ sᴏɴɢ ɴᴀᴍᴇ**")
        return

    msg = await message.reply("🕊️")
    try:
        with YoutubeDL(ydl_opts_video) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **Error:** {e}")

    preview = wget.download(thumbnail)
    await msg.edit("**ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇᴅ.\n ɴᴏᴡ ᴜᴘʟᴏᴀᴅɪɴɢ.**")
    title = ytdl_data.get("title", "Unknown")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data.get("duration", 0)),
        thumb=preview,
        caption=f"{title}\n**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ {user_mention}**"
    )

    await msg.delete()
    try:
        os.remove(file_name)
        os.remove(thumb_name)
        os.remove(preview)
    except Exception as e:
        print(e)

# ============ Audio Download ============

ydl_opts_audio = {
    "format": "bestaudio[ext=m4a]",
    "outtmpl": "%(title)s.%(ext)s",
    "quiet": True,
}

@Chizuru.on_message(filters.command("song"))
async def download_song(_, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("💌 **ᴜsᴀɢᴇ: /sᴏɴɢ [ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴏʀ sᴏɴɢ ɴᴀᴍᴇ]**")
        return

    m = await message.reply("🕊️")
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        user_mention = message.from_user.mention
    except Exception as e:
        await m.edit("**⚠️ ɴᴏ ʀᴇsᴜʟᴛs ᴡᴇʀᴇ ғᴏᴜɴᴅ. ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ sᴏɴɢ ɴᴀᴍᴇ**")
        print(str(e))
        return

    await m.edit("**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
    try:
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info_dict)

        # Convert duration to seconds
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60

        await m.edit("**📤 ᴜᴘʟᴏᴀᴅɪɴɢ...**")
        await message.reply_audio(
            audio_file,
            thumb=thumb_name,
            title=title,
            caption=f"{title}\n**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ {user_mention}**",
            duration=dur
        )
        await m.delete()
    except Exception as e:
        await m.edit("❌ An error occurred!")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
