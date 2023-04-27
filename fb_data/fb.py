import pickle
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import random

chrome_options = Options()

chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# chrome_options.add_extension("proxy.zip")
browser1 = webdriver.Chrome(
    executable_path="./chromedriver3/chromedriver.exe", options=chrome_options)



# 2. Mở thử một trang web
browser1.get("https://m.facebook.com")  # mbasic https://www.facebook.com/?sk=welcome
sleep(random.randint(2, 4))


txtUser1 = browser1.find_element(
    By.ID, "m_login_email").send_keys("td563822@gmail.com") 
# vulongh5834@gmail.com xxx
# td563822@gmail.com xxx
# 000xyz.abc2001@gmail.com dang cho xxx
# ntu50347@gmail.com gOogle90210 24/4/2023 xxx
# lnhat14333@gmail.com 
# nba5167036@gmail.com  
# bmai37399@gmail.com
# vunamm533@gmail.com
# 19020372@vnu.edu.vn

txtPass1 = browser1.find_element(By.XPATH, '//*[@id="m_login_password"]')
txtPass1.send_keys("QqqPPassword99. ")
sleep(random.randint(1, 3))
txtPass1.send_keys(Keys.ENTER)
sleep(25)

browser1.get("https://m.facebook.com/")
sleep(50)

pickle.dump(browser1.get_cookies(), open("my_cookie_3.pkl", "wb"))

browser1.close()
browser1.quit()

"""
proxyList = [
    '116.98.191.244:10003'
    # '216.215.123.174:8080'
    # '50.174.7.152:80'
]

chrome_options.add_argument(
    '--proxy-server=%s' % random.choice(proxyList))
"""