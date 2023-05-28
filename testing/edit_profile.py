import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
service = Service('C:\Program Files\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("http://127.0.0.1:8000/login/")
driver.maximize_window()
driver.find_element(By.ID, "email").send_keys("demo@gmail.com")
driver.find_element(By.ID, "password").send_keys("Demo@1234")
driver.find_element(By.ID, "submit").click()
time.sleep(1)
driver.find_element(By.ID, "accounts").click()
driver.find_element(By.ID, "edit").click()
driver.find_element(By.ID, "fname").send_keys("Demo")
driver.find_element(By.ID, "lname").send_keys("Demo")
driver.find_element(By.ID, "tel").send_keys("6708989853")
driver.find_element(By.ID, "save").click()
time.sleep(1)
expectedurl="http://127.0.0.1:8000/myprofile/"
currentur1=driver.current_url
if expectedurl== currentur1:
    print("Test Case Passed")
else:
    print("Failed")