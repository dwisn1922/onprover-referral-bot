import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OnproverReferralBot:
    def __init__(self, config):
        self.config = config
        self.driver = self.setup_driver()
        
    def setup_driver(self):
        chrome_options = Options()
        if self.config['headless']:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Use ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)  # seconds
        return driver
    
    def generate_email(self, index):
        if self.config['use_temp_email']:
            return f"{self.config['email_prefix']}{random.randint(1000,9999)}@tempmail.com"
        else:
            return f"{self.config['email_prefix']}+ref{index}@{self.config['email_domain']}"
    
    def register_account(self, email):
        try:
            self.driver.get("https://onprover.orochi.network/register")
            
            # Wait for elements to be present
            wait = WebDriverWait(self.driver, 15)
            
            # Find elements using more robust selectors
            email_field = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='email'], input[type='email']")
            ))
            password_field = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='password'], input[type='password']")
            ))
            referral_field = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='referral_code']")
            ))
            
            # Fill the form
            email_field.send_keys(email)
            password_field.send_keys(self.config['password'])
            referral_field.send_keys(self.config['referral_code'])
            
            # Handle terms checkbox if exists
            try:
                terms_checkbox = self.driver.find_element(
                    By.CSS_SELECTOR, "input[type='checkbox'][name*='terms']"
                )
                terms_checkbox.click()
            except NoSuchElementException:
                pass
            
            # Submit form
            submit_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']")
            ))
            submit_button.click()
            
            # Wait for success or timeout
            try:
                wait.until(EC.url_contains("success") | EC.url_contains("dashboard"))
                print(f"[SUCCESS] Akun {email} berhasil didaftarkan!")
                return True
            except:
                print(f"[WARNING] Pendaftaran {email} mungkin gagal, verifikasi manual diperlukan")
                return False
                
        except Exception as e:
            print(f"[ERROR] Gagal mendaftarkan {email}: {str(e)}")
            return False
    
    def run(self):
        print("Memulai proses pendaftaran referral...")
        for i in range(1, self.config['account_count'] + 1):
            email = self.generate_email(i)
            print(f"Mendaftarkan akun {i}/{self.config['account_count']} dengan email: {email}")
            self.register_account(email)
            time.sleep(random.uniform(self.config['min_delay'], self.config['max_delay']))
        
        print("Proses pendaftaran selesai!")
        self.driver.quit()

if __name__ == "__main__":
    # Load configuration
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    # Run bot
    bot = OnproverReferralBot(config)
    bot.run()
    
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
