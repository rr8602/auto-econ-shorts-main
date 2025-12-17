# longform/script_generator_long.py
import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY 환경변수가 없습니다.")

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = os.environ.get("OPENAI_TEXT_MODEL", "gpt-4o-mini")


def generate_us_long_script(target_date: str) -> str:
    """
    target_date: "YYYY.MM.DD" (미국장은 전일 기준을 외부에서 넘겨줌)
    """
    prompt = f"""
너는 유튜브 경제 시황 채널의 메인 작가다.
아래 조건을 만족하는 '미국장 시황' 유튜브 롱폼 통대본을 한국어로 작성하라.

[조건]
- 대상 날짜: {target_date} (전일 미국장)
- 최소 6000자 이상 (10분+ 분량)
- 말투: ~합니다 체
- 구성: 오프닝(훅) -> 핵심 요약 -> 지표/이슈 3~6개 -> 섹터/종목 흐름 -> 앞으로 체크포인트 -> 마무리
- 지나친 단정 금지(투자권유 아님 고지 포함)
- 이슈는 '가장 핵심적인 것' 위주로, 이해하기 쉽게 설명
- 숫자/지표는 "정확히 모르면" 추정하지 말고 "대략" 수준으로 표현

[출력 형식]
- 제목/자막용 문구 제외, 통대본만 출력
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "너는 경제 시황 유튜브 대본 전문가다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
    )

    return res.choices[0].message.content.strip()


def generate_kr_long_script(target_date: str) -> str:
    prompt = f"""
너는 유튜브 경제 시황 채널의 메인 작가다.
아래 조건을 만족하는 '국장 시황' 유튜브 롱폼 통대본을 한국어로 작성하라.

[조건]
- 대상 날짜: {target_date} (당일 국장)
- 최소 6000자 이상 (10분+ 분량)
- 말투: ~합니다 체
- 구성: 오프닝(훅) -> 핵심 요약 -> 이슈 3~6개 -> 코스피/코스닥 흐름 -> 수급/환율/금리 -> 업종/테마 -> 내일 체크포인트 -> 마무리
- 지나친 단정 금지(투자권유 아님 고지 포함)
- 숫자/지표는 정확히 모르면 추정하지 말고 “대략” 수준으로

[출력 형식]
- 제목/자막용 문구 제외, 통대본만 출력
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "너는 한국 주식시장(국장) 시황 유튜브 대본 전문가다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
    )

    return res.choices[0].message.content.strip()
