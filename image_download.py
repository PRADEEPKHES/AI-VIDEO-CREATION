import os
import shutil
import time
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

# Log setup
log_file = None

def log_message(message):
    global log_file
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}"
    print(log_entry)
    if log_file:
        log_file.write(log_entry + "\n")
        log_file.flush()

# Initialize web_image folder and log file
if os.path.exists("web_image"):
    shutil.rmtree("web_image")  # Remove previous web_image folder
os.makedirs("web_image")  # Create a new web_image folder

# Set up log file in the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "image_download_log.txt")
log_file = open(log_file_path, "w")

# Download image function
def download_image(src, img_path):
    try:
        response = requests.get(src, stream=True, timeout=60)  # Set timeout for download
        if response.status_code == 200:
            with open(img_path, "wb") as img_file:
                img_file.write(response.content)
            log_message(f"Downloaded: {img_path}")
            return img_path  # Return the path of the downloaded image
        else:
            log_message(f"Failed to download: {src}")
            return None
    except Exception as e:
        log_message(f"Error downloading {src}: {e}")
        return None

# ChromeDriver setup
driver_path = r"C:\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # Suppress console logs

# First, user prompt
prompt = input("Enter topic to search for images: ")
log_message(f"Starting process for topic: {prompt}")

# Open ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open Pexels
    search_url = f"https://www.pexels.com/search/{prompt}/?orientation=landscape"
    driver.get(search_url)
    time.sleep(5)

    # Scroll down to load images initially
    for _ in range(50):
        driver.execute_script("window.scrollBy(0, 40);")
        time.sleep(0.1)  # 100ms per scroll
    time.sleep(4.6)
    downloaded_images = set()
    image_urls = []

    max_images = 30

    while len(downloaded_images) < max_images:
        images = driver.find_elements(By.XPATH, '//article/a/img')
        log_message(f"Found {len(images)} images on the page.")

        for img in images:
            if len(downloaded_images) >= max_images:
                break

            src = img.get_attribute("src")
            if src and src not in downloaded_images:  # Avoid duplicates
                src = src.split("?")[0]
                image_name = f"img_{len(downloaded_images) + 1}.jpeg"
                img_path = f"web_image/{image_name}"
                image_urls.append((src, img_path))
                downloaded_images.add(src)

        # Scroll again to load more images if needed
        if len(downloaded_images) < max_images:
            for _ in range(20):  # Scroll a bit more to load additional images
                driver.execute_script("window.scrollBy(0, 40);")
                time.sleep(0.1)  # 100 milliseconds per frame
            time.sleep(4.6)

    # Download images in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as executor:  # Adjust number of threads as needed
        results = list(executor.map(lambda p: download_image(p[0], p[1]), image_urls))

    log_message(f"Image extraction completed: {len(downloaded_images)} images downloaded.")

finally:
    driver.quit()
    log_message("Closed Chrome.")

# Run image_resize.py after downloads are complete
try:
    subprocess.run(["python", os.path.join(script_dir, "image_resize.py")])
except Exception as e:
    log_message(f"Error running image_resize: {e}")

# Script finished
log_message("Script finished. Press Enter to exit.")

if log_file:
    log_file.close()

input()
