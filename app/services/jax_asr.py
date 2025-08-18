# from whisper_jax import FlaxWhisperForConditionalGeneration, FlaxWhisperPipline
# import jax.numpy as jnp
# from app.config import AUDIO_DIR
# import os

# audio_path= os.path.join(AUDIO_DIR, "Niye Jabe Ki.mp3")

# pipeline = FlaxWhisperPipline('parthiv11/indic_whisper_nodcil', dtype=jnp.bfloat16)
# result = pipeline(audio_path)
# print(result["text"])

from pydub import AudioSegment
import math
from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp
import os
from app.config import AUDIO_DIR

audio_path = os.path.join(AUDIO_DIR, "Niye Jabe Ki.mp3")
segment_length_ms = 30 * 1000  # 30 seconds

# Load audio
audio = AudioSegment.from_file(audio_path)
duration_ms = len(audio)
num_segments = math.ceil(duration_ms / segment_length_ms)

# Whisper pipeline
pipeline = FlaxWhisperPipline('indonesian-nlp/whisper-small-ml', dtype=jnp.float32) # ai4bharat/indic-whisper-small

full_transcript = ""

for i in range(num_segments):
    start = i * segment_length_ms
    end = min((i + 1) * segment_length_ms, duration_ms)
    segment = audio[start:end]
    segment_path = f"temp_segment_{i}.wav"
    segment.export(segment_path, format="wav")
    
    # Transcribe segment
    result = pipeline(segment_path, language="bn")
    print(result)
    full_transcript += result["text"].strip() + " "
    
    # Optional: Delete temp file
    os.remove(segment_path)

print(full_transcript.strip())