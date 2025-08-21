import os 
import cloudinary
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
AUDIO_DIR = os.path.join(DATA_DIR, 'audio')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')


cloudinary.config( 
    cloud_name = os.getenv("CLOUD_NAME"), 
    api_key = os.getenv("API_KEY"), 
    api_secret = os.getenv("API_SECRET")
)