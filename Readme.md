AI VideoSlide Creator
AI VideoSlide Creator is a Python-based script that allows you to create video slides using images. The script requires certain dependencies and configurations to be set up in order to work smoothly. Follow the instructions below to install and set it up.

Requirements
Python (Ensure you have Python installed)
Google Chrome (Used for web scraping or image downloading)
ChromeDriver (For Chrome WebDriver to interact with the browser)
Installation Instructions
Step 1: Install Dependencies
First, you need to install the required Python libraries. You can do this by running the following command:

bash
Copy code
pip install selenium moviepy pillow requests
Step 2: Configure ChromeDriver
You need to configure ChromeDriver to enable the script to interact with the Chrome browser.

Download ChromeDriver:
Ensure that you have the ChromeDriver executable compatible with your version of Chrome. You can download it from here.

Edit the ChromeDriver Path:
Open the image_download.py file in your project directory. Look for the following section of the code:

python
Copy code
# ChromeDriver setup
driver_path = r"C:\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # Suppress console logs
Update the driver_path variable to match the location of your chromedriver.exe file.

Example (for Windows):

python
Copy code
driver_path = r"C:\path\to\your\chromedriver.exe"
Step 3: Run the Script
Once you’ve configured ChromeDriver, run the aivideo_create.py script to generate your video slides.

bash
Copy code
python aivideo_create.py
Enjoy creating your AI-powered video slides!