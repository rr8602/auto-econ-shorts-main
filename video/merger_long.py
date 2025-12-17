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
        "-stream_loop", "-1",          # 배경 영상 무한 루프
        "-i", bg_video,
        "-i", audio_path,
        "-vf",
        f"subtitles={subtitle_path}:"
        "force_style='Fontsize=28,Alignment=2,MarginV=80,Outline=2'",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",                   # 이제 기준은 오디오
        output_path
    ]

    subprocess.run(cmd, check=True)
    print("롱폼 최종 영상 생성:", output_path)
    return output_path

