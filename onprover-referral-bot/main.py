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
        
        # Explicit paths
        chrome_options.binary_location = "/usr/bin/google-chrome"
        
        try:
            service = Service(executable_path="/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(15)
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
            
            # Wait for page to load completely
            WebDriverWait(self.driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete")
            
            print("Taking screenshot of page...")
            self.driver.save_screenshot("registration_page.png")
            
            print("Locating form elements...")
            # More robust element finding with multiple fallbacks
            email_field = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, 
                "//input[@type='email']|//input[@name='email']|//input[contains(@id,'email')]")))
            
            password_field = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH,
                "//input[@type='password']|//input[@name='password']|//input[contains(@id,'password')]")))
            
            referral_field = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH,
                "//input[@name='referral_code']|//input[contains(@id,'referral')]")))
            
            print("Filling form...")
            self.driver.execute_script("arguments[0].value = arguments[1]", email_field, email)
            self.driver.execute_script("arguments[0].value = arguments[1]", password_field, self.config['password'])
            self.driver.execute_script("arguments[0].value = arguments[1]", referral_field, self.config['referral_code'])
            
            # Check for CAPTCHA
            try:
                iframe = self.driver.find_element(By.XPATH, "//iframe[contains(@src,'recaptcha')]")
                print("[WARNING] CAPTCHA detected - manual intervention required")
                input("Please solve the CAPTCHA and press Enter to continue...")
            except NoSuchElementException:
                pass
                
            # Submit form
            submit_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH,
                "//button[@type='submit']|//input[@type='submit']")))
            submit_button.click()
            
            # Verify success
            try:
                WebDriverWait(self.driver, 30).until(
                    lambda d: "success" in d.current_url.lower() or 
                             "dashboard" in d.current_url.lower() or
                             "welcome" in d.current_url.lower())
                print(f"[SUCCESS] Account {email} registered successfully!")
                return True
            except:
                print(f"[WARNING] Registration may have failed for {email}")
                self.driver.save_screenshot(f"error_{email}.png")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to register {email}: {str(e)}")
            self.driver.save_screenshot(f"error_{email}.png")
            return False

    def run(self):
        print("Starting referral process...")
        for i in range(1, self.config['account_count'] + 1):
            email = self.generate_email(i)
            print(f"\nRegistering account {i}/{self.config['account_count']} with email: {email}")
            success = self.register_account(email)
            time.sleep(random.uniform(self.config['min_delay'], self.config['max_delay']))
            
            if not success and self.config['pause_on_failure']:
                input("Press Enter to continue after fixing the issue...")
        
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
