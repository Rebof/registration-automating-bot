from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def select_checkbox_by_label(driver, label_text):
    # Wait for container of checkboxes to be present
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.gap-1.lg\\:gap-3.flex-wrap"))
    )
    checkbox_wrappers = container.find_elements(By.CSS_SELECTOR, "div.flex.flex-row.items-start")

    found = False

    for wrapper in checkbox_wrappers:
        try:
            label = wrapper.find_element(By.TAG_NAME, "label").text.strip()
            if label == label_text:
                checkbox_btn = wrapper.find_element(By.CSS_SELECTOR, "button[role='checkbox']")
                if checkbox_btn.get_attribute("aria-checked") == "false":
                    checkbox_btn.click()
                    print(f"☑️ Checked checkbox: {label}")
                else:
                    print(f"☑️ Already checked: {label}")
                found = True
                break
        except Exception as e:
            continue

    if not found:
        raise Exception(f"❌ Checkbox with label '{label_text}' not found.")

def select_checkbox_by_label_final(driver, label_text):
    # Find <label> with text, then select the preceding-sibling <button>
    checkbox_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//label[contains(text(), '{label_text}')]/preceding-sibling::button"
        ))
    )
    checkbox_button.click() 