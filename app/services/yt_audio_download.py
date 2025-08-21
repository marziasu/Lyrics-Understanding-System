import os
from yt_dlp import YoutubeDL
import cloudinary.uploader
from app.config import AUDIO_DIR

def download_audio_from_youtube(url):
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(AUDIO_DIR, '%(title)s.%(ext)s'),
        'restrictfilenames': True,  # makes filename safe for filesystem
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info)
        # Replace extension to mp3 after audio extraction
        downloaded_file = os.path.splitext(downloaded_file)[0] + ".mp3"

    print(f"Downloaded file path: {downloaded_file}")

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(downloaded_file, resource_type="video")
    print(f"Cloudinary URL: {upload_result['secure_url']}")

    return upload_result["secure_url"], downloaded_file




if __name__ == "__main__":
    youtube_url = "https://youtu.be/dIQSBvoev0Y?si=2H_17j_Oogg0aBiN"
    cloud_url, local_path = download_audio_from_youtube(youtube_url)
    print("Cloud URL:", cloud_url)
    print("Local Path:", local_path)
