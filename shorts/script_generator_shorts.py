from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_global_shorts_script():
    prompt = """
    지금 시점에서 글로벌 경제에서 가장 중요한 이슈 3~4가지를
    숏츠용으로 1분 이내 분량으로 요약해줘.

    조건:
    - 한국어
    - 말하듯 자연스럽게
    - ~합니다 체
    - 불필요한 서론 없이 바로 핵심
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return res.choices[0].message.content.strip()
