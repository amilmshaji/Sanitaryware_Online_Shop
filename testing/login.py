
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Update the path to the Microsoft Edge WebDriver
PATH= 'C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe'
driver = webdriver.Edge(PATH)

driver.get("http://127.0.0.1:8000/login/")
driver.maximize_window()
driver.find_element(By.ID, "email").send_keys("demo@gmail.com")
driver.find_element(By.ID, "password").send_keys("Demo@1234")
driver.find_element(By.ID, "submit").click()

expectedurl="http://127.0.0.1:8000/"
currenturl=driver.current_url
if expectedurl == currenturl:
   print("Test Case Passed")
else:
    print("Failed")
