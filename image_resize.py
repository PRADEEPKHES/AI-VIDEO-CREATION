import os
import time
import subprocess
from PIL import Image
from moviepy.editor import ImageClip

# Log setup function
def log_message(log_file_path, message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}"
    print(log_entry)
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry + "\n")

# Initialize logging for image resizing
log_file_path_images = "image_resize_log.txt"
if os.path.exists(log_file_path_images):
    os.remove(log_file_path_images)

try:
    log_message(log_file_path_images, "Starting image resizing process from images.")

    # Define paths to source and destination folders
    image_folder = os.path.join(os.getcwd(), "web_image")
    temp_folder = os.path.join(os.getcwd(), "resized_image")

    # Ensure the destination folder exists or create it
    if os.path.exists(temp_folder):
        log_message(log_file_path_images, "Resized image folder exists. Deleting...")
        for file in os.listdir(temp_folder):
            os.remove(os.path.join(temp_folder, file))
        os.rmdir(temp_folder)
    os.makedirs(temp_folder)

    # Get a list of image files in the source folder
    image_files = [file for file in os.listdir(image_folder) if file.lower().endswith((".jpg", ".jpeg", ".png"))]
    num_images = len(image_files)

    # Log the number of images found
    log_message(log_file_path_images, f"Found {num_images} images.")

    if num_images == 0:
        raise Exception("No images found. Cannot create resized images.")

    # Resize each image to approximately 500 KB
    for image_name in image_files:
        image_path = os.path.join(image_folder, image_name)
        try:
            with Image.open(image_path) as img:
                img_format = img.format
                quality = 85  # Start with a reasonable quality setting

                # Save the image to the destination folder with reduced quality
                resized_image_path = os.path.join(temp_folder, image_name)

                while True:
                    img.save(resized_image_path, format=img_format, quality=quality, optimize=True)
                    if os.path.getsize(resized_image_path) <= 500 * 1024 or quality <= 10:  # Target: ~500 KB
                        break
                    quality -= 5  # Decrease quality stepwise

                log_message(log_file_path_images, f"Resized and saved {image_name} to {resized_image_path}")
        except Exception as img_error:
            log_message(log_file_path_images, f"Error processing {image_name}: {img_error}")

except Exception as e:
    log_message(log_file_path_images, f"Error during processing: {e}")

# Initialize logging for video clip creation
log_file_path_videos = "video_clip_log.txt"
if os.path.exists(log_file_path_videos):
    os.remove(log_file_path_videos)

try:
    log_message(log_file_path_videos, "Starting video clip creation process from images.")

    # Define the path to the "resized_image" folder and temporary folder for video clips
    image_folder = os.path.join(os.getcwd(), "resized_image")
    temp_folder = os.path.join(os.getcwd(), "video_clip_tempfolder")

    # Remove existing temporary folder if it exists, and create a new one
    if os.path.exists(temp_folder):
        for file in os.listdir(temp_folder):
            os.remove(os.path.join(temp_folder, file))
        os.rmdir(temp_folder)
    os.makedirs(temp_folder)

    # Load all JPEG image paths from the "resized_image" folder
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if img.lower().endswith((".jpeg", ".jpg"))]

    # Log the number of images found
    num_images = len(images)
    log_message(log_file_path_videos, f"Found {num_images} images.")

    if num_images == 0:
        raise Exception("No images found. Cannot create video clips.")

    # Set duration per image (5 seconds)
    duration_per_image = 6  # seconds

    # Create temporary video clips for each image
    for idx, img in enumerate(images):
        temp_video_clip_path = os.path.join(temp_folder, f"video_clip_{idx}.mp4")  # Change to .mp4
        img_clip = ImageClip(img).set_duration(duration_per_image).resize(height=720).set_fps(10)  
        img_clip.write_videofile(temp_video_clip_path, codec="libx264", fps=10, audio=False)  # MP4 format
        log_message(log_file_path_videos, f"Created temporary video clip: {temp_video_clip_path}")

except Exception as e:
    log_message(log_file_path_videos, f"Error creating video clip: {e}")

finally:
    # Log completion and run another script if it exists
    log_message(log_file_path_videos, "Script finished.")
    
    script_dir = os.getcwd()  # Get current working directory
    
    try:
        subprocess.run(["python", os.path.join(script_dir, "video_combine.py")])
        log_message(log_file_path_videos, "'video_combine.py' executed successfully.")
        
    except Exception as e:
        log_message(log_file_path_videos, f"Error running video_combine: {e}")
