import os
from pydub import AudioSegment
from app.config import TEMP_DIR
import os

def convert_mp3_to_wav(mp3_path):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        
    wav_path = os.path.join(TEMP_DIR, os.path.basename(mp3_path).replace(".mp3", ".wav"))
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    print(f"Converted {mp3_path} to {wav_path}")
    return wav_path