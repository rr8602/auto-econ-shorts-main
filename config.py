# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Shorts
OUTPUT_AUDIO = os.path.join(OUTPUT_DIR, "shorts_audio.mp3")
OUTPUT_BG_VIDEO = os.path.join(OUTPUT_DIR, "bg_video.mp4")
OUTPUT_FINAL = os.path.join(OUTPUT_DIR, "final_video.mp4")

# Longform
OUTPUT_LONG_AUDIO = os.path.join(OUTPUT_DIR, "long_audio.mp3")
OUTPUT_LONG_VIDEO = os.path.join(OUTPUT_DIR, "long_video.mp4")

# OAuth
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "token.json"
