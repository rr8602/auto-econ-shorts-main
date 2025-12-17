# shorts/shorts_pipeline.py
from datetime import datetime

from shorts.script_generator_shorts import generate_global_shorts_script

from audio.audio_generator import generate_narration
from shorts.subtitle_generator_shorts import generate_subtitles

from video.video_generator import generate_bg_video
from video.merger import merge_audio_video_with_subtitles

from uploader import upload_video


def run_shorts_pipeline():
    """
    01/09/17시: 롱폼과 무관한 '글로벌 경제 이슈' 숏츠 업로드
    """
    print("SHORTS PIPELINE (글로벌 이슈) 시작")

    # 글로벌 이슈 숏츠 스크립트 생성
    script = generate_global_shorts_script()

    # TTS
    audio_path = generate_narration(script)

    # 자막
    subtitle_path = generate_subtitles(audio_path)

    # 배경영상 (9:16, 60초 내)
    bg_video_path = generate_bg_video(
        script=script,
        aspect_ratio="9:16",
        seconds=60
    )

    # 합성 (날짜 오버레이 + 마지막 3초 고정멘트 포함하도록 merger가 구성돼 있어야 함)
    final_video = merge_audio_video_with_subtitles(
        subtitle_path=subtitle_path,
        market_type="GLOBAL"
    )

    # 업로드
    now_kst = datetime.now().strftime("%Y.%m.%d %H시")
    upload_video(
        video_path=final_video,
        title=f"{now_kst} 글로벌 경제 핵심 요약",
        description="지금 이 시간, 꼭 알아야 할 글로벌 경제 이슈 요약입니다.",
        tags=["shorts", "글로벌경제", "경제뉴스", "금리", "환율", "미국증시"],
        video_type="short"
    )

    print("SHORTS PIPELINE (글로벌 이슈) 완료")


def run_shorts_from_script(
    script: str,
    market_type: str,  # "US" | "KR"
    title: str,
    tags: list,
    long_video_id: str | None = None
):
    """
    08시/15시: 롱폼 대본을 요약한 숏츠를 생성/업로드
    - 숏폼 설명란에 롱폼 링크 삽입(long_video_id)
    """
    print(f"SHORTS FROM SCRIPT 시작 ({market_type})")

    # TTS
    audio_path = generate_narration(script)

    # 자막
    subtitle_path = generate_subtitles(audio_path)

    # 배경영상
    bg_video_path = generate_bg_video(
        script=script,
        aspect_ratio="9:16",
        seconds=60
    )

    # 합성
    final_video = merge_audio_video_with_subtitles(
        subtitle_path=subtitle_path,
        market_type=market_type
    )

    # 업로드
    upload_video(
        video_path=final_video,
        title=title,
        description="오늘 시황 핵심 요약입니다.",
        tags=tags,
        video_type="short",
        long_video_id=long_video_id
    )

    print(f"SHORTS FROM SCRIPT 완료 ({market_type})")
