# video/merger_long.py
import subprocess

def merge_longform_video(
    bg_video: str,
    audio_path: str,
    subtitle_path: str,
    output_path: str = "output/long_final.mp4"
):
    print("롱폼 영상 + 오디오 + 자막 합성 중…")

    cmd = [
        "ffmpeg", "-y",
        "-i", bg_video,
        "-i", audio_path,
        "-vf",
        f"subtitles={subtitle_path}:"
        "force_style='Fontsize=28,Alignment=2,MarginV=80,Outline=2'",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print("롱폼 최종 영상 생성:", output_path)
    return output_path
