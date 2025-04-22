import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

class OnproverReferralBot:
    def __init__(self, config):
        self.config = config
        try:
            self.driver = self.setup_driver()
        except Exception as e:
            print(f"[CRITICAL] Failed to initialize WebDriver: {str(e)}")
            sys.exit(1)
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        if self.config['headless']:
            chrome_options.add_argument("--headless=new")
        
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        
        # Set explicit path to Chrome binary
        chrome_options.binary_location = "/usr/bin/google-chrome"
        
        try:
            # Use ChromeDriverManager to automatically handle driver installation
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(15)
            return driver
        except WebDriverException as e:
            print(f"[DRIVER ERROR] ChromeDriver issue: {str(e)}")
            raise

    # ... [rest of your existing methods remain the same] ...

if __name__ == "__main__":
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
        
        bot = OnproverReferralBot(config)
        bot.run()
    except Exception as e:
        print(f"[FATAL ERROR] {str(e)}")
        sys.exit(1)
    
# Set the correct paths for your environment
chrome_binary_path = "/usr/bin/google-chrome"
chromedriver_path = "/usr/local/bin/chromedriver"

chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
chrome_options.add_argument("--headless")  # Remove if you want to see the browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
