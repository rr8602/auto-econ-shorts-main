from openai import OpenAI
import os
import subprocess
from config import OUTPUT_LONG_AUDIO

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MAX_CHARS = 1500

def split_text(text):
    chunks, buf = [], ""
    for line in text.split("\n"):
        if len(buf) + len(line) < MAX_CHARS:
            buf += line + "\n"
        else:
            chunks.append(buf.strip())
            buf = line + "\n"
    if buf:
        chunks.append(buf.strip())
    return chunks

def generate_long_narration(script: str):
    os.makedirs("output", exist_ok=True)
    parts = []

    for i, chunk in enumerate(split_text(script)):
        res = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=chunk
        )
        path = f"output/part_{i}.mp3"
        with open(path, "wb") as f:
            f.write(res.read())
        parts.append(path)

    with open("output/concat.txt", "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "output/concat.txt",
        "-c", "copy",
        OUTPUT_LONG_AUDIO
    ], check=True)

    return OUTPUT_LONG_AUDIO
