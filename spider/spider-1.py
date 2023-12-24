'''
可能先爬取各个医生的主页URL，然后再根据URL来爬取医生主页的信息
'''
from urllib import parse
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

import seleniumwire
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
from Config import config
import random
import json

# url = 'https://www.haodf.com/doctor/list-all-xinxueguanneike.html'
# url = 'https://www.haodf.com/doctor/610483525.html'
url = 'https://www.haodf.com/doctor/5808/fuwu-wenzhen.html'
# url = 'https://www.haodf.com/doctor/5808/pingjia-zhenliao.html'

def get_random_number(data):
    return random.randint(0, len(data)-1)

#利用selenium架构爬虫
class haodf_spider_sele():

    #初始化
    def __init__(self, url) -> None:
        pass
        self.url = url
        self.options = webdriver.EdgeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)
        # 模拟请求，避免被反爬
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('detach', True)
        # 获取请求信息，避免被反爬
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.options.add_experimental_option("prefs", prefs)
        random_index = get_random_number(config.user_agent_list)
        random_agent = config.user_agent_list[random_index]
        self.options.add_argument('user-agent=%s' % random_agent)
        self.browser = webdriver.Edge(options = self.options)
        with open ('', 'r') as f:
            self.cookies_list = json.load(f)
        
        
    def base(self):
        pass
        self.browser.get(self.url)
        self.browser.delete_all_cookies()
        for cookie in self.cookies_list:
            self.browser.add_cookie(cookie)
        self.browser.refresh()
        time.sleep(10)

    def get_cookie(self):
        browser = webdriver.Edge()  #seleniumwire_options = headers
        browser.get(self.url)
        time.sleep(20)
        with open('','w') as f:
            f.write(json.dumps(browser.get_cookies()))
        browser.close()
        with open ('', 'r') as f:
            self.cookies_list = json.load(f)
            
    def get_data(self):
        src = self.browser.find_element(By.XPATH, '').get_attribute('')
        print(src)

    def doc_spider(self):
        pass

    def pat_spider(self):
        pass

    def sys_spider(self):
        pass

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    # 'Cookie': 'g=3909_1698570580704; HMF_CI=3b827a4b3881da007e34c1138709aa2af3b23c844c3591f63d5545b04034d964b5bda328e0a7984393b8f44e260dc14d7ca8d1b6d53c39427b1e82b964d0a02d4f; sdmsg=1; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1703084256,1703142559,1703167131,1703212423; g=HDF.149.6584b161228e4; krandom_a119fcaa84=823479; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1703231242   ',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    # 'Referer': 'https://www.haodf.com/doctor/5808/xinxi-jieshao.html',
    # 'If-None-Match': 'W/"1a06-AjWYN1MfPJVJ5GktKwbcRgYaaj8"',
}

#利用requests无法进入fuwu-wenzhen.html页面，可能是因为有data-v-b5789996（vue渲染页面）的元素
class haodf_spider_req():
    
    #初始化
    def __init__(self, headers) -> None:
        self.headers = headers
        pass
    
    def crawl(self):
        session = requests.Session()    #注意加括号，这是实例化session对象
        rep = session.get(url = url, headers = self.headers)
        data = rep.text
        # print(data)
        list = re.findall('<div data-v-b5789996 class="wrap-outer">(.*?)</div>', data, re.S)
        print('111\n')
        print(list)
        # html = etree.HTML(rep.content, etree.HTMLParser(encoding = 'utf-8'))
        # doc = html.xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/span[2]/text()')
        # print(doc)
        # for i in doc:
            # print(i)
        pass
        
        # list = re.findall('<ul class="fam-doc-ul js-fam-doc-ul">(.*?)</ul>', data, re.S)
        # print(list)

    def get_random_number(data):
        return random.randint(0, len(data)-1)
    
    def get_random_agent(self):
        random_index = get_random_number(config.user_agent_list)
        random_agent = config.user_agent_list[random_index]
        self.headers['User-agent'] = random_agent
        pass

#测试selenium是否可以访问fuwu_wenzhen.html
def sele_test():
    options = webdriver.EdgeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('useAutomationExtension', False)
    # 模拟请求，避免被反爬
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('detach', True)
    # 获取请求信息，避免被反爬
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # options.add_experimental_option("prefs", prefs)
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188'
    options.add_argument('user-agent=%s' % agent)
    browser = webdriver.Edge(options = options)
    browser.get(url)
    time.sleep(10)

def req_test():
    pass
    session = requests.Session()    #注意加括号，这是实例化session对象
    rep = requests.get(url = url, headers = headers)
    print(rep.status_code)
    # data = rep.text
    html = etree.HTML(rep.content, etree.HTMLParser(encoding = 'utf-8'))
    doc = html.xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/span[2]/text()')
    print(doc)
