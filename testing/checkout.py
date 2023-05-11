import time

import selenium
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
driver.find_element(By.ID, "shop").click()


# driver.find_element(By.ID, "1").click()
driver.find_element(By.ID, "cart").click()
driver.find_element(By.ID, "checkout").click()


time.sleep(2)


expectedurl="http://127.0.0.1:8000/checkout/"
currentur1=driver.current_url
if expectedurl== currentur1:
    print("Test Case Passed")
else:
    print("Failed")