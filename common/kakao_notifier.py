import os
import json
import requests

KAKAO_API_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"


def send_kakao_message(title: str, url: str, status: str = "success"):
    """
    status: success | fail
    """

    token_json = os.environ.get("KAKAO_TOKEN_JSON")
    if not token_json:
        print("❌ KAKAO_TOKEN_JSON 환경변수 없음")
        return

    token = json.loads(token_json)
    access_token = token.get("access_token")

    if not access_token:
        print("❌ access_token 없음")
        return

    if status == "success":
        text = (
            f"✅ 업로드 완료\n\n"
            f"📌 {title}\n"
            f"🔗 {url}"
        )
    else:
        text = (
            f"❌ 업로드 실패\n\n"
            f"📌 {title}\n"
            f"로그 확인 필요"
        )

    payload = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": url,
            "mobile_web_url": url,
        },
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    res = requests.post(
        KAKAO_API_URL,
        headers=headers,
        data={"template_object": json.dumps(payload, ensure_ascii=False)},
    )

    if res.status_code != 200:
        print("❌ 카카오 메시지 실패:", res.text)
    else:
        print("🔔 카카오 메시지 전송 완료")
