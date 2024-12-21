import os
import time
from moviepy.editor import ImageClip, concatenate_videoclips

# Initialize logging by deleting the log file if it exists
log_file_path = "video_clip_log.txt"
if os.path.exists(log_file_path):
    os.remove(log_file_path)

def log_message(message):
    """
    Logs a message with a timestamp to the console and a log file.
    """
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}"
    print(log_entry)
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry + "\n")

try:
    log_message("Starting video clip creation process from images.")

    # Define the path to the "resized_image" folder and temporary folder
    image_folder = os.path.join(os.getcwd(), "resized_image")
    temp_folder = os.path.join(os.getcwd(), "video_clip_tempfolder")

    # Remove existing temporary folder if it exists, and create a new one
    if os.path.exists(temp_folder):
        for file in os.listdir(temp_folder):
            os.remove(os.path.join(temp_folder, file))
        os.rmdir(temp_folder)
    os.makedirs(temp_folder, exist_ok=True)

    # Load all JPEG image paths from the "resized_image" folder
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if img.lower().endswith((".jpeg", ".jpg"))]

    # Log the number of images found
    num_images = len(images)
    log_message(f"Found {num_images} images.")

    if num_images == 0:
        raise Exception("No images found. Cannot create video clips.")

    # Set duration per image (5 seconds)
    duration_per_image = 6  # seconds

    # Create temporary video clips for each image
    temp_resized_image_files = []
    for idx, img in enumerate(images):
        temp_video_clip_path = os.path.join(temp_folder, f"video_clip_{idx}.mp4")  # Change to .mp4
        img_clip = ImageClip(img).set_duration(duration_per_image).resize(height=720, width=1280).set_fps(10)  
        img_clip.write_videofile(temp_video_clip_path, codec="libx264", fps=10, audio=False)  # MP4 format
        temp_resized_image_files.append(temp_video_clip_path)
        log_message(f"Created temporary video clip: {temp_video_clip_path}")

except Exception as e:
    log_message(f"Error creating video clip: {e}")

finally:
    # Log completion and open another script
    log_message("Script finished.")
    # Open 'video_combine.py' if it exists in the same directory
    combine_script_path = os.path.join(os.getcwd(), "video_combine.py")
    if os.path.isfile(combine_script_path):
        os.system(f"python {combine_script_path}")
    else:
        log_message("No 'video_combine.py' script found.")
