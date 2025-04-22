import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
            service = Service(executable_path="/usr/local/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(10)
            return driver
        except WebDriverException as e:
            print(f"[DRIVER ERROR] ChromeDriver issue: {str(e)}")
            raise

    def generate_email(self, index):
        if self.config['use_temp_email']:
            return f"{self.config['email_prefix']}{random.randint(1000,9999)}@tempmail.com"
        return f"{self.config['email_prefix']}+ref{index}@{self.config['email_domain']}"

    def register_account(self, email):
        try:
            print(f"Navigating to registration page...")
            self.driver.get("https://onprover.orochi.network/register")
            
            # Wait for page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            
            print("Locating form elements...")
            # Try multiple possible selectors for each field
            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email']"))
            
            password_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password' or @name='password']"))
            
            referral_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='referral_code' or contains(@id,'referral')]"))
            
            print("Filling form...")
            email_field.clear()
            email_field.send_keys(email)
            
            password_field.clear()
            password_field.send_keys(self.config['password'])
            
            referral_field.clear()
            referral_field.send_keys(self.config['referral_code'])
            
            # Handle terms checkbox if exists
            try:
                terms_checkbox = self.driver.find_element(
                    By.XPATH, "//input[@type='checkbox' and contains(@name, 'terms')]")
                if not terms_checkbox.is_selected():
                    terms_checkbox.click()
            except NoSuchElementException:
                pass
            
            # Submit form
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            submit_button.click()
            
            # Verify success
            try:
                WebDriverWait(self.driver, 20).until(
                    lambda d: "success" in d.current_url.lower() or "dashboard" in d.current_url.lower())
                print(f"[SUCCESS] Account {email} registered successfully!")
                return True
            except:
                print(f"[WARNING] Registration may have failed for {email}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to register {email}: {str(e)}")
            # Take screenshot for debugging
            self.driver.save_screenshot(f"error_{email}.png")
            return False

    def run(self):
        print("Starting referral process...")
        for i in range(1, self.config['account_count'] + 1):
            email = self.generate_email(i)
            print(f"\nRegistering account {i}/{self.config['account_count']} with email: {email}")
            self.register_account(email)
            time.sleep(random.uniform(self.config['min_delay'], self.config['max_delay']))
        
        print("\nReferral process completed!")
        self.driver.quit()

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
