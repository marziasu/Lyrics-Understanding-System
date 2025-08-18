import os
import subprocess
from app.config import AUDIO_DIR
import os
import cloudinary.uploader

def download_audio_from_youtube(url):
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    output_file = os.path.join(AUDIO_DIR, '%(title)s.%(ext)s')
    cmd = [
        "yt-dlp",
        "-x",  # extract audio only
        "--audio-format", "mp3",
        "-o", output_file,
        url
    ]
    subprocess.run(cmd, check=True)
    print(f"Downloaded audio saved as {output_file}")

    # Upload an image
    upload_result = cloudinary.uploader.upload(output_file)
    print(upload_result["secure_url"])

    return upload_result["secure_url"], output_file

if __name__ == "__main__":
    # youtube_url = "https://www.youtube.com/watch?v=L7b6vQQkIow&list=RD-lcd1ixHqjE&index=4"
    youtube_url = "https://youtu.be/dIQSBvoev0Y?si=2H_17j_Oogg0aBiN"
    download_audio_from_youtube(youtube_url)