import os,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

MAIL = os.environ["email"]
PASSWORD = os.environ["password"]
TARGET = "thegoatagency"

class InstaFollower():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--detach")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/")
        wait = WebDriverWait(self.driver, 10)
        allow_cookies = wait.until(EC.presence_of_element_located((By.XPATH,
                        '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'))).click()
        email_input = wait.until(EC.presence_of_element_located((By.XPATH,
                        '//*[@id="loginForm"]/div/div[1]/div/label/input')))
        email_input.send_keys(MAIL)
        pass_input = wait.until(EC.presence_of_element_located((By.XPATH,
                        '//*[@id="loginForm"]/div/div[2]/div/label/input')))
        pass_input.send_keys(PASSWORD)
        pass_input.send_keys(Keys.ENTER)

    def find_followers(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(f"https://www.instagram.com/{TARGET}")
        followers = wait.until(EC.presence_of_element_located((By.XPATH,
                                                               '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a')))
        followers.click()
    def follow_accounts(self):
        wait = WebDriverWait(self.driver, 10)
        followers = wait.until(EC.presence_of_element_located((By.XPATH,
                        '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span')))
        followersNum = int(followers.text.replace(',',''))

        for i in range(1, followersNum):
            try:
                follow = wait.until(EC.presence_of_element_located((By.XPATH,
                                                  f'/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{i}]/div/div/div/div[3]/div/button')))
                follow.click()
                time.sleep(2)
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", follow)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(By.XPATH,
                                                         '/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]')
                cancel_button.click()
                time.sleep(1)
bot = InstaFollower()
bot.login()
time.sleep(5)
bot.find_followers()
time.sleep(5)
bot.follow_accounts()
time.sleep(10)
