from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_shorts_summary(market_type: str, long_script: str) -> str:
    prompt = f"""
아래 {market_type} 시황 롱폼을 1분 숏폼용으로 핵심만 요약해줘.
문장은 짧고 빠르게.

{long_script[:3000]}
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
