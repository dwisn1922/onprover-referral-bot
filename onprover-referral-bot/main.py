import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

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
    
    # Untuk Selenium 4.6+ tidak perlu executable_path
    service = webdriver.ChromeService()
    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    return driver
    
    def generate_email(self, index):
        if self.config['use_temp_email']:
            return f"{self.config['email_prefix']}{random.randint(1000,9999)}@tempmail.com"
        else:
            return f"{self.config['email_prefix']}+ref{index}@{self.config['email_domain']}"
    
    def register_account(self, email):
        try:
            self.driver.get("https://onprover.orochi.network/register")
            time.sleep(random.uniform(2, 4))
            
            # Isi form pendaftaran
            self.driver.find_element(By.NAME, "email").send_keys(email)
            self.driver.find_element(By.NAME, "password").send_keys(self.config['password'])
            self.driver.find_element(By.NAME, "referral_code").send_keys(self.config['referral_code'])
            
            # Handle terms and conditions jika ada
            try:
                terms_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox' and contains(@name, 'terms')]")
                terms_checkbox.click()
            except NoSuchElementException:
                pass
            
            # Submit form
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            time.sleep(random.uniform(3, 6))
            
            # Verifikasi pendaftaran berhasil
            try:
                success_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'Success')]")
                print(f"[SUCCESS] Akun {email} berhasil didaftarkan!")
                return True
            except NoSuchElementException:
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
    # Load konfigurasi
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    # Jalankan bot
    bot = OnproverReferralBot(config)
    bot.run()
