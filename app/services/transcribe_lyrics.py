import whisper
from pydub import AudioSegment
import os
import math
from app.config import AUDIO_DIR

# Load Whisper model
model = whisper.load_model("base")  # base / small / medium / large
speech_file = "speech_only.wav"
# Path to your audio file (mp3, wav, etc.)
AUDIO_FILE = os.path.join(AUDIO_DIR, "Niye Jabe Ki (নিয়ে যাবে কি)｜ Daagi ｜ Afran Nisho,Xefer,Tama,Sunerah ｜ Shihab S ｜SVF Alpha-i｜ Chorki.mp3")

# Load audio with pydub
audio = AudioSegment.from_file(AUDIO_FILE)

# Split audio into 10-second chunks (simulate real-time)
chunk_length_ms = 10 * 1000  # 10 seconds
total_chunks = math.ceil(len(audio) / chunk_length_ms)

print(f"Total Chunks: {total_chunks}")

for i in range(total_chunks):
    start_ms = i * chunk_length_ms
    end_ms = min((i + 1) * chunk_length_ms, len(audio))

    chunk = audio[start_ms:end_ms]
    chunk_path = f"temp_chunk_{i}.wav"
    chunk.export(chunk_path, format="wav")

    result = model.transcribe(chunk_path)
    print(f"[{start_ms/1000:.1f}s - {end_ms/1000:.1f}s] ➤ {result['text'].strip()}")

    os.remove(chunk_path)
