from openai import OpenAI
from config import OUTPUT_AUDIO
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_narration(script: str):
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=script
    )

    with open(OUTPUT_AUDIO, "wb") as f:
        f.write(response.read())

    return OUTPUT_AUDIO
