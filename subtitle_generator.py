import os
import subprocess
from datetime import timedelta
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import whisper

OUTPUT_SRT = "output.srt"
OUTPUT_VID = "output.mp4"
TEMP_FILE = "temp.mp3"

def generate_subtitles(video_path):
    def check_ffmpeg():
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            return result.returncode == 0 and 'ffmpeg' in result.stdout
        except FileNotFoundError:
            return False

    if not check_ffmpeg():
        print("ffmpeg must be installed to run this script.")
        return

    if not os.path.exists(video_path):
        print("Video file does not exist.")
        return

    video = VideoFileClip(video_path)
    if video.audio:
        video.audio.write_audiofile(TEMP_FILE, codec="mp3")
    else:
        print("Video has no audio.")
        return

    model = whisper.load_model("base")
    transcribe = model.transcribe(audio=TEMP_FILE, fp16=False)
    segments = transcribe["segments"]

    with open(OUTPUT_SRT, "w", encoding="utf-8") as f:
        for seg in segments:
            start = str(0) + str(timedelta(seconds=int(seg["start"]))) + ",000"
            end = str(0) + str(timedelta(seconds=int(seg["end"]))) + ",000"
            text = seg["text"]
            segment_id = seg["id"] + 1
            segment = f"{segment_id}\n{start} --> {end}\n{text[1:] if text[0] == ' ' else text}\n\n"
            f.write(segment)

    # Styling for subtitles
    def style_text(txt):
        return TextClip(
            txt, font="Verdana", fontsize=36, color="white", 
            stroke_color="black", stroke_width=1, align="center", 
            kerning=5, interline=-2
        )

    subtitles = SubtitlesClip(OUTPUT_SRT, style_text)
    video_with_subtitles = CompositeVideoClip(
        [video, subtitles.set_position(("center", "bottom"), relative=True)]
    )
    video_with_subtitles.write_videofile(OUTPUT_VID, codec="libx264")

    # Delete temporary files
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)
    if os.path.exists(OUTPUT_SRT):
        os.remove(OUTPUT_SRT)

    print(f"Subtitles generated and attached to {OUTPUT_VID}. Temporary files removed.")