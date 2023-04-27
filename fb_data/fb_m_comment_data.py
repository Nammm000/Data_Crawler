import pickle
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import sys
import random
import pandas as pd

from selenium.webdriver.common.proxy import Proxy, ProxyType

def parse_fb_url(string):
    """parses facebook cdn urls"""

    # convert to raw string
    raw_string = string.encode("unicode_escape").decode()

    # manual inspection of the url reveals the encoding
    replacement_map = {
        r"\x03a": ":",
        r"\x03d": "=",
        r"\x16": "&",
        r" ": "",
    }

    for key, replacement in replacement_map.items():
        raw_string = raw_string.replace(key, replacement)

    return raw_string


def browser_cookie():
    chrome_options = Options()

    chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
    )
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_extension("proxy.zip")

    browser = webdriver.Chrome(
    executable_path="./chromedriver5/chromedriver.exe", options=chrome_options)

    return browser


browser = browser_cookie()

# 2. Mở thử một trang web
browser.get("https://m.facebook.com")  # mbasic

cookies = pickle.load(open("my_cookie_1.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

# 3. Refresh the browser
browser.get("https://m.facebook.com") 

browser.get(
    "https://m.facebook.com/tran.thanh.ne/posts/pfbid0GHAHDxHg6ENcAYQQ3EGXZvzn4myC3Jn787ESML1eTSML8D4MAPKa3y5WiSQg8psEl")
    # https://mbasic.facebook.com/tran.thanh.ne/posts/pfbid0GHAHDxHg6ENcAYQQ3EGXZvzn4myC3Jn787ESML1eTSML8D4MAPKa3y5WiSQg8psEl
    # https://mbasic.facebook.com/TaylorSwiftVietnamFC/posts/pfbid0381SEUKjQjpYCFrSNTRiBjHcbQuCuLzuP8i8sEJnHNKUeSWiJHyL7iWYdkiRJyGGAl
sleep(3)

last_height = browser.execute_script("return document.body.scrollHeight")
x = 0
while True and x<=20:
    # //*[contains(text(), "Xem thêm bình luận…")]
    showmore_link = browser.find_element(By.XPATH, '//a[@class="_108_"]')
    showmore_link.click()
    sleep(random.randint(3, 5))

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    x += 1
"""
showmore_link = browser.find_element(By.XPATH, '//a[@class="_108_"]')
showmore_link.click()
sleep(6)
"""

comment_data_columns = ['commentID', 'UserName',
                        'Comment', 'Image-Video', 'Response', 'Profile_link']
comment_data = []


#comment_list = browser.find_elements(By.XPATH, '//div[@class="_2a_i"]')
#print("***", type(comment_list))

userName = browser.find_elements(By.XPATH, '//div[@class="_2b05"]/a')
a = len(userName)
comment = browser.find_elements(By.XPATH, '//div[@data-sigil="comment-body"]')
#profile_link = browser.find_elements(By.XPATH, '//div[@class="_2b00"]/a')


if a == len(comment):
    for i in range(0, a):
        comID = comment[i].get_attribute('data-commentid')
        xpathRES = '//div[@data-reply-to="' + comID + '"]/a/span[2]'
        try:
            res = browser.find_element(By.XPATH, xpathRES).text
            resInt = int(re.search(r'\d+', res).group())
        except:
            resInt = "0"

        IVILink = ''
        try:
            img = comment[i].find_element(
                By.XPATH, '../../div[2]/div/a').get_attribute('href')
        except:
            img = 'x'

        try:
            comment[i].find_element(
                By.XPATH, '../../div[2]/div/div/div').click()
            vid = comment[i].find_element(
                By.XPATH, '../../div[2]/div/div/video').get_attribute('src')
        except:
            vid = 'x'

        try:
            s = comment[i].find_element(
                By.XPATH, '../../div[2]/i').get_attribute('style')
            s1 = s.split(" url('")[1]
            icon = s1.split("');")[0]
            icon = parse_fb_url(icon)
            #emo: //div[@data-sigil="comment-body"]/../../div[2]/div/i
        except:
            icon = 'x'

        if img!='x' :
            IVILink = img
        elif vid!='x' :
            IVILink = vid
        elif icon!='x' :
            IVILink = icon
        else:
            IVILink = 'x'

        comment_data.append([comID, userName[i].text, comment[i].text, IVILink,
                            resInt, userName[i].get_attribute('href')])
else:
    print("***")


sleep(5)

df = pd.DataFrame(comment_data, columns=comment_data_columns)

print(df)
df.to_csv('fb_comments_data.csv')
df.to_json('fb_comments_data.json', orient="records")
