import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TempMailExtractor:
    def __init__(self, driver):
        self.driver = driver
        self.main_window = driver.current_window_handle

    def open_temp_mail(self):
        self.driver.execute_script("window.open('https://temp-mail.io/en');")
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        print("🟢 Opened Temp Mail in new tab.")

    def get_email_address(self):
        time.sleep(5)
        email_elem = self.driver.find_element(By.ID, "email")
        temp_email = email_elem.get_attribute("value")
        print(f"📧 Temp Email: {temp_email}")
        return temp_email

    def open_inbox_and_get_otp(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "line-clamp-2"))
        )
        otp_elem = self.driver.find_element(By.CLASS_NAME, "line-clamp-2")
        otp_text = otp_elem.text.strip()
        otp_match = re.search(r'\d{6}', otp_text)

        if otp_match:
            print(f"🔑 OTP extracted: {otp_match.group(0)}")
            return otp_match.group(0)
        else:
            raise AssertionError("❌ Failed to extract OTP")

    def switch_to_temp_mail_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_registration_tab(self):
        self.driver.switch_to.window(self.main_window)

    def close_temp_mail_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.main_window)
