from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to your ChromeDriver
# driver_path = "/home/piyushverma/Downloads/Scrapping/chrome-linux64"  # Adjust with your path
driver_path = "/home/piyushverma/Downloads/Scrapping/chromedriver-linux64/chromedriver"

# Create a Service object with the path to the ChromeDriver
service = Service(driver_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Open the webpage
driver.get("https://www.freepik.com/search?format=search&last_filter=query&last_value=Credit%20Cards&query=Credit%20Cards")  # Adjust with the correct URL

# Wait for the page to load
time.sleep(5)

# Find all the figure elements (this can be adjusted to be more specific if needed)
figure_elements = driver.find_elements(By.TAG_NAME, "figure")

# Loop through the first 15 elements (if there are that many)
for i in range(min(15, len(figure_elements))):
    try:
        # Find the 'Download' button inside the current figure's aside tag
        # download_button = figure_elements[i].find_element(By.CSS_SELECTOR, 'aside button[data-cy="download-thumbnail"]')
        # download_button = WebDriverWait(figure_elements[i], 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'aside button[data-cy="download-thumbnail"]'))
        # )
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-cy="download-thumbnail"]'))
        )

        # Scroll to the element to ensure it is in view
        actions = ActionChains(driver)
        actions.move_to_element(download_button).perform()
        
        # Click the download button to initiate the image download
        download_button.click()

        # Wait a bit before moving to the next download
        time.sleep(2)
    except Exception as e:
        print(f"Error while downloading image {i+1}: {e}")

# Wait for the downloads to complete (adjust this if needed)
time.sleep(5)

# Close the browser
driver.quit()
