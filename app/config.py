import os 
import cloudinary

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
AUDIO_DIR = os.path.join(DATA_DIR, 'audio')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')

cloudinary.config( 
    cloud_name = "dcs9fld5h", 
    api_key = "727872373946729", 
    api_secret = "<your_api_secret>", # Click 'View API Keys' above to copy your API secret
    secure=True
)