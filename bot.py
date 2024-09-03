import os
from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip
import pytesseract
from pyrogram import Client

api_id = int(os.getenv("API_ID" , 22505271 ))
api_hash = os.getenv("API_HASH", "c89a94fcfda4bc06524d0903977fc81e")
bot_token = os.getenv("BOT_TOKEN")

app = Client("watermark_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Configure paths and fonts for watermarking
WATERMARK_TEXT = "© DarkysEx"
FONT_PATH = "/path/to/font.ttf"  # Ensure you have a TTF font file
FONT_SIZE = 30

@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await message.reply("Send me an image or video to add a watermark and auto-generate captions!")

@app.on_message(filters.photo & filters.private)
async def watermark_image(client: Client, message: Message):
    # Download the image
    photo_path = await message.download()

    # Open the image and apply the watermark
    image = Image.open(photo_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    textwidth, textheight = draw.textsize(WATERMARK_TEXT, font)

    # Position the watermark at the bottom right corner
    width, height = image.size
    x, y = width - textwidth - 10, height - textheight - 10
    draw.text((x, y), WATERMARK_TEXT, font=font, fill=(255, 255, 255))

    # Save and send the watermarked image
    watermarked_image_path = "watermarked_image.jpg"
    image.save(watermarked_image_path)
    await message.reply_photo(photo=watermarked_image_path)

    # Optionally, add auto-generated caption using OCR (for existing text in the image)
    caption_text = pytesseract.image_to_string(image)
    await message.reply_text(caption_text)

    # Clean up files
    os.remove(photo_path)
    os.remove(watermarked_image_path)

@app.on_message(filters.video & filters.private)
async def watermark_video(client: Client, message: Message):
    # Download the video
    video_path = await message.download()

    # Open the video and apply the watermark
    clip = VideoFileClip(video_path)
    w, h = clip.size

    # Define watermark position and size
    watermark = TextClip(WATERMARK_TEXT, fontsize=FONT_SIZE, color='white', font=FONT_PATH)
    watermark = watermark.set_position(('right', 'bottom')).set_duration(clip.duration)

    # Overlay watermark on video
    video = CompositeVideoClip([clip, watermark])

    # Save the watermarked video
    watermarked_video_path = "watermarked_video.mp4"
    video.write_videofile(watermarked_video_path)

    await message.reply_video(video=watermarked_video_path)

    # Clean up files
    os.remove(video_path)
    os.remove(watermarked_video_path)

# Start the bot
app.run()
