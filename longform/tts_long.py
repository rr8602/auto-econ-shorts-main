# longform/tts_long.py
import os
import subprocess
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY 환경변수가 없습니다.")

client = OpenAI(api_key=OPENAI_API_KEY)

MAX_TTS_CHARS = 1500


def split_script(script: str, max_chars: int = MAX_TTS_CHARS):
    chunks = []
    cur = ""
    for para in script.split("\n"):
        if len(cur) + len(para) + 1 <= max_chars:
            cur += para + "\n"
        else:
            if cur.strip():
                chunks.append(cur.strip())
            cur = para + "\n"
    if cur.strip():
        chunks.append(cur.strip())
    return chunks


def generate_long_narration(script: str):
    """
    return: (audio_path, video_path)
    여기서는 audio만 만들고, video는 '기본 16:9 검정 화면'을 만들어 리턴(업로드용).
    """
    os.makedirs("output", exist_ok=True)

    chunks = split_script(script)
    part_paths = []

    print("롱폼 TTS 생성(분할)...")
    for i, chunk in enumerate(chunks, start=1):
        print(f"  - 파트 {i}/{len(chunks)}")
        resp = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=chunk
        )
        p = f"output/tts_part_{i:03d}.mp3"
        with open(p, "wb") as f:
            f.write(resp.read())
        part_paths.append(p)

    # concat list
    concat_txt = "output/concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in part_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")

    audio_out = "output/long_narration.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", audio_out],
        check=True
    )
    print("롱폼 오디오 생성 완료:", audio_out)

    # 임시 16:9 더미 영상 (검정 화면) - 최소한 업로드 가능한 형태
    video_out = "output/long_video.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1280x720:r=30", "-t", "5", video_out],
        check=True
    )

    return audio_out, video_out
