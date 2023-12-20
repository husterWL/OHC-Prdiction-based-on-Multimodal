'''
可能先爬取各个医生的主页URL，然后再根据URL来爬取医生主页的信息
'''
import seleniumwire
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
from Config import config
import random
import json

def get_random_number(data):
    return random.randint(0, len(data)-1)

class haodf_spider():

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
    