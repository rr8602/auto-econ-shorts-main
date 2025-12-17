import os
import subprocess
from datetime import datetime, timedelta
from config import OUTPUT_BG_VIDEO, OUTPUT_AUDIO, OUTPUT_FINAL

CI_VALUE = os.environ.get("CI", "").lower()
IS_CI = CI_VALUE in ("1", "true", "yes")


def merge_audio_video_with_subtitles(subtitle_path: str, market_type: str) -> str | None:
    """
    숏폼(9:16) 최종 영상 합성
    - 배경영상(OUTPUT_BG_VIDEO) + 나레이션(OUTPUT_AUDIO) + 자막(subtitle_path)
    - 길이는 TTS 오디오 길이를 기준으로, 최대 60초 내로 강제
    - 오디오 트랙이 빠지지 않도록 명시적으로 map
    """
    if IS_CI:
        print("⚠️ CI 환경: 숏폼 영상 합성 스킵")
        return None

    if market_type == "US":
        date_text = (datetime.now() - timedelta(days=1)).strftime("%Y.%m.%d") + " 미국장"
    else:
        date_text = datetime.now().strftime("%Y.%m.%d") + " 국장"

    # 1) 오디오 길이 측정
    duration = float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                OUTPUT_AUDIO,
            ]
        )
        .decode()
        .strip()
    )

    # Shorts 규격을 위해 최대 60초(여유를 두고 58초)로 클램프
    max_duration = min(duration, 58.0)
    outro_start = max(max_duration - 3.0, 0.0)

    # 2) 필터 체인 구성 (한 번의 -vf 인자로 전달)
    vf_filter = (
        f"drawtext=text='{date_text}':x=(w-text_w)/2:y=40:"
        f"fontsize=26:box=1:boxcolor=black@0.4,"
        f"subtitles={subtitle_path}:force_style='Fontsize=18,Alignment=2,MarginV=120',"
        f"drawtext=text='본편에서 자세히':x=(w-text_w)/2:y=h-200:fontsize=32:"
        f"enable='gte(t,{outro_start})'"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-stream_loop",
        "-1",  # 배경 영상 무한 반복
        "-i",
        OUTPUT_BG_VIDEO,
        "-i",
        OUTPUT_AUDIO,
        "-t",
        f"{max_duration:.2f}",  # 출력 길이 제한 (<= 60초)
        "-vf",
        vf_filter,
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-shortest",
        OUTPUT_FINAL,
    ]

    print("FFmpeg (shorts) merge command:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    return OUTPUT_FINAL
