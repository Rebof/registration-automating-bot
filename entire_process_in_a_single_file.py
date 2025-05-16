from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import random
import string
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

class RandomNumberGenerator:
    def __init__(self, length=10):
        self.length = length

    def generate(self):
        return ''.join(random.choices(string.digits, k=self.length))

class TempMailExtractor:
    def __init__(self, driver):
        self.driver = driver
        self.main_window = driver.current_window_handle

    def open_temp_mail(self):
        self.driver.execute_script("window.open('https://temp-mail.io/en');")
        time.sleep(5)
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


def select_checkbox_by_label(label_text):
    # Find <label> with text, then select the preceding-sibling <button>
    checkbox_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//label[contains(text(), '{label_text}')]/preceding-sibling::button"
        ))
    )
    checkbox_button.click()        

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
rng = RandomNumberGenerator()
number=rng.generate()
driver.find_element(By.NAME, "phoneNumber").send_keys(number)
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

#here i need to insert the name of the country, as region btn opens a search menu for the countries, we can type there 
search_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.XPATH,
        "/html/body/div[4]/div[1]/div[1]/input[1]"
    ))
)


country_name = "Canada"
search_input.send_keys(country_name)

# Click result
result_item = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]"
    ))
)
result_item.click()

# Simulate pressing ESC to close the dropdown
actions = ActionChains(driver)
actions.send_keys(Keys.ESCAPE).perform()

# Wait for the dropdown/search overlay to disappear
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((
        By.XPATH,
        "/html/body/div[4]/div[1]/div[1]/input[1]"
    ))
)

# Now click the Next button
next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
)
next_button.click()

# Optional: wait after clicking
time.sleep(3)
#new section
experience_dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[@role='combobox' and .//span[contains(., 'Select Your Experience Level')]]"
    ))
)
experience_dropdown_button.click()

options_container = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//div[@role='presentation']//div[1]"))
)

option_to_click = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,
        f"//div[@role='presentation']//div[1]"  # Replace with actual option selector
    ))
)
option_to_click.click()

actions = ActionChains(driver)
actions.send_keys(Keys.ESCAPE).perform()

# Enter value into number_of_students_recruited_annually
num_students_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "number_of_students_recruited_annually"))
)
num_students_input.clear()
num_students_input.send_keys("1000")

# Enter value into success_metrics
success_metrics_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "success_metrics"))
)
success_metrics_input.clear()
success_metrics_input.send_keys("20")

# Enter value into focus_area
focus_area_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "focus_area"))
)
focus_area_input.clear()
focus_area_input.send_keys("Computer Science")

time.sleep(3)

container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.gap-1.lg\\:gap-3.flex-wrap"))
)

# Find all checkbox wrapper divs inside container
checkbox_wrappers = container.find_elements(By.CSS_SELECTOR, "div.flex.flex-row.items-start")

# The labels you want to select (example)
labels_to_select = ["Career Counseling", "Some Other Checkbox Label"]

for wrapper in checkbox_wrappers:
    # Find the label text inside this wrapper
    label = wrapper.find_element(By.TAG_NAME, "label").text.strip()
    
    if label in labels_to_select:
        # Find the checkbox button inside this wrapper and click it if not already checked
        checkbox_btn = wrapper.find_element(By.CSS_SELECTOR, "button[role='checkbox']")
        
        # Check if it's already checked by reading aria-checked attribute
        aria_checked = checkbox_btn.get_attribute("aria-checked")
        if aria_checked == "false":
            checkbox_btn.click()
            print(f"Checked checkbox with label: {label}")
        else:
            print(f"Checkbox with label: {label} is already checked")




next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
)
next_button.click()

time.sleep(3)



#new section
business_reg_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "business_registration_number"))
)
business_reg_input.send_keys("BRN-123456789")

# Certification Details field
certification_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "certification_details"))
)
certification_input.send_keys("ISO 9001 Certified")

country_dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[3]/div[4]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[2]/button[1]"))
)
country_dropdown_button.click()

search_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search...']"))
)
search_input.clear()
search_input.send_keys("Canada")

country_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]"))
)
country_option.click()

# Step 4: Send ESC key to close the dropdown
search_input.send_keys(Keys.ESCAPE)

select_checkbox_by_label("Universities")
select_checkbox_by_label("Colleges")

time.sleep(3)

#file upoad procedure
import os
from PIL import Image
from pathlib import Path

file_path = Path(__file__).parent / "dummy.png"

if not os.path.exists(file_path):
    img = Image.new('RGB', (100, 100), color=(255, 255, 255))  # white square
    img.save(file_path)
    print(f"File '{file_path}' created.")
else:
    print(f"File '{file_path}' already exists.")

upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
upload_input.send_keys(str(file_path))


time.sleep(3)

next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
)
next_button.click()

time.sleep(10)

WebDriverWait(driver, 10).until(EC.url_contains("/admin/profile"))


#just check if successfull or not
# Check if the redirection is successful
current_url = driver.current_url
if current_url == "https://authorized-partner.netlify.app/admin/profile":
    print("✅ Successfully registered and redirected to profile page.")
else:
    print(f"❌ Registration may have failed. Current URL: {current_url}")

time.sleep(10)
driver.quit()    
