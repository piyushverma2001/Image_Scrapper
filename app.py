import os
import time
import zipfile

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
driver_path = "./chromedriver-win64/chromedriver.exe"
user_data_dir = r"C:\Users\piyus\AppData\Local\BraveSoftware\Brave-Browser\User Data"

options = Options()
options.binary_location = brave_path
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Profile-Selenium")
# options.add_argument("--disable-dev-shm-usage")     #Linux only
options.add_argument("--no-sandbox")
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.freepik.com/search?format=search&last_filter=query&last_value=Credit%20Cards&query=Credit%20Cards")
time.sleep(5)
imageElement = driver.find_elements(By.TAG_NAME, "figure")

for i, figure in enumerate(imageElement[:10]):
    try:
        actions = ActionChains(driver)
        actions.move_to_element(figure).perform()
        time.sleep(1)

        download_button = figure.find_element(By.CSS_SELECTOR, 'button[data-cy="download-thumbnail"]')
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(download_button))
        download_button.click()
        print(f"Image {i+1} downloaded successfully.")

        zip_path = None
        timeout = time.time() + 20
        while time.time() < timeout:
            for filename in os.listdir(download_dir):
                if filename.endswith(".zip"):
                    zip_path = os.path.join(download_dir, filename)
                    break
            if zip_path:
                break
            time.sleep(1)

        if zip_path:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if file.endswith('.jpg'):
                        zip_ref.extract(file, os.path.join(download_dir, f"image_{i+1}"))
                        print(f"Extracted .jpg from ZIP for image {i+1}")
            os.remove(zip_path)

        else:
            print(f"No ZIP found for image {i+1}")

    except Exception as e:
        print(f"Error while downloading image {i+1}: {e}")

driver.quit()
