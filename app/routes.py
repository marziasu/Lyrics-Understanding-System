from fastapi import APIRouter
from app.services.yt_audio_download import download_audio_from_youtube
from app.services.vocal_seperation import run_demucs_separation
import cloudinary.uploader

router = APIRouter()

@router.post("/extract-vocal-music")
def Extract(url: str):
    audio_url, audio_file = download_audio_from_youtube(url)
    print(audio_file)
    
    vocals, instrumental = run_demucs_separation(
        audio_file,
        model="htdemucs",
        two_stems=True,
        output_dir="demucs_output"
    )
    
    print(f"Separated vocals: {vocals}")
    print(f"Separated instrumental: {instrumental}")

    vocals_result = cloudinary.uploader.upload(vocals)
    vocal_url = vocals_result["secure_url"]
    print(vocal_url)

    instro_result = cloudinary.uploader.upload(instrumental)
    instro_url = instro_result["secure_url"]
    print(instro_url)

    return {
        "audio_url": audio_url,
        "vocal_url": vocals,
        "instromental_url": instro_url
    }


