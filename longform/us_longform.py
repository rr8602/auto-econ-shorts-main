from audio.tts_long import generate_long_narration
from uploader import upload_video
from shorts.shorts_pipeline import run_shorts_pipeline
from datetime import datetime, timedelta

def run_us_longform():
    date = (datetime.now() - timedelta(days=1)).strftime("%Y.%m.%d")
    script = f"{date} 미국 증시 시황 전체 분석..."
    audio = generate_long_narration(script)

    video_path = "output/long_video.mp4"
    video_id = upload_video(
        video_path=video_path,
        title=f"{date} 미장 시황 - 핵심 이슈 총정리",
        description=script[:4000],
        tags=["미국증시", "시황"],
        video_type="long"
    )

    run_shorts_pipeline("US", script, f"{date} 미장 시황")
