import os
import subprocess
from datetime import timedelta  # Import timedelta
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import whisper

OUTPUT_SRT = "output.srt"
OUTPUT_VID = "output.mp4"
TEMP_FILE = "temp.mp3"

def generate_subtitles(video_path):
    # Check if ffmpeg is installed
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

    # Extract audio from video
    video = VideoFileClip(video_path)
    if video.audio:
        video.audio.write_audiofile(TEMP_FILE, codec="mp3")
    else:
        print("Video has no audio.")
        return

    # Generate subtitles using Whisper
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

    # Attach subtitles to video
    subtitles = SubtitlesClip(OUTPUT_SRT, lambda txt: TextClip(txt, font="Arial", fontsize=24, color="white", bg_color="black"))
    video_with_subtitles = CompositeVideoClip([video, subtitles.set_position(("center", 0.95), relative=True)])
    video_with_subtitles.write_videofile(OUTPUT_VID, codec="libx264")

    print(f"Subtitles generated and attached to {OUTPUT_VID}")

# Optional: You can also provide a function to install required libraries if they are not installed.
