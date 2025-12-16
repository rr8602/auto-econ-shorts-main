# longform/thumbnail_text_generator.py
import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY 환경변수가 없습니다.")

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL_NAME = os.environ.get("OPENAI_TEXT_MODEL", "gpt-4o-mini")


def generate_thumbnail_text(market_type: str, issue_summary: str) -> str:
    """
    market_type: "US" | "KR"
    issue_summary: 대본 일부(앞부분 500~1000자 정도) 넣으면 됨
    return: 썸네일용 클릭 유도 문구 (짧고 강하게)
    """
    market_name = "미국장" if market_type == "US" else "국장"

    prompt = f"""
너는 유튜브 썸네일 카피라이터다.
아래는 오늘 {market_name} 시황 대본 일부 요약이다.

[요약]
{issue_summary}

[요구사항]
- 한국어
- 12자~22자 내외 (너무 길면 안 됨)
- 클릭 유도형(호기심 유발)
- 과장/낚시/허위는 금지
- 숫자/회사명은 확신할 때만
- 출력은 문구 1개만

문구:
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "너는 썸네일 카피라이터다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )
    text = res.choices[0].message.content.strip()
    # 따옴표/불필요 줄 제거
    return text.replace('"', "").replace("'", "").splitlines()[0].strip()
