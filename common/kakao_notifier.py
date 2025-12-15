import requests
import os
import json

def send_kakao_message(title: str, url: str):
    token_json = os.environ.get("KAKAO_TOKEN_JSON")
    if not token_json:
        print("⚠️ 카카오 토큰 없음, 알림 스킵")
        return

    token = json.loads(token_json)
    headers = {"Authorization": f"Bearer {token['access_token']}"}

    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": f"📢 유튜브 업로드 완료\n\n{title}\n{url}",
            "link": {"web_url": url},
            "button_title": "영상 보기"
        })
    }

    requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers=headers,
        data=data
    )
