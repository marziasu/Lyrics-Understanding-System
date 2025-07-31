
from faster_whisper import WhisperModel
from pydub import AudioSegment
import os
import math
from app.config import BASE_DIR

# Load Faster-Whisper model (supports large-v3)
model_size = "large-v3"  # or "base", "small", etc.
model = WhisperModel(model_size, device="cuda" if os.environ.get("USE_CUDA") else "cpu", compute_type="int8")

# Path to your audio file
AUDIO_FILE = os.path.join("demucs_output/htdemucs/Niye Jabe Ki", "vocals.wav")

# Load audio with pydub
audio = AudioSegment.from_file(AUDIO_FILE)

# Split audio into 30-second chunks
chunk_length_ms = 30 * 1000
total_chunks = math.ceil(len(audio) / chunk_length_ms)

print(f"Total Chunks: {total_chunks}")


for i in range(total_chunks):
    start_ms = i * chunk_length_ms
    end_ms = min((i + 1) * chunk_length_ms, len(audio))

    chunk = audio[start_ms:end_ms]
    chunk_path = f"temp_chunk_{i}.wav"
    chunk.export(chunk_path, format="wav")

    # Transcribe with Faster-Whisper
    segments, info = model.transcribe(chunk_path, beam_size=5)
    print("Detected Language:", info.language)

    transcribed_text = "".join([segment.text for segment in segments])
    print(f"[{start_ms/1000:.1f}s - {end_ms/1000:.1f}s] ➤ {transcribed_text.strip()}")

    os.remove(chunk_path)
