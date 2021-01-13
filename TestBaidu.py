from bs4 import BeautifulSoup
from selenium import webdriver
import time
# import pandas as pd
import requests
import re
from collections import defaultdict

def driver_open(key_word):
    url = "http://xueshu.baidu.com/"
    driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
#     driver = webdriver.Chrome("D:\\Program Files\\selenium_driver\\chromedriver.exe")
    driver.get(url)
    # time.sleep(10)
    driver.find_element_by_class_name('s_ipt').send_keys(key_word)
    # time.sleep(2)
    driver.find_element_by_class_name('s_btn_wr').click()
    # time.sleep(2)
    content = driver.page_source.encode('utf-8')
    driver.close()
    # with open("1.html","w",encoding="utf-8") as f:
    #     f.write(str(content))
    # print(content)
    soup = BeautifulSoup(content, 'lxml')
    with open("1.html","w",encoding="utf-8") as f:
        f.write(str(soup.contents))
    print(soup.contents)
    return soup
driver_open("机器学习")