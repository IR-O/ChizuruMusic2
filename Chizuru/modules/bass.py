import os
import pydub
from pyrogram import filters, types as t
from Chizuru import Chizuru

# Temporary file path
TEMP_AUDIO_PATH = "temp_audio.mp3"

async def process_audio(message: t.Message, effect_type: str, effect_value: int = 10):
    """Generic audio processing function"""
    try:
        reply_message = message.reply_to_message
        
        if not reply_message or not reply_message.audio:
            return await message.reply("❌ Please reply to an audio file.")
        
        # Initial status
        msg = await message.reply("⏳ Processing audio...")
        
        # Download audio
        audio_path = await reply_message.download()
        if not audio_path:
            await msg.edit("❌ Failed to download audio.")
            return
        
        # Load audio
        audio_segment = pydub.AudioSegment.from_file(audio_path)
        
        # Apply effect based on type
        if effect_type == "bass":
            await msg.edit("🎵 Adding bass boost...")
            enhanced_audio = audio_segment + effect_value
        elif effect_type == "loudly":
            await msg.edit("🔊 Making audio louder...")
            enhanced_audio = audio_segment + effect_value
        elif effect_type == "mono":
            await msg.edit("🎧 Converting to mono...")
            mono_tracks = audio_segment.split_to_mono()
            enhanced_audio = mono_tracks[0] if mono_tracks else audio_segment
        else:
            await msg.edit("❌ Unknown effect type.")
            return
        
        # Export modified audio
        output_path = f"{message.from_user.id}_output.mp3"
        enhanced_audio.export(output_path, format="mp3")
        
        await msg.edit("📤 Uploading modified audio...")
        
        # Send modified audio
        await message.reply_audio(
            output_path,
            caption=f"✅ {effect_type.capitalize()} effect applied!",
            performer="Chizuru Music Bot"
        )
        
        # Cleanup
        await msg.delete()
        try:
            os.remove(audio_path)
            os.remove(output_path)
        except:
            pass
            
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

@Chizuru.on_message(filters.command("bass") & filters.reply)
async def add_bass(client, message: t.Message):
    """Add bass boost to audio"""
    await process_audio(message, "bass", 10)

@Chizuru.on_message(filters.command("loudly") & filters.reply)
async def make_louder(client, message: t.Message):
    """Make audio louder"""
    await process_audio(message, "loudly", 15)

@Chizuru.on_message(filters.command("mono") & filters.reply)
async def convert_to_mono(client, message: t.Message):
    """Convert stereo to mono"""
    await process_audio(message, "mono")

# Optional: Combined effect command
@Chizuru.on_message(filters.command("bassboost") & filters.reply)
async def bass_boost(client, message: t.Message):
    """Add bass boost with custom intensity"""
    try:
        args = message.text.split()
        boost_level = int(args[1]) if len(args) > 1 and args[1].isdigit() else 10
        await process_audio(message, "bass", min(boost_level, 30))  # Max 30dB boost
    except:
        await process_audio(message, "bass", 10)
