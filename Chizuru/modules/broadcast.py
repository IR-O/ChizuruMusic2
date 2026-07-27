import asyncio
import traceback
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from Chizuru import Chizuru
from config import OWNER_ID
from Chizuru.core.mongo import get_chats, get_users

# Helper function to send message with retry
async def send_msg(user_id: int, message: Message):
    """Send a message to a user/chat with flood wait handling"""
    try:
        await message.copy(chat_id=user_id)
        return True, None
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return False, f"{user_id}: Deactivated account"
    except UserIsBlocked:
        return False, f"{user_id}: Blocked the bot"
    except PeerIdInvalid:
        return False, f"{user_id}: Invalid ID"
    except Exception as e:
        return False, f"{user_id}: {traceback.format_exc()}"

@Chizuru.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_command(_, message: Message):
    """Broadcast a message to all chats and users"""
    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to a message to broadcast.")
        return
    
    status_msg = await message.reply_text("⏳ Starting broadcast...")
    
    # Fetch all chats and users
    all_chats = await get_chats() or {}
    all_users = await get_users() or {}
    
    done_chats = 0
    done_users = 0
    failed_chats = 0
    failed_users = 0
    failed_chat_list = []
    failed_user_list = []
    
    # Broadcast to chats
    for chat_id in all_chats:
        try:
            success, error = await send_msg(chat_id, message.reply_to_message)
            if success:
                done_chats += 1
            else:
                failed_chats += 1
                failed_chat_list.append(error)
            await asyncio.sleep(0.1)  # Rate limit
        except Exception as e:
            failed_chats += 1
            failed_chat_list.append(f"{chat_id}: {str(e)}")
    
    # Broadcast to users
    for user_id in all_users:
        try:
            success, error = await send_msg(user_id, message.reply_to_message)
            if success:
                done_users += 1
            else:
                failed_users += 1
                failed_user_list.append(error)
            await asyncio.sleep(0.1)  # Rate limit
        except Exception as e:
            failed_users += 1
            failed_user_list.append(f"{user_id}: {str(e)}")
    
    # Prepare final message
    final_msg = (
        f"✅ **Broadcast Complete!**\n\n"
        f"📨 **Chats:** {done_chats} successful, {failed_chats} failed\n"
        f"👤 **Users:** {done_users} successful, {failed_users} failed"
    )
    
    if failed_chats > 0 or failed_users > 0:
        final_msg += f"\n\n⚠️ Some errors occurred:\n"
        if failed_chat_list:
            final_msg += f"\n**Chat errors:**\n`{chr(10).join(failed_chat_list[:5])}`"
        if failed_user_list:
            final_msg += f"\n**User errors:**\n`{chr(10).join(failed_user_list[:5])}`"
    
    await status_msg.edit_text(final_msg)

@Chizuru.on_message(filters.command("announce") & filters.user(OWNER_ID))
async def announce_command(_, message: Message):
    """Forward a message to all chats and users"""
    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to a message to announce.")
        return
    
    msg_id = message.reply_to_message.id
    chat_id = message.chat.id
    
    # Fetch all chats and users
    all_chats = await get_chats() or []
    all_users = await get_users() or []
    
    failed_chats = 0
    failed_users = 0
    
    status_msg = await message.reply_text("⏳ Starting announcement...")
    
    # Forward to chats
    for chat in all_chats:
        try:
            await _.forward_messages(
                chat_id=int(chat),
                from_chat_id=chat_id,
                message_ids=msg_id
            )
            await asyncio.sleep(1)  # Rate limit
        except Exception:
            failed_chats += 1
    
    # Forward to users
    for user in all_users:
        try:
            await _.forward_messages(
                chat_id=int(user),
                from_chat_id=chat_id,
                message_ids=msg_id
            )
            await asyncio.sleep(1)  # Rate limit
        except Exception:
            failed_users += 1
    
    await status_msg.edit_text(
        f"✅ **Announcement Complete!**\n\n"
        f"📨 **Chats:** {len(all_chats) - failed_chats} successful, {failed_chats} failed\n"
        f"👤 **Users:** {len(all_users) - failed_users} successful, {failed_users} failed\n\n"
        f"⚠️ Failed due to being kicked or banned."
    )
