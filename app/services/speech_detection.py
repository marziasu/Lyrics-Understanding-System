from pydub import AudioSegment
import numpy as np
import torch
import os
import soundfile as sf
from silero_vad import get_speech_timestamps, collect_chunks, read_audio
from silero_vad.utils_vad import read_audio, collect_chunks, init_jit_model, get_speech_timestamps
from app.services.convert_mp3_to_wav import convert_mp3_to_wav

def stereo_to_mono(waveform: torch.Tensor) -> torch.Tensor:
    if waveform.shape[0] == 2:
        return torch.mean(waveform, dim=0, keepdim=True)
    return waveform


def load_audio_stereo(filepath: str) -> torch.Tensor:
    audio = AudioSegment.from_file(filepath)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    if audio.channels == 2:
        waveform = torch.tensor(samples).reshape(audio.channels, -1)
    else:
        waveform = torch.tensor(samples).unsqueeze(0)

    waveform = waveform / (2 ** 15)  # normalize to [-1, 1]
    return waveform, audio.frame_rate


def run_vad(audio_path, save_chunks=True, output_dir="chunks"):
    model_path = "silero-vad/src/silero_vad/data/silero_vad.jit"
    model = init_jit_model(model_path)

    wav = read_audio(audio_path, sampling_rate=16000)

    print(f"wav shape before fix: {wav.shape}")
    if wav.dim() == 1:
        wav = wav.unsqueeze(0)
        print(f"wav shape after fix: {wav.shape}")

    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000) # output like [{'start': 14368, 'end': 80864},{'start': 95264, 'end': 102368}]
    print(f"speech timestamps: {speech_timestamps}")

    if wav.dim() == 2:
        wav = wav.squeeze(0)  # [1, N] → [N]
        print(f"wav shape : {wav.shape}")
    speech_only = torch.cat([wav[i['start']: i['end']] for i in speech_timestamps])
    sf.write("speech_only.wav", speech_only.numpy(), samplerate=16000)

    # if save_chunks:
    #     os.makedirs(output_dir, exist_ok=True)
    #     print("wav shape before stereo to mono:", wav.shape)
    #     if wav.dim() == 2:
    #         wav = wav.squeeze(0)  # [1, N] → [N]
    #     print(f"wav shape : {wav.shape}")
    #     chunks = collect_chunks(speech_timestamps, wav) # collect chunks combined all speech segments (from timestamps to waveform) # outpu: tensor([ 0.0035,  0.0056,  0.0109,  ..., -0.0504])
    #     print(chunks)
    #     for i, chunk in enumerate(chunks):
    #         chunk_np = (chunk.squeeze().numpy() * 32767).astype("int16")
    #         audio_chunk = AudioSegment(
    #             chunk_np.tobytes(),
    #             frame_rate=16000,
    #             sample_width=2,
    #             channels=1,
    #         )
    #         out_path = os.path.join(output_dir, f"chunk_{i+1}.wav")
    #         audio_chunk.export(out_path, format="wav")
    #         print(f"Saved chunk: {out_path}")

    return speech_timestamps



if __name__ == "__main__":
    input_path = "app/data/audio/Abhi Na Jaao Chhod kar ｜｜ Ananya and Ankush.mp3"

    # MP3 থেকে WAV এ রূপান্তর
    wav_path = convert_mp3_to_wav(input_path)

    run_vad(wav_path)
