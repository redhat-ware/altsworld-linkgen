import random
import string
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from threading import Thread
from threading import Lock
from google.colab import files

# Function to generate a random alphanumeric string
def get_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

# Function to save URL to a text file
def save_url(url):
    with open('hit.txt', 'a') as f:
        f.write(url + '\n')
    files.download('hit.txt')  # Download the file to your local system

# Global counter for log entries
log_counter = 0

# Global set for unique URLs and a lock for thread-safe operations
unique_urls = set()
lock = Lock()

# Function to log bad URLs
def log_bad_url(url):
    global log_counter
    log_counter += 1
    print(f'\\033[91m {log_counter}: {url}')  # Red color for bad URLs

# Function to log good URLs
def log_good_url(url):
    global log_counter
    log_counter += 1
    print(f'\\033[92m {log_counter}: {url}')  # Green color for good URLs

# Function to open URL in browser and check if it's good
def open_url():
    while True:
        random_string = get_random_string(17)
        url = f"https://altsworld.atshop.io/order/{random_string}/completed"
        with lock:
            if url in unique_urls:
                continue
            unique_urls.add(url)
        options = Options()
        options.add_argument('--headless')  # We'll run Chrome in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options for Chrome in Colab
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.get(url)
        time.sleep(5)  # Wait for 5 seconds
        current_url = driver.current_url
        if current_url == 'https://altsworld.atshop.io/':
            log_bad_url(current_url)
        else:
            save_url(url)
            log_good_url(url)
            time.sleep(2)  # Wait for 2 seconds
            driver.get(url)
            time.sleep(2.5)  # Wait for 2.5 seconds
            current_url = driver.current_url
            if current_url == 'https://altsworld.atshop.io/':
                log_bad_url(current_url)
            else:
                save_url(url)
                log_good_url(url)
        driver.quit()

# Create and start 20 threads
for _ in range(20):
    thread = Thread(target=open_url)
    thread.start()
