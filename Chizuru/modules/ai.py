import asyncio
import base64
import mimetypes
import os
import aiohttp
from pyrogram import filters, types as t
from Chizuru import Chizuru

# Configuration - Apni API key yahan daalein
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Optional
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Optional

# Available models (without external dependencies)
AVAILABLE_MODELS = {
    "gpt": "gpt-3.5-turbo",
    "gemini": "gemini-pro",
    "bard": "bard",  # Legacy support
    "llama": "llama2",
    "mistral": "mistral",
    "palm": "palm2"
}

async def ChatCompletion(prompt, model) -> str:
    """Simple chat completion without external dependencies"""
    try:
        # Mock response for demo (Replace with actual API calls)
        if model == "gemini" and GEMINI_API_KEY:
            return await gemini_chat(prompt)
        elif model == "gpt" and OPENAI_API_KEY:
            return await openai_chat(prompt)
        else:
            # Fallback mock response
            return f"AI response for '{prompt}' (Model: {model})"
    except Exception as E:
        raise Exception(f"API error: {E}")

async def openai_chat(prompt):
    """OpenAI API call"""
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        ) as resp:
            result = await resp.json()
            return result["choices"][0]["message"]["content"]

async def gemini_chat(prompt):
    """Google Gemini API call"""
    async with aiohttp.ClientSession() as session:
        params = {"key": GEMINI_API_KEY}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        async with session.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params=params,
            json=data
        ) as resp:
            result = await resp.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]

async def geminiVision(prompt, model, images) -> str:
    """Vision API for images"""
    # Simple implementation without external dependencies
    return f"Vision analysis for '{prompt}' with {len(images)} images"

def getMedia(message):
    """Extract Media"""
    media = message.media if message.media else message.reply_to_message.media if message.reply_to_message else None
    if message.media:
        if message.photo:
            media = message.photo
        elif message.document and message.document.mime_type in ['image/png','image/jpg','image/jpeg'] and message.document.file_size < 5242880:
            media = message.document
        else:
            media = None
    elif message.reply_to_message and message.reply_to_message.media:
        if message.reply_to_message.photo:
            media = message.reply_to_message.photo
        elif message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png','image/jpg','image/jpeg'] and message.reply_to_message.document.file_size < 5242880:
            media = message.reply_to_message.document
        else:
            media = None
    else:
        media = None
    return media

def getText(message):
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

@Chizuru.on_message(filters.command(["gpt","bard","llama","mistral","palm","gemini","ai"]))
async def chatbots(_, m: t.Message):
    prompt = getText(m)
    media = getMedia(m)
    
    if media is not None:
        return await askAboutImage(_, m, [media], prompt)
    
    if prompt is None:
        return await m.reply_text("Hello! How can I assist you today?")
    
    model = m.command[0].lower()
    try:
        output = await ChatCompletion(prompt, model)
        await m.reply_text(output[:4096])  # Telegram limit
    except Exception as e:
        await m.reply_text(f"Error: {str(e)}")

async def askAboutImage(_, m: t.Message, mediaFiles: list, prompt: str):
    images = []
    for media in mediaFiles:
        image = await _.download_media(media.file_id, file_name=f'./downloads/{m.from_user.id}_ask.jpg')
        images.append(image)
    
    output = await geminiVision(prompt if prompt else "whats this?", "geminiVision", images)
    await m.reply_text(output[:4096])
