# subtitle/subtitle_generator.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_subtitles(audio_path: str, output_path: str = "output/subtitles.srt") -> str:
    """
    Whisper로 오디오 -> SRT 생성
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("Whisper로 숏폼 자막 생성 중…", audio_path)

    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="srt"
        )

    # result는 srt 문자열
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(result)

    print("숏폼 자막 생성 완료:", output_path)
    return output_path
