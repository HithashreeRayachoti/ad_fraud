from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# --- Setup ---
driver = webdriver.Chrome()
driver.get("http://localhost:3000")  # your local React site
time.sleep(3)  # allow JS to mount

actions = ActionChains(driver)
body = driver.find_element(By.TAG_NAME, "body")
width = driver.execute_script("return window.innerWidth")
height = driver.execute_script("return window.innerHeight")

# --- Simulated human-like mouse movement ---
def simulate_mouse_wandering(steps=100, delay=0.03):
    for _ in range(steps):
        x = random.randint(0, driver.execute_script("return window.innerWidth") - 1)
        y = random.randint(0, driver.execute_script("return window.innerHeight") - 1)

        driver.execute_script("""
            const e = new MouseEvent('mousemove', {
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: arguments[0],
                clientY: arguments[1]
            });
            document.dispatchEvent(e);
        """, x, y)

        time.sleep(delay + random.uniform(0.01, 0.05))

def bot_instant_click():
    time.sleep(1)
    link = driver.find_element(By.CLASS_NAME, "link")
    link.click()
bot_instant_click()

# --- Find and click random link ---
links = driver.find_elements(By.CLASS_NAME, "link")
valid_links = [link for link in links if link.get_attribute("href")]

if not valid_links:
    print("❌ No valid links found.")
    driver.quit()
    exit()

selected_link = random.choice(valid_links)
href = selected_link.get_attribute("href")
print(f"👉 Clicking: {href}")
selected_link.click()

time.sleep(4)  # simulate user reading new page

# --- Handle tabs ---
original_window = driver.window_handles[0]
if len(driver.window_handles) > 1:
    new_window = driver.window_handles[1]
    driver.switch_to.window(new_window)
    driver.close()
    driver.switch_to.window(original_window)
    print("🔁 Switched back to original tab.")

# --- Manually trigger endTracking() ---
time.sleep(2)
try:
    driver.execute_script("endTracking()")
    print("📤 endTracking() triggered manually.")
except Exception as e:
    print("❌ Failed to call endTracking():", e)

time.sleep(2)  # allow tracking to complete
print("✅ Done. Closing browser.")
driver.quit()
