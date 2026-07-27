import os
import random
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import aiohttp
import aiofiles
import ffmpeg

# ============ Helper Functions ============

def make_col():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)

def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

def truncate(text):
    words = text.split(" ")
    text1 = ""
    text2 = ""
    for i in words:
        if len(text1) + len(i) < 27:
            text1 += " " + i
        elif len(text2) + len(i) < 25:
            text2 += " " + i
    text1 = text1.strip()
    text2 = text2.strip()
    return [text1, text2]

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

# ============ Cover Generator ============

async def generate_cover(requested_by, title, views, duration, thumbnail):
    # Download thumbnail
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    # Load images
    image = Image.open("./background.png")
    black = Image.open("tp.sam/core/resources/black.jpg")
    img = Image.open("tp.sam/core/resources/music.png")

    # Process images
    image5 = changeImageSize(1280, 720, img)
    image1 = changeImageSize(1280, 720, image)
    image1 = image1.filter(ImageFilter.BoxBlur(10))
    image11 = changeImageSize(1280, 720, image)
    image1 = image11.filter(ImageFilter.BoxBlur(20))
    image2 = Image.blend(image1, black, 0.6)

    # Add color overlay
    im = image5.convert('RGBA')
    color = make_col()
    data = np.array(im)
    red, green, blue, alpha = data.T
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = color
    image5 = Image.fromarray(data)

    # Create circular image
    image3 = image11.crop((280, 0, 1000, 720))
    lum_img = Image.new('L', [720, 720], 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0, 0), (720, 720)], 0, 360, fill=255, outline="white")
    img_arr = np.array(image3)
    lum_img_arr = np.array(lum_img)
    final_img_arr = np.dstack((img_arr, lum_img_arr))
    image3 = Image.fromarray(final_img_arr)
    image3 = image3.resize((600, 600))

    # Paste onto main image
    image2.paste(image3, (50, 70), mask=image3)
    image2.paste(image5, (0, 0), mask=image5)

    # Fonts
    font1 = ImageFont.truetype('tp.sam/core/resources/robot.otf', 30)
    font2 = ImageFont.truetype('tp.sam/core/resources/robot.otf', 60)
    font3 = ImageFont.truetype('tp.sam/core/resources/robot.otf', 49)
    font4 = ImageFont.truetype('tp.sam/core/resources/chizuru.ttf', 35)

    # Draw text
    image4 = ImageDraw.Draw(image2)
    image4.text((10, 10), "ᴛᴘ.sᴀᴍ", fill="white", font=font1, align="left")
    image4.text((670, 150), "NOW PLAYING", fill="white", font=font2, stroke_width=2, stroke_fill="white", align="left")

    title1 = truncate(title)
    image4.text((670, 280), text=title1[0], fill="white", font=font3, align="left")
    image4.text((670, 332), text=title1[1], fill="white", font=font3, align="left")

    views = f"Views : {views}"
    duration = f"Duration : {duration} minutes"
    channel = f"Channel : T-Series"

    image4.text((670, 410), text=views, fill="white", font=font4, align="left")
    image4.text((670, 460), text=duration, fill="white", font=font4, align="left")
    image4.text((670, 510), text=channel, fill="white", font=font4, align="left")

    # Save final image
    image2.save("final.png")
    os.remove("background.png")
    return "temp.png"
