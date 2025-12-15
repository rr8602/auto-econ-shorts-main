from audio.audio_generator import generate_narration
from shorts.shorts_summary_generator import generate_shorts_summary
from video.video_generator import generate_bg_video
from video.merger import merge_audio_video_with_subtitles
from uploader import upload_video
from config import OUTPUT_AUDIO

def run_shorts_pipeline(market_type="US", long_script=None, title="시황 요약"):
    script = generate_shorts_summary(market_type, long_script)
    generate_narration(script)
    subtitle_path = "output/subtitles.srt"
    generate_bg_video(script)
    final_video = merge_audio_video_with_subtitles(subtitle_path, market_type)

    upload_video(
        video_path=final_video,
        title=title,
        description="시황 핵심 요약 #shorts",
        tags=["shorts", "경제", "시황"],
        video_type="short"
    )
