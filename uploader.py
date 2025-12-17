from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from common.kakao_notifier import send_kakao_message
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "token.json"
IS_CI = os.environ.get("CI", "").lower() == "true"
print("DEBUG >>> CI =", os.environ.get("CI"))
print("DEBUG >>> IS_CI =", IS_CI)



def get_youtube_client():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def build_shorts_description(long_video_id: str | None):
    if not long_video_id:
        return "오늘 시황 핵심 요약입니다."

    return (
        "본편 전체 영상 바로보기\n"
        f"https://www.youtube.com/watch?v={long_video_id}\n\n"
        "자세한 분석은 본편에서 확인하세요."
    )


def upload_video(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    thumbnail_path: str | None = None,
    video_type: str = "short",
    long_video_id: str | None = None,
):
    if IS_CI:
        print("CI 환경에서는 업로드를 건너뜁니다.")
        return None


    youtube = get_youtube_client()

    if video_type == "short":
        description = build_shorts_description(long_video_id)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "25",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True,
        ),
    )

    response = request.execute()
    video_id = response["id"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    if video_type == "long" and thumbnail_path:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=thumbnail_path,
        ).execute()

    send_kakao_message(title=title, url=video_url)

    return video_id
