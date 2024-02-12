from moviepy.editor import VideoFileClip
import os

def process_video(video_path):
    clip_length = 61  # Clip length in seconds
    clips = []

    # Load the video
    video = VideoFileClip(video_path)
    total_duration = int(video.duration)

    # Calculate the number of clips
    num_clips = total_duration // clip_length
    last_clip_length = total_duration % clip_length

    # Handle the special case for the last clip
    if last_clip_length > 0:
        if last_clip_length + clip_length <= total_duration:
            num_clips -= 1
        else:
            clip_length = total_duration - (num_clips * clip_length)

    # Create a directory named after the video file
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    clips_directory = os.path.join(os.path.dirname(video_path), f"{video_name}_clips")
    if not os.path.exists(clips_directory):
        os.makedirs(clips_directory)

    # Generate clips
    for i in range(num_clips):
        start_time = i * clip_length
        end_time = start_time + clip_length
        clip = video.subclip(start_time, min(end_time, total_duration))
        clips.append(clip)

        # Save the clip in the newly created folder
        output_filename = os.path.join(clips_directory, f"clip_{i+1}.mp4")
        clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")

    # Close the video file
    video.close()
    return clips

# Example usage
# process_video("path_to_your_video.mp4")
