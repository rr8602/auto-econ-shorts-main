import os
import subprocess

CI_VALUE = os.environ.get("CI", "").lower()
IS_CI = CI_VALUE in ("1", "true", "yes")


def merge_audio_video_with_subtitles(
    bg_video,
    audio_path,
    subtitle_path,
    output_path="output/final_video.mp4",
):
    if IS_CI:
        print("CI 환경: 숏폼 영상 합성 스킵")
        return output_path  # 더미 반환

    print("숏폼 영상 합성 시작")

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-stream_loop", "50", "-i", bg_video,
            "-i", audio_path,
            "-vf",
            f"subtitles={os.path.abspath(subtitle_path)}:"
            "force_style='Fontsize=18,Alignment=2,MarginV=120'",
            "-shortest",
            output_path,
        ],
        check=True,
    )

    print("숏폼 최종 영상 생성:", output_path)
    return output_path
