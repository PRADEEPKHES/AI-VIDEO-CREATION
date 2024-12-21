import os
import subprocess

# Define the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Run image_download.py
try:
    subprocess.run(["python", os.path.join(script_dir, "image_download.py")], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while trying to run image_download.py: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print("image_download.py ran successfully.")
