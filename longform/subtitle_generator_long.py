# longform/subtitle_generator_long.py
import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_long_subtitles(
    audio_path: str,
    output_path: str = "output/long_subtitles.srt"
) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("📝 롱폼 Whisper 자막 생성 중…")

    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="srt"
        )

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(result)

    print("✅ 롱폼 자막 생성 완료:", output_path)
    return output_path
