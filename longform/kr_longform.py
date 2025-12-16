# longform/kr_longform.py
from datetime import datetime

from longform.tts_long import generate_long_narration
from longform.script_generator_long import generate_us_long_script
from longform.subtitle_generator_long import generate_long_subtitles
from video.video_generator_long import generate_bg_video
from video.merger_long import merge_longform_video
from uploader import upload_video
from shorts.shorts_pipeline import run_shorts_from_script


def run_kr_longform():
    print("🔵 국장 롱폼 파이프라인 시작")

    # -----------------------------
    # 1️⃣ 날짜 (국장은 당일)
    # -----------------------------
    target_date = datetime.now().strftime("%Y.%m.%d")

    # -----------------------------
    # 2️⃣ 롱폼 스크립트 (직접 포함)
    # -----------------------------
    script = generate_us_long_script(target_date)

    # -----------------------------
    # 3️⃣ TTS → 롱폼 오디오
    # -----------------------------
    audio_path, _ = generate_long_narration(script)

    # -----------------------------
    # 4️⃣ Whisper 자막 생성
    # -----------------------------
    subtitle_path = generate_long_subtitles(audio_path)

    # -----------------------------
    # 5️⃣ 16:9 배경 영상 생성
    # -----------------------------
    bg_video_path = generate_bg_video(audio_path)

    # -----------------------------
    # 6️⃣ 영상 + 오디오 + 자막 합성
    # -----------------------------
    final_video_path = merge_longform_video(
        bg_video=bg_video_path,
        audio_path=audio_path,
        subtitle_path=subtitle_path
    )

    # -----------------------------
    # 7️⃣ 유튜브 롱폼 업로드
    # -----------------------------
    video_id = upload_video(
        video_path=final_video_path,
        title=f"{target_date} 국장 시황 - 오늘 국내 증시 정리",
        description=script[:4000],
        tags=[
            "국장시황", "코스피", "코스닥",
            "국내증시", "경제시황", "주식시장"
        ],
        video_type="long"
    )

    print("✅ 국장 롱폼 업로드 완료")

    # -----------------------------
    # 8️⃣ 롱폼 요약 숏폼 생성 + 업로드
    # -----------------------------
    run_shorts_from_script(
        script=script,
        market_type="KR",
        title=f"{target_date} 국장 시황",
        tags=["shorts", "국장", "코스피", "경제"],
        long_video_id=video_id
    )

    print("🎉 국장 롱폼 + 요약 숏폼 완료")
