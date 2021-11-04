from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

VBsearch = []

driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://www.instagram.com")

username = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='username']")))
password = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='password']")))

username.clear()
password.clear()
username.send_keys("")   # Username
password.send_keys("")   # Password

log_in = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit']"))).click()
not_now = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Not Now')]"))).click()
#not_now2 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Not Now')]"))).click()

query = "marketing"
page = driver.get("https://www.instagram.com/explore/tags/" + query)

driver.execute_script("window.scrollBy(0,1000000)")
time.sleep(5)
driver.execute_script("window.scrollBy(0,1000000)")
time.sleep(5)
driver.execute_script("window.scrollBy(0,1000000)")
time.sleep(5)
driver.execute_script("window.scrollBy(0,1000000)")
time.sleep(5)
driver.execute_script("window.scrollBy(0,1000000)")
time.sleep(5)
driver.execute_script("window.scrollBy(0,1000000)")
time.sleep(5)
driver.execute_script("window.scrollBy(0,1000000)")
time.sleep(5)


links = driver.find_elements_by_tag_name('a')
links = [link.get_attribute('href') for link in links]


df = pd.DataFrame(links,columns=["InstagramPostLink"])
print(df)
df.to_csv('PostLink.csv')