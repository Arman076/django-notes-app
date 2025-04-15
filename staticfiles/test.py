from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()  # You can use any supported browser

driver.get("http://13.233.63.179:8081")  # URL of your Django app

# Interact with the form
note_input = driver.find_element(By.NAME, "note")
note_input.send_keys("This is a test note")
note_input.send_keys(Keys.RETURN)  # Submit the form

time.sleep(2)  # Wait for the page to refresh

# Check if the note appears on the page
note_text = driver.find_element(By.XPATH, "//li[text()='This is a test note']")
assert note_text.is_displayed(), "Test failed: Note not found"

driver.quit()
