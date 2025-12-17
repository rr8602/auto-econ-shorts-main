import subprocess

def merge_longform_video(
    bg_video: str,
    audio_path: str,
    subtitle_path: str,
    output_path: str = "output/long_final.mp4"
):
    subtitle_path = subtitle_path.replace("\\", "/")

    print("[MERGE] start", flush=True)

    vf = (
        f"subtitles='{subtitle_path}':"
        "force_style='Fontsize=28,Alignment=2,MarginV=80,Outline=2'"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", bg_video,
        "-i", audio_path,
        "-vf", vf,
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print("[MERGE] done:", output_path, flush=True)

    return output_path
