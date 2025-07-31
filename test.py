import torchaudio
torchaudio.set_audio_backend("sox_io") 
print(torchaudio.list_audio_backends()) 