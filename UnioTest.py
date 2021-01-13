from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import json
def get_url_lists(soup):
    #单页面
    c_fonts = soup.find_all("h3", class_="t c_font")
    url_list=[]
    for c_font in c_fonts:
        url = " http://" + c_font.find("a").attrs["href"][2:]
        print(url)
        url_list.append(url)
    return url_list
def parase_one(url):
    result = dict()
    content_details = requests.get(url)
    soup_new = BeautifulSoup(content_details.text, "lxml")
    try :
        result['title']=''.join(list(soup_new.select('#dtl_l > div > h3 > a')[0].stripped_strings))
        result['abstract']=soup_new.find_all("p",class_="abstract")[0].get_text().strip()
        result["author"]=soup.find_all("p", class_="author_text")[0].get_text().strip()
        keywords=soup_new.find_all("p",class_="kw_main")
        if len(keywords) == 0 :
            keywords = soup_new.find_all("p", class_="kw_main_s")
        result['keywords']=list(keywords[0].stripped_strings)
    except IndexError:
        return result

    print(result)


def page_url_list(soup, page=0):
    print(soup.find_all("a", class_="n")[0]["href"])
    fir_page = "http://xueshu.baidu.com" + soup.find_all("a", class_="n")[0]["href"]
    url_lists = []
    for i in range(page):
        next_page = fir_page.replace("pn=10", "pn={:d}".format(i * 10))
        response = requests.get(next_page)
        soup_new = BeautifulSoup(response.text, "lxml")
        url_lists=url_lists+get_url_lists(soup_new)

    return url_lists
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
    soup = BeautifulSoup(content, 'lxml')
    # with open("1.html","w",encoding="utf-8") as f:
    #     f.write(str(soup.contents))
    # print(soup.contents)
    return soup

soup=driver_open("机器学习")
url_lists= page_url_list(soup,3)
with open("url_lists.txt","w",encoding="utf-8") as f:
    for i in url_lists:
        f.write(str(i)+"\n")
result =list()
f= open("result.json","w",encoding="utf-8")
for url in url_lists:
    t = parase_one(url)
    print(t)
    if t!=None:
        result.append(t)
json.dump(result,f)

