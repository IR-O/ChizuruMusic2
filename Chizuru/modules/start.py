from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified
from Chizuru import Chizuru, BOT_USERNAME
from Chizuru.core.strings import (
    music_txt, ai_txt, bass_txt, youtube_txt,
    misc_txt, broadcast_txt, checker_txt, devs_txt, instagram_txt
)

# ============ Texts ============

start_txt = """
**ʜᴇʟʟᴏ** {} 

**ɪ ᴀᴍ ᴄʜɪᴢᴜʀᴜ, ʏᴏᴜʀ ᴍᴜsɪᴄ ᴠɪʀᴛᴜᴏsᴏ! ɪᴍᴍᴇʀsᴇ ʏᴏᴜʀsᴇʟғ ɪɴ ғʟᴀᴡʟᴇss ʙᴇᴀᴛs ᴡɪᴛʜ ᴢᴇʀᴏ ʟᴀɢ – ɪ'ᴍ ɴᴏᴛ ᴊᴜsᴛ ᴀ ᴍᴜsɪᴄ ʙᴏᴛ; ɪ'ᴍ ᴛʜᴇ sʏᴍᴘʜᴏɴʏ ᴏғ ᴛʜᴇ ғᴜᴛᴜʀᴇ, ᴛᴀɪʟᴏʀᴇᴅ ғᴏʀ ʏᴏᴜʀ ᴍᴜsɪᴄᴀʟ ʙʟɪss.
"""

help_txt = """**
**» ˹ᴄʜɪᴢᴜʀᴜ˼ ᴄᴏᴏʟ ᴏʀ ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs** 
"""

# ============ Keyboards ============

start_button = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [InlineKeyboardButton("↯ ᴄᴏᴍᴍᴀɴᴅs ↯", callback_data="help_")]
])

chizuru_buttons = [
    [
        InlineKeyboardButton("ᴍᴜsɪᴄ", callback_data="music_"),
        InlineKeyboardButton("ᴀɪ", callback_data="ai_"),
        InlineKeyboardButton("ʙᴀss", callback_data="bass_")
    ],
    [
        InlineKeyboardButton("ʏᴏᴜᴛᴜʙᴇ", callback_data="youtube_"),
        InlineKeyboardButton("ᴍɪsᴄ", callback_data="misc_"),
        InlineKeyboardButton("ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="broadcast_")
    ],
    [
        InlineKeyboardButton("ᴄʜᴇᴄᴋᴇʀ", callback_data="checker_"),
        InlineKeyboardButton("ᴅᴇᴠs", callback_data="devs_"),
        InlineKeyboardButton("ɪɴsᴛᴀɢʀᴀᴍ", callback_data="instagram_")
    ],
    [
        InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="home_"),
        InlineKeyboardButton("⟲ ᴄʟᴏꜱᴇ ⟳", callback_data="close_data")
    ]
]

back_buttons = [[
    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="help_")
]]

# ============ Start Command ============

@Chizuru.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_photo(
        "https://te.legra.ph/file/c079d38540f2871c74423.mp4",
        caption=start_txt.format(message.from_user.mention),
        reply_markup=start_button
    )

# ============ Callback Handler ============

@Chizuru.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    try:
        data = query.data

        if data == "home_":
            await query.edit_message_text(
                start_txt.format(query.from_user.mention),
                reply_markup=start_button
            )

        elif data == "help_":
            await query.edit_message_text(
                help_txt,
                reply_markup=InlineKeyboardMarkup(chizuru_buttons)
            )

        elif data in ["music_", "ai_", "bass_", "youtube_", "misc_", "broadcast_", "checker_", "devs_", "instagram_"]:
            text_map = {
                "music_": music_txt,
                "ai_": ai_txt,
                "bass_": bass_txt,
                "youtube_": youtube_txt,
                "misc_": misc_txt,
                "broadcast_": broadcast_txt,
                "checker_": checker_txt,
                "devs_": devs_txt,
                "instagram_": instagram_txt
            }
            await query.edit_message_text(
                text_map[data],
                reply_markup=InlineKeyboardMarkup(back_buttons)
            )

        elif data == "maintainer_":
            await query.answer("sᴏᴏɴ.... \n ʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ", show_alert=True)

        elif data == "close_data":
            try:
                await query.message.delete()
                if query.message.reply_to_message:
                    await query.message.reply_to_message.delete()
            except:
                pass

    except MessageNotModified:
        pass
    except Exception as e:
        print(f"Error in callback: {e}")
