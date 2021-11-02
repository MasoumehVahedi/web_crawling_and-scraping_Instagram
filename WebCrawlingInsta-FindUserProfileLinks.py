from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

UserProfileLinksearch = []

driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://www.instagram.com")

username = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='username']")))
password = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='password']")))

username.clear()
password.clear()
username.send_keys("")   # Instagram ID
password.send_keys("")   # Password

log_in = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit']"))).click()
not_now = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Not Now')]"))).click()
not_now2 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Not Now')]"))).click()



df = pd.read_csv("PostLinkfilename.csv")
URLs = df["InstagramPostLink"]
links = []
for url in URLs:
    links.append(url)

# print(links)

urls = links
for url in urls:
    driver.get(url)
    try:
        UserProfile = driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a')
    except Exception as e:
        UserProfile = None
    try:
        UserProfile1 = UserProfile.get_attribute('href')
    except Exception as e:
        UserProfile1 = None

    try:
        LikeNumber = driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/a')
    except Exception as e:
        LikeNumber = None

    try:
        LikeNumber2 = LikeNumber.text
    except Exception as e:
        LikeNumber2 = None

    element_info = {
        'UserProfileLink': UserProfile1,
        'Likes': LikeNumber2,
    }

    UserProfileLinksearch.append(element_info)

df = pd.DataFrame(UserProfileLinksearch)
print(df)
df.to_csv('IGTopprofilefilename.csv')
