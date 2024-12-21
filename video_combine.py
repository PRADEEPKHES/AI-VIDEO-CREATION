import os
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import shutil

# Log setup using context manager to delete the existing log file at startup
log_file_path = "video_combine_log.txt"

if os.path.exists(log_file_path):
    os.remove(log_file_path)

def log_message(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}"
    print(log_entry)
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry + "\n")

try:
    log_message("Starting video creation process from clips.")

    # Define the path to the "video" folder and "music" folder
    clip_folder = os.path.join(os.getcwd(), "video_clip_tempfolder")
    music_folder = os.path.join(os.getcwd(), "music")
    
    # Create the temporary folder if it doesn't exist
    temp_folder = os.path.join(os.getcwd(), "video_combine_tempfolder")
    os.makedirs(temp_folder, exist_ok=True)

    # Get a list of all video files in the clip folder
    temp_video_files = [os.path.join(clip_folder, file) for file in os.listdir(clip_folder) if file.endswith(('.mp4', '.avi', '.mov'))]

    if not temp_video_files:
        raise ValueError("No video files found in the 'video' folder.")

    log_message(f"Found {len(temp_video_files)} video file(s) to process.")

    # Load all video clips
    final_clips = [VideoFileClip(temp_video) for temp_video in temp_video_files]
    
    # Concatenate all video clips into a single video
    final_video = concatenate_videoclips(final_clips, method="compose")
    log_message("Video clips successfully concatenated.")

    # Add background music from the "music" folder
    audio_background_path = None
    
    # Search for any MP3 file in the music folder
    for file in os.listdir(music_folder):
        if file.endswith('.mp3'):
            audio_background_path = os.path.join(music_folder, file)
            break  # Use the first MP3 file found

    if audio_background_path and os.path.exists(audio_background_path):
        audio_background = AudioFileClip(audio_background_path).set_duration(final_video.duration)
        final_video = final_video.set_audio(audio_background)
        log_message(f"Background music added from: {audio_background_path}")
    else:
        log_message("No background music file found. Proceeding without music.")

    # Define output video path
    output_video_path = "final_output_video.mp4"
    
    # Write the final video file with appropriate settings
    final_video.write_videofile(output_video_path, fps=10)
    
    log_message(f"Final video created: {output_video_path}, Total Duration: {final_video.duration:.2f} seconds")

except Exception as e:
    log_message(f"Error creating video: {e}")

finally:
    log_message("Script finished.")

# Delete the folders and log files
folders_to_delete = ['resized_image', 'video_clip_tempfolder', 'video_combine_tempfolder', 'web_image']
files_to_delete = ['image_download_log.txt', 'image_resize_log.txt', 'video_clip_log.txt', 'video_combine_log.txt']

# Delete files
for file in files_to_delete:
    try:
        if os.path.exists(file):
            os.remove(file)
            log_message(f"File deleted: {file}")
    except Exception as e:
        log_message(f"Error deleting file {file}: {e}")

# Delete folders
for folder in folders_to_delete:
    try:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            log_message(f"Folder deleted: {folder}")
    except Exception as e:
        log_message(f"Error deleting folder {folder}: {e}")
    
# Prompt user to press Enter before exiting
input("Press Enter to exit...")
