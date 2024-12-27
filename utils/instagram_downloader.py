import yt_dlp as ytdl
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download Instagram video
def download_instagram_video(url: str):
    try:
        # yt-dlp download options
        ydl_opts = {
            'format': 'best',  # Download the best quality available
            'outtmpl': './%(id)s.%(ext)s',  # Save the file with the video ID as the filename
            'quiet': True,  # Suppress unnecessary output
        }

        # Use yt-dlp to download the video
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  # This downloads the video
            video_filename = f"{info_dict['id']}.mp4"  # Save as video_id.mp4
            logger.info(f"Downloaded: {video_filename}")
            return video_filename
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None

