from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import json
import time
def get_url_lists(soup):
    #单页面
    c_fonts = soup.find_all("h3", class_="t c_font")
    url_list=[]
    for c_font in c_fonts:
        url = " http://" + c_font.find("a").attrs["href"][2:]
        print(url)
        url_list.append(url)
    return url_list
def driver_open(key_word,page):
    url = "http://xueshu.baidu.com/"
    driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
    driver.get(url)
    driver.find_element_by_class_name('s_ipt').send_keys(key_word)
    driver.find_element_by_class_name('s_btn_wr').click()
    content = driver.page_source.encode('utf-8')
    # driver.close()
    soup = BeautifulSoup(content, 'lxml')
    fir_page = "http://xueshu.baidu.com" + soup.find_all("a", class_="n")[0]["href"]
    url_lists = []
    for i in range(page):
        next_page = fir_page.replace("pn=10", "pn={:d}".format(i * 10))
        driver.get(next_page)
        # response = requests.get(next_page)
        time.sleep(10)
        soup_new = BeautifulSoup(driver.page_source.encode('utf-8'), "lxml")
        url_lists = url_lists + get_url_lists(soup_new)
        time.sleep(10)
        if len(url_lists)%10 == 0:
            write_url_lists(url_lists)
        time.sleep(10)
        print(len(url_lists))
    write_url_lists(url_lists)
    driver.close()
    # return soup
def write_url_lists(url_lists):
    with open("url_lists.txt","w",encoding="utf-8") as f:
        for i in url_lists:
            f.write(str(i)+"\n")
def parase_one(url,driver):
    result = dict()
    driver.get(url)
    # content_details = requests.get(url)
    soup_new = BeautifulSoup(driver.page_source.encode('utf-8'), "lxml")
    try :
        result['title']=soup_new.find_all("div",class_="main-info")[0].h3.text.strip()
        result['abstract']=soup_new.find_all("p",class_="abstract")[0].get_text().strip()
        result["author"]=soup_new.find_all("p", class_="author_text")[0].get_text().strip()
        keywords=soup_new.find_all("p",class_="kw_main")
        if len(keywords) == 0 :
            keywords = soup_new.find_all("p",attrs={"data-click":"{\'button_tp\':\'keyword\'}"})
        result['keywords']=list(keywords[0].stripped_strings)
    except IndexError as e:
        print(url)
        print(e)
        # print(driver.page_source.encode('utf-8'),)
        return None
    print(result)
    return result
# driver_open("机器学习",100)
with open("url_lists.txt","r",encoding="utf-8") as f:
    url_lists=list(f.readlines())
result=[]
# f= open("result.json","w",encoding="utf-8")
def get_result():
    driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
    cnt = 0
    num = 1
    for url in url_lists:
        url=url.strip()
        r = parase_one(url,driver)
        if r!= None:
            result.append(r)
        else :
            cnt= cnt + 1
        if cnt > 3:
            driver.close()
            time.sleep(300)
            driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
            cnt = 0
        time.sleep(60)
        if len(result) %10==0:
            num = num+1
            name="result_"+str(num)+".json"
            try:
                with open(name, "w", encoding="utf-8") as f:
                    json.dump(result, f)
            except Exception:
                print("clear")
                time.sleep(60)
            result.clear()
        # time.sleep(20)
        # if len(result) == 20:
        #     break

get_result()
