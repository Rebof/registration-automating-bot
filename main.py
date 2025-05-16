from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

from helpers.temp_mail import TempMailExtractor
from helpers.random_generator import RandomNumberGenerator
from helpers.checkbox_selector import select_checkbox_by_label, select_checkbox_by_label_final
from helpers.file_uploader import ensure_dummy_file_exists

driver = webdriver.Chrome()
driver.get("https://authorized-partner.netlify.app/register")
print("🌐 Opened registration page.")
assert "register" in driver.current_url, "❌ Registration page did not load."

# Temp mail setup
temp_mail = TempMailExtractor(driver)
temp_mail.open_temp_mail()
temp_email = temp_mail.get_email_address()
assert "@" in temp_email, "❌ Failed to fetch a valid temporary email."
temp_mail.switch_to_registration_tab()

# Step 1: Initial checkbox and continue
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "remember")))
checkbox = driver.find_element(By.ID, "remember")
if not checkbox.is_selected():
    checkbox.click()
    print("🟢 Remember checkbox selected.")
driver.find_element(By.XPATH, "//button[text()='Continue']").click()

# Step 2: Fill form
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("John")
driver.find_element(By.NAME, "lastName").send_keys("Doe")
driver.find_element(By.NAME, "email").send_keys(temp_email)
number = RandomNumberGenerator().generate()
driver.find_element(By.NAME, "phoneNumber").send_keys(number)
driver.find_element(By.NAME, "password").send_keys("MyStrongPassword123!")
driver.find_element(By.NAME, "confirmPassword").send_keys("MyStrongPassword123!")
driver.find_element(By.XPATH, "//button[text()='Next']").click()
print("📝 Submitted basic user details.")

# Step 3: Get OTP
time.sleep(10)
temp_mail.switch_to_temp_mail_tab()
otp = temp_mail.open_inbox_and_get_otp()
assert otp.isdigit() and len(otp) == 6, f"❌ OTP format invalid: {otp}"
temp_mail.switch_to_registration_tab()
driver.find_element(By.CSS_SELECTOR, 'input[data-input-otp="true"]').send_keys(otp)
driver.find_element(By.XPATH, "//button[text()='Verify Code']").click()

# Step 4: Agency details
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "agency_name"))).send_keys("My Agency")
driver.find_element(By.NAME, "role_in_agency").send_keys("Director")
driver.find_element(By.NAME, "agency_website").send_keys("www.instagram.com")
driver.find_element(By.NAME, "agency_address").send_keys("123 Street")
driver.find_element(By.NAME, "agency_email").send_keys("contact@myagency.com")

region_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Select Your Region of Operation']]"))
)
region_button.click()
search_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[1]/div[1]/input[1]")))
search_input.send_keys("Canada")

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]"))
).click()
ActionChains(driver).send_keys(Keys.ESCAPE).perform()

driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

# Step 5: Experience details
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and .//span[contains(., 'Select Your Experience Level')]]"))
).click()
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@role='presentation']//div[1]"))
).click()
ActionChains(driver).send_keys(Keys.ESCAPE).perform()

driver.find_element(By.NAME, "number_of_students_recruited_annually").send_keys("1000")
driver.find_element(By.NAME, "success_metrics").send_keys("85")
driver.find_element(By.NAME, "focus_area").send_keys("Engineering")

# Select checkboxes
container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.gap-1.lg\\:gap-3.flex-wrap"))
)
assert container is not None, "❌ Checkbox container not found."
checkbox_labels = ["Career Counseling"]
for label in checkbox_labels:
    select_checkbox_by_label(driver, label)

driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
time.sleep(3)

# Step 6: Final details
select_checkbox_by_label_final(driver, "Universities")
select_checkbox_by_label_final(driver, "Colleges")

driver.find_element(By.NAME, "business_registration_number").send_keys("BRN-987654321")
driver.find_element(By.NAME, "certification_details").send_keys("ISO Certified")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[4]/div[1]/div[1]/div[1]/div[2]/form/div/div[2]/button"))).click()
search_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search...']")))
search_input.send_keys("Canada")
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]"))
).click()
search_input.send_keys(Keys.ESCAPE)

# Upload file
upload_path = ensure_dummy_file_exists()
assert upload_path is not None, "❌ Dummy file path is None."
upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
upload_input.send_keys(upload_path)

driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()

# Final assertion
WebDriverWait(driver, 10).until(EC.url_contains("/admin/profile"))
final_url = driver.current_url
assert final_url == "https://authorized-partner.netlify.app/admin/profile", f"❌ Expected success page but got {final_url}"
print("✅ Successfully completed registration!")

driver.quit()
