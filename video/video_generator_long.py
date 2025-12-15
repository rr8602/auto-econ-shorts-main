from openai import OpenAI
import os
from config import OUTPUT_BG_VIDEO

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_bg_video(prompt: str):
    job = client.videos.create(
        model="sora-2",
        prompt=prompt,
        size="720x1280",
        seconds="12"
    )

    while job.status not in ("succeeded", "failed"):
        job = client.videos.retrieve(job.id)

    if job.status == "failed":
        raise RuntimeError("Sora 생성 실패")

    content = client.videos.download_content(job.id, variant="video")
    content.write_to_file(OUTPUT_BG_VIDEO)
    return OUTPUT_BG_VIDEO
