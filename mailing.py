from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class TempMailExtractor:
    def __init__(self, driver):
        self.driver = driver
        self.main_window = driver.current_window_handle

    def open_temp_mail(self):
        self.driver.execute_script("window.open('https://temp-mail.io/en');")
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def get_email_address(self):
        time.sleep(5)
        email_elem = self.driver.find_element(By.ID, "email")
        temp_email = email_elem.get_attribute("value")
        return temp_email

    def open_inbox_and_get_otp(self):
        # Wait until the inbox is loaded and a new mail is active
        pass
        WebDriverWait(self.driver, 20).until(
        EC.presence_of_element_located((
            By.CLASS_NAME,
            "line-clamp-2"  # Use the class name directly
        ))
    )
        otp_elem = self.driver.find_element(By.CLASS_NAME, "line-clamp-2")
        otp_text = otp_elem.text.strip()
        otp_match = re.search(r'\d{6}', otp_text)

        if otp_match:
            return otp_match.group(0)  # Return the OTP (the matched 6-digit number)
        else:
            return None

    def switch_to_temp_mail_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_registration_tab(self):
        self.driver.switch_to.window(self.main_window)

    def close_temp_mail_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.main_window)

# Initialize driver
driver = webdriver.Chrome()

# Step 1: Load registration page
driver.get("https://authorized-partner.netlify.app/register")
temp_mail = TempMailExtractor(driver)

# Step 2: Open TempMail tab and get email
temp_mail.open_temp_mail()
temp_email = temp_mail.get_email_address()
print("Temp Email:", temp_email)

# Step 3: Fill registration form
temp_mail.switch_to_registration_tab()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "remember")))
checkbox = driver.find_element(By.ID, "remember")
if not checkbox.is_selected():
    checkbox.click()

driver.find_element(By.XPATH, "//button[text()='Continue']").click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName")))
driver.find_element(By.NAME, "firstName").send_keys("John")
driver.find_element(By.NAME, "lastName").send_keys("Doe")
driver.find_element(By.NAME, "email").send_keys(temp_email)
driver.find_element(By.NAME, "phoneNumber").send_keys("9813837494")
driver.find_element(By.NAME, "password").send_keys("MyStrongPassword123!")
driver.find_element(By.NAME, "confirmPassword").send_keys("MyStrongPassword123!")
driver.find_element(By.XPATH, "//button[text()='Next']").click()

# Step 4: Wait for email to arrive (Added a brief sleep time for mail arrival)
time.sleep(10)

# Step 5: Extract OTP
temp_mail.switch_to_temp_mail_tab()
otp = temp_mail.open_inbox_and_get_otp()
print("OTP extracted:", otp)

# Step 6: Back to registration tab
temp_mail.switch_to_registration_tab()

otp_field = driver.find_element(By.CSS_SELECTOR, 'input[data-input-otp="true"]')  # Use the unique data attribute
otp_field.send_keys(otp)
time.sleep(3)
button = driver.find_element(By.XPATH, "//button[text()='Verify Code']")
button.click()
time.sleep(5)

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "agency_name"))
)
agency_name_field = driver.find_element(By.NAME, "agency_name")
agency_name_field.send_keys("Your Agency Name")

# Step 3: Wait for the "role_in_agency" field and enter a value
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "role_in_agency"))
)
role_in_agency_field = driver.find_element(By.NAME, "role_in_agency")
role_in_agency_field.send_keys("Your Role in Agency")

# Step 4: Wait for the "agency_website" field and enter a value
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "agency_website"))
)
agency_website_field = driver.find_element(By.NAME, "agency_website")
agency_website_field.send_keys("www.instagram.com")

# Step 5: Wait for the "agency_address" field and enter a value
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "agency_address"))
)
agency_address_field = driver.find_element(By.NAME, "agency_address")
agency_address_field.send_keys("ghar")


driver.find_element(By.NAME, "agency_email").send_keys("Youragency@mailinator.com")
region_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[.//span[text()='Select Your Region of Operation']]"
    ))
)
region_button.click()
region_button.send_keys("Nepal")
time.sleep(5)

# Step 6: Wait for the "Next" button to be clickable and click it
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
)
next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
next_button.click()

# Step 7: Optional: Wait for the next page to load or perform further actions
time.sleep(3)  # Optional, you can replace this with WebDriverWait for a specific condition

# Close driver after the task is complete
# driver.quit()