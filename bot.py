import logging
import yt_dlp as ytdl
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram Bot API token
TELEGRAM_API_TOKEN = '7332398186:AAHG5L3MF-8BtP4ouR_9a_T2tBgje_GegN0'

# Define the command to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Send me a TikTok video link, and I\'ll download it for you.')

# Function to fetch the video file using yt-dlp
async def download_video(url: str) -> str:
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best',  # Download the best quality available
            'outtmpl': './%(id)s.%(ext)s',  # Save file with video ID as filename
            'quiet': True,  # Suppress output
        }

        # Use yt-dlp to download the video
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  # This downloads the video
            video_filename = f"{info_dict['id']}.mp4"
            return video_filename
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None

# Function to handle incoming messages (downloads and sends videos)
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    if 'tiktok.com' in user_message:
        try:
            # Download the video using yt-dlp
            video_filename = await download_video(user_message)

            if video_filename:
                # Send video to the user
                with open(video_filename, 'rb') as video_file:
                    await update.message.reply_video(video_file)
                
                # Optionally delete the video file after sending
                os.remove(video_filename)
            else:
                await update.message.reply_text("Couldn't download the video. Please try again.")
        except Exception as e:
            logger.error(f"Error: {e}")
            await update.message.reply_text("An error occurred. Please try again later.")
    else:
        await update.message.reply_text("Please send a valid TikTok video URL.")

# Error handling
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

async def main() -> None:
    # Create the Application and pass the bot's API token
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    application.add_error_handler(error)

    # Start the Bot
    await application.run_polling()

if __name__ == '__main__':
    # Running the bot asynchronously
    import nest_asyncio
    nest_asyncio.apply()

    # Running the main asynchronous function
    asyncio.run(main())
