import subprocess
from datetime import datetime, timedelta
from config import OUTPUT_BG_VIDEO, OUTPUT_AUDIO, OUTPUT_FINAL

def merge_audio_video_with_subtitles(subtitle_path, market_type):
    if market_type == "US":
        date_text = (datetime.now() - timedelta(days=1)).strftime("%Y.%m.%d") + " 미국장"
    else:
        date_text = datetime.now().strftime("%Y.%m.%d") + " 국장"

    duration = float(subprocess.check_output(
        f'ffprobe -v error -show_entries format=duration '
        f'-of default=noprint_wrappers=1:nokey=1 "{OUTPUT_AUDIO}"',
        shell=True
    ).decode().strip())

    subprocess.run([
        "ffmpeg", "-y",
        "-stream_loop", "50",
        "-i", OUTPUT_BG_VIDEO,
        "-t", str(duration),
        "-i", OUTPUT_AUDIO,
        "-vf",
        f"drawtext=text='{date_text}':x=(w-text_w)/2:y=40:fontsize=26:box=1:boxcolor=black@0.4,"
        f"subtitles={subtitle_path}:force_style='Fontsize=18,Alignment=2,MarginV=120',"
        f"drawtext=text='본편에서 자세히':x=(w-text_w)/2:y=h-200:fontsize=32:"
        f"enable='gte(t,{duration-3})'",
        "-shortest",
        OUTPUT_FINAL
    ], check=True)

    return OUTPUT_FINAL
