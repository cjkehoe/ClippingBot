import os
from video_processor import process_video
from subtitle_generator import generate_subtitles
from tiktok_uploader import upload_to_tiktok


def main():
    video_path = r"/Users/chriskehoe/Projects/ClippingBot/videos/video1_clips/clip_2.mp4"
    
    #Clip The Video
    #process_video(video_path)
    
    # Add Subtitles
    generate_subtitles(video_path)
    pass

if __name__ == "__main__":
    main()
