from openai import OpenAI
import os
import time

OUTPUT_BG_VIDEO = "output/long_video.mp4"

CI_VALUE = os.environ.get("CI", "").lower()
IS_CI = CI_VALUE in ("1", "true", "yes")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_bg_video(prompt: str):
    if IS_CI:
        print("CI 환경: Sora 비디오 생성 스킵 (더미 영상 사용)", flush=True)

        # 더미 16:9 영상 생성
        os.system(
            "ffmpeg -y -f lavfi -i color=c=black:s=1280x720:r=30 -t 5 output/long_video.mp4"
        )
        return OUTPUT_BG_VIDEO

    print("Sora 배경 영상 생성 시작", flush=True)

    job = client.videos.create(
        model="sora-2",
        prompt=prompt,
        size="720x1280",
        seconds=str(12)
    )

    # 안전한 폴링 (타임아웃 포함)
    for _ in range(60):  # 최대 60초
        job = client.videos.retrieve(job.id)
        print(f"Sora status: {job.status}", flush=True)

        if job.status == "succeeded":
            break
        if job.status == "failed":
            raise RuntimeError("Sora 비디오 생성 실패")

        time.sleep(2)

    if job.status != "succeeded":
        raise TimeoutError("Sora 비디오 생성 타임아웃")

    content = client.videos.download_content(job.id, variant="video")
    content.write_to_file(OUTPUT_BG_VIDEO)

    print("Sora 배경 영상 생성 완료", flush=True)
    return OUTPUT_BG_VIDEO
