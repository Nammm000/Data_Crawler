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


def browser_cookie(path):
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
    )
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_extension("proxy.zip")
    #chrome_options.add_argument(
    #'--proxy-server=%s' % proxy)

    browser = webdriver.Chrome(
    executable_path=path, options=chrome_options)

    return browser


browser1 = browser_cookie("./chromedriver1/chromedriver.exe")
browser2 = browser_cookie("./chromedriver2/chromedriver.exe")

# 2. Mở thử một trang web
cookies1 = pickle.load(open("my_cookie_1.pkl", "rb"))
for cookie in cookies1:
    browser1.add_cookie(cookie)

cookies2 = pickle.load(open("my_cookie_2.pkl", "rb"))
for cookie in cookies2:
    browser2.add_cookie(cookie)

sleep(random.randint(10, 15))
# 3. Refresh the browser

browser1.get("https://m.facebook.com")  # mbasic
browser2.get("https://m.facebook.com")
sleep(random.randint(10, 15))

browser1.get(
    "https://mbasic.facebook.com/tran.thanh.ne/posts/pfbid0GHAHDxHg6ENcAYQQ3EGXZvzn4myC3Jn787ESML1eTSML8D4MAPKa3y5WiSQg8psEl")
    # https://mbasic.facebook.com/tran.thanh.ne/posts/pfbid0GHAHDxHg6ENcAYQQ3EGXZvzn4myC3Jn787ESML1eTSML8D4MAPKa3y5WiSQg8psEl
    # https://mbasic.facebook.com/groups/704953753737448/posts/1322912711941546/
    # https://mbasic.facebook.com/TaylorSwiftVietnamFC/posts/pfbid0381SEUKjQjpYCFrSNTRiBjHcbQuCuLzuP8i8sEJnHNKUeSWiJHyL7iWYdkiRJyGGAl
# https://www.facebook.com/FCHuongQuocvn/posts/pfbid0FYMQLgdXNSxWtbvaudpQqzqqsPuwu1FzFoMRV3yVSGoSwfLaNGQ3QU78URobS5CLl
sleep(3)

comment_data_columns = ['commentID', 'UserName',
                        'Comment', 'Image-Video', 'Response', 'Profile_link']
comment_data = []

x = 1
y = 1
z = 0
nextBtn = ''

while x==1 and z<200:
    commentIDs = []
    if y==1:
        browser = browser1
    elif y==2:
        browser = browser2

    try:
        if z != 0:
            browser.get(nextBtn)
            sleep(random.randint(6, 15))
        
        userName = browser.find_elements(By.XPATH, '//div[@class][@id]/div/h3/a')
        a = len(userName)
        comment = browser.find_elements(By.XPATH, '//div[@class][@id]/div/h3/../div[1]')

        if a==len(comment):
            for i in range(0, a):
                comID = userName[i].find_element(By.XPATH, '../../..').get_attribute('id')
                if (comID in commentIDs):
                    continue
                else:
                    commentIDs.append(comID)
                
                xpathIMG = '//div[@id="' + comID + '"]/div/div[2]/div/a/img'
                xpathVID = '//div[@id="' + comID + '"]/div/div[2]/div/a'
                xpathICON = '//div[@id="' + comID + '"]/div/div[2]/img'
                xpathRES = '//div[@id="' + comID + '"]/div/div[4]/div/div/a'


                try:
                    res = browser.find_element(By.XPATH, xpathRES).text
                    resInt = int(re.search(r'\d+', res).group())
                except:
                    resInt = "0"

                IVILink = ''
                try:
                    img = browser.find_element(By.XPATH, xpathIMG).get_attribute('src')
                except:
                    img = 'x'

                try:
                    vid = browser.find_element(By.XPATH, xpathVID).get_attribute('href')
                except:
                    vid = 'x'

                try:
                    icon = browser.find_element(By.XPATH, xpathICON).get_attribute('src')
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
        nextBtn = browser.find_element(
            By.XPATH, '//div[contains(@id, "see_next")]/a').get_attribute('href')
        z += 1
        if y==2:
            y = 1
        else:
            y += 1

        sleep(random.randint(3, 5))
    except:
        x = 0


sleep(5)

df = pd.DataFrame(comment_data, columns=comment_data_columns)

print(df)
df.to_csv('fb_comments_data.csv')
df.to_json('fb_comments_data.json', orient="records")
