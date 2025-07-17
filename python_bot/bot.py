from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# Set up Chrome
driver = webdriver.Chrome()
driver.get("http://localhost:3000")
time.sleep(3)  # wait for React app to mount JS

# Simulate mouse movement
actions = ActionChains(driver)
body = driver.find_element(By.TAG_NAME, "body")

for _ in range(5):
    try:
        x_offset = random.randint(0, 200)
        y_offset = random.randint(0, 100)
        actions.move_to_element_with_offset(body, x_offset, y_offset).perform()
        time.sleep(0.2)
    except:
        continue

# Find links
links = driver.find_elements(By.CLASS_NAME, "link")
valid_links = [link for link in links if link.get_attribute("href")]

if not valid_links:
    print("❌ No valid links found.")
    driver.quit()
    exit()

# Click a random link (opens new tab)
selected_link = random.choice(valid_links)
href = selected_link.get_attribute("href")
print(f"👉 Clicking: {href}")
selected_link.click()

time.sleep(4)  # simulate reading the opened tab

# Switch back to original tab
original_window = driver.window_handles[0]
if len(driver.window_handles) > 1:
    new_window = driver.window_handles[1]
    driver.switch_to.window(new_window)
    driver.close()  # close the opened tab
    driver.switch_to.window(original_window)  # back to main page
    print("🔁 Switched back to original tab.")

time.sleep(10)
# Trigger endTracking manually
try:
    driver.execute_script("endTracking()")
    print("📤 endTracking() triggered manually.")
except Exception as e:
    print("❌ Failed to call endTracking():", e)

time.sleep(2)  # allow fetch() to complete

print("✅ Done. Closing browser.")
driver.quit()
