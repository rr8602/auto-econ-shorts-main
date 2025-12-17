# video/video_generator_long.py
import os
import time
import subprocess
from openai import OpenAI

OUTPUT_BG_VIDEO = "output/long_video.mp4"

CI_VALUE = os.environ.get("CI", "").lower()
IS_CI = CI_VALUE in ("1", "true", "yes")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY 환경변수가 없습니다.")

client = OpenAI(api_key=OPENAI_API_KEY)


def _make_dummy_169_video(out_path: str = OUTPUT_BG_VIDEO, seconds: int = 10) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=black:s=1280x720:r=30",
        "-t", str(seconds),
        out_path
    ]
    subprocess.run(cmd, check=True)
    return out_path


def generate_bg_video(prompt: str, sora_seconds: str = "12") -> str:
    """
    롱폼(16:9) 배경 영상 생성.
    - CI면 더미 영상 생성
    - 로컬에서는 Sora 시도
      - 오래 걸리면 fallback(더미 영상)로 넘어가서 파이프라인이 죽지 않게 함
    """

    # 0) CI에서는 Sora 금지 → 더미
    if IS_CI:
        print("CI 환경: Sora 비디오 생성 스킵 (더미 16:9)", flush=True)
        return _make_dummy_169_video(seconds=10)

    # 1) Sora seconds는 문자열이며 '4','8','12'만 허용되는 경우가 있음
    if sora_seconds not in ("4", "8", "12"):
        sora_seconds = "12"

    print("Sora 배경 영상 생성 시작 (LONG, 16:9)", flush=True)

    job = client.videos.create(
        model="sora-2",
        prompt=prompt,
        size="1280x720",     # 롱폼은 16:9
        seconds=sora_seconds # 문자열
    )

    print(f"Sora job id: {job.id}", flush=True)

    # 2) 폴링 (현실적으로 2분은 짧음 → 넉넉하게)
    MAX_WAIT_SEC = 12 * 60   # 최대 12분
    INTERVAL_SEC = 5
    waited = 0

    # 상태값 호환: SDK/버전에 따라 succeeded/completed 등 다양
    SUCCESS_STATES = {"succeeded", "completed", "success"}
    FAIL_STATES = {"failed", "error", "cancelled", "canceled"}

    while True:
        job = client.videos.retrieve(job.id)
        status = str(job.status).lower()

        print(f"Sora status: {status} ({waited}s)", flush=True)

        if status in SUCCESS_STATES:
            break
        if status in FAIL_STATES:
            print("Sora 실패 상태 → 더미 영상으로 대체", flush=True)
            return _make_dummy_169_video(seconds=10)

        time.sleep(INTERVAL_SEC)
        waited += INTERVAL_SEC

        if waited >= MAX_WAIT_SEC:
            print("Sora 생성 지연(타임아웃) → 더미 영상으로 대체", flush=True)
            return _make_dummy_169_video(seconds=10)

    # 3) 성공 시 다운로드
    try:
        content = client.videos.download_content(job.id, variant="video")
        os.makedirs(os.path.dirname(OUTPUT_BG_VIDEO), exist_ok=True)
        content.write_to_file(OUTPUT_BG_VIDEO)
        print("Sora 배경 영상 생성 완료:", OUTPUT_BG_VIDEO, flush=True)
        return OUTPUT_BG_VIDEO
    except Exception as e:
        print(f"다운로드 실패({e}) → 더미 영상으로 대체", flush=True)
        return _make_dummy_169_video(seconds=10)
