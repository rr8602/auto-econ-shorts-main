import os
import time
from openai import OpenAI
from config import OPENAI_API_KEY, OUTPUT_BG_VIDEO

# -----------------------------
# OpenAI Client
# -----------------------------
client = OpenAI(api_key=OPENAI_API_KEY)

os.makedirs("output", exist_ok=True)


# -----------------------------
# 프롬프트 생성
# -----------------------------
def build_prompt(script: str) -> str:
    """
    숏폼용 배경 영상 프롬프트
    (사람/텍스트 절대 없음)
    """
    return f"""
Cinematic background video for an economic market update short-form video.

Requirements:
- No humans
- No text, no subtitles
- Animated financial charts, candlestick graphs
- Global stock market visuals
- Dark theme, modern UI, neon accents
- Smooth camera movement
- Professional finance YouTube Shorts style
- Vertical 9:16 format
- Calm but dynamic motion

Context (do NOT display text from this):
\"\"\"{script}\"\"\"
"""


# -----------------------------
# 배경 영상 생성
# -----------------------------
def generate_bg_video(script: str) -> str:
    """
    OpenAI Sora API로 숏폼 배경 영상 생성
    """
    print("🎬 숏폼 배경 영상 생성 시작")

    prompt = build_prompt(script)

    job = client.videos.create(
        model="sora-2",
        prompt=prompt,
        size="720x1280",     # ✅ Shorts 9:16
        seconds=12           # ✅ 숏폼 반복용 기본 단위
    )

    print("⌛ 영상 생성 요청 ID:", job.id)

    # 생성 완료 대기
    while job.status in ("queued", "in_progress"):
        print(f"  - 상태: {job.status}")
        time.sleep(5)
        job = client.videos.retrieve(job.id)

    if job.status != "completed":
        raise RuntimeError("❌ 배경 영상 생성 실패")

    print("📥 영상 다운로드 중…")

    video_content = client.videos.download_content(
        job.id,
        variant="video"
    )
    video_content.write_to_file(OUTPUT_BG_VIDEO)

    print("✅ 배경 영상 저장 완료:", OUTPUT_BG_VIDEO)
    return OUTPUT_BG_VIDEO
