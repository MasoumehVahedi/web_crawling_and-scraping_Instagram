import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramScraping:

    def __init__(self, username, password):
        self.Username = username
        self.Password = password
        self.driver = webdriver.Chrome('chromedriver.exe')
        
        self.login = self.Login()
        self.links = self.__read_csv()


    def Login(self):
        self.driver.get("https://instagram.com/")

        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        username.clear()
        password.clear()
        username.send_keys("...")    # Username
        password.send_keys("...")    # Password

        log_in = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        log_in.click()

        not_now = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]")))
        not_now.click()
        not_now2 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]")))
        not_now2.click()

    def __read_csv(self):
        df = pd.read_csv("IGTopprofilefilename.csv")
        URLs = df["KOL"]
        links = []
        for url in URLs:
            links.append(url)
        # print(links)
        return links

    def __search(self, link):
        # To search JSON data structure
        self.driver.get(link + "?__a=1")
        soup = BeautifulSoup(self.driver.page_source, "html.parser").get_text()
        jsondata = json.loads(soup)
        user_info = jsondata["graphql"]["user"]
        return user_info

    def get_profile_Email(self, biography):
        # Email Regex
        emailRegex = re.search(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+', biography)
        if emailRegex != None:
            Email = emailRegex.group(0)
        else:
            Email = "null"
        return Email

    def get_profile_PhoneNumber(self, biography):
        # Phone number Regex
        phoneRegex = re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', biography)
        if phoneRegex != None:
            PhoneNumber = phoneRegex.group(0)
        else:
            PhoneNumber = "null"
        return PhoneNumber

    def get_username(self):
        # Username of the given user
        return self.user_info["username"]

    def get_full_name(self):
        return self.user_info["full_name"]

    def get_biography(self):
        return self.user_info["biography"]

    def _category_name(self):
        return self.user_info["category_name"]

    def get_number_of_followers(self):
        return self.user_info["edge_followed_by"]["count"]

    def get_number_of_following(self):
        return self.user_info["edge_follow"]["count"]

    def get_number_of_posts(self):
        return self.user_info["edge_owner_to_timeline_media"]["count"]

    def get_website(self):
        return self.user_info["external_url"]

    def _is_private(self):
        return self.user_info["is_private"]

    def _is_verified(self):
        return self.user_info["is_verified"]

    def _is_business_account(self):
        return self.user_info["is_business_account"]

    def _is_professional_account(self):
        return self.user_info["is_professional_account"]

    def _business_contact_method(self):
        return self.user_info["business_contact_method"]

    def get_posts(self):
        # Only give the top 5 posts details from each user
        post_list = []
        post_detail = self.user_info["edge_owner_to_timeline_media"]["edges"]
        for i in post_detail:
            information = {}

            # Add all details in the information dict
            information["likes"] = i["node"]["edge_liked_by"]["count"]
            information["comments"] = i["node"]["edge_media_to_comment"]["count"]
            information["caption"] = i["node"]["accessibility_caption"]
            information["is_video"] = i["node"]["is_video"]
            information["timestap"] = i["node"]["taken_at_timestamp"]
            information["location"] = i["node"]["location"]
            information["shortcode"] = i["node"]["shortcode"]
            information["post_url"] = f'https://www.instagram.com/p/{i["node"]["shortcode"]}/'

            posts = namedtuple("Post", information.keys())(*information.values())
            post_list.append(posts)
        return post_list


    def get_profile_information(self):
        ProfileInfosearch = []

        for link in self.links:
            self.driver.get(link)
            # Number of followers
            FollowerNumber = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
            FollowerNumber = FollowerNumber.text    # is a string with non-numeric values, for example: "534k"

            # To convert str into float number
            if FollowerNumber.endswith("k"):
                Follower_Number = FollowerNumber.replace("k", "")
                Follower_Number = float(Follower_Number) * 1000
                Follower_Number = int(Follower_Number)
            elif FollowerNumber.endswith("m"):
                Follower_Number = FollowerNumber.replace("m", "")
                Follower_Number = float(Follower_Number) * 10**6
                Follower_Number = int(Follower_Number)
            else:
                Follower_Number = FollowerNumber.replace(",", "")
                Follower_Number = int(Follower_Number)
            print(Follower_Number)

            # Get only user ptofiles more than 1000 followers
            if Follower_Number > 1000:
                self.user_info = self.__search(link)
                Username = self.get_username()
                Fullname = self.get_full_name()
                Biography = self.get_biography()
                FollowerNumber = self.get_number_of_followers()
                FollowingNumber = self.get_number_of_following()
                PostNumber = self.get_number_of_posts()
                BusinessAccount = self._is_business_account()
                ProfessionalAccount = self._is_professional_account()
                ContactMethod = self._business_contact_method()
                PageCategory = self._category_name()
                PrivatePage = self._is_private()
                ExternalUrl = self.get_website()
                Posts = self.get_posts()
                Email = self.get_profile_Email(Biography)
                PhoneNumber = self.get_profile_PhoneNumber(Biography)

                profile_info = {
                    'Username': Username,
                    'Full Name': Fullname,
                    'Biography': Biography,
                    'Post Number': PostNumber,
                    'Follower Number': FollowerNumber,
                    'Following Number': FollowingNumber,
                    'Is Business Account': BusinessAccount,
                    'Is Professional Account': ProfessionalAccount,
                    'Contact Method': ContactMethod,
                    'Page Category': PageCategory,
                    'Phone Number': PhoneNumber,
                    'Is Private': PrivatePage,
                    'Website': ExternalUrl,
                    'Post Details': Posts,
                    'Emails': Email,
                }
                ProfileInfosearch.append(profile_info)
            else:
                continue
        return ProfileInfosearch


if __name__ == '__main__':
    Login = InstagramScraping(username='', password='')
    ProfileInfosearch = Login.get_profile_information()
    df = pd.DataFrame(ProfileInfosearch)
    # print(df)
    df.to_csv('InstagramInfo.csv')