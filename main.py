import os
from video_processor import process_video
from subtitle_generator import generate_subtitles
from tiktok_uploader import upload_to_tiktok


def main():
    video_path = r"C:\Projects\TikTok Bot\videos\video1.mp4"
    
    #Clip The Video
    #process_video(r"C:\Projects\TikTok Bot\videos\video1.mp4")
    
    # Add Subtitles
    generate_subtitles(video_path)
    pass

if __name__ == "__main__":
    main()
