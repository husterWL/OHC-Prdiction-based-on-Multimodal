'''
思路：
1.借用cookie和user-agent来访问页面中的class="EZC0YBrG Nfs9sicY"部分
2.然后在从列表中获取每一个视频的href
3.访问每一个href，然后从网页中提取视频地址，之后下载存储即可

上面这个思路应该是需要加载javascript的

1、还有一种思路是使用webdriver模拟人来爬取数据，也就是自动打开浏览器获取其中的源码链接

测试后发现由于视频资源链接为动态获取，直接requests.get拿不到视频地址
所以采取后一种方法 selenium+webdriver

抑或是找出界限之前的所有视频的url，放置到列表中
再访问列表进行下载
'''
from urllib import parse
import requests
import re
from bs4 import BeautifulSoup
import selenium
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import random
from Config import config
import time
from contextlib import closing
import json  

#抖音是js动态加载的，需要解密参数signature
headers = {
    'Connection':'keep-alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control':'max-age=0',
    'Cookie':'douyin.com; xg_device_score=7.710242117932399; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; __ac_referer=__ac_blank; ttwid=1%7CZAY4sBJZ9XMM9pWoPGdIfeIC_wK-E54--NByW5m7ZbA%7C1701222597%7C25dca317841c31fef0767f2c992bd107aaecea394f129efdee386b00668110b0; dy_swidth=1707; dy_sheight=1067; passport_csrf_token=fdc485ca1365a9a571ee65fc0fe3ab86; passport_csrf_token_default=fdc485ca1365a9a571ee65fc0fe3ab86; s_v_web_id=verify_lpj405t3_SFnk3D3x_2Tyx_4ign_8tnE_S18owaKwNeTP; bd_ticket_guard_client_web_domain=2; passport_assist_user=CkGpoosZ5ElotqtyO7W-uXIFL2eEOsL7yPtsjfkBliLQXp4Eb4iTiDjn6b9H0vjXIvsnu3GkmGGJSNSdqNNdKo73gRpKCjwnKJn8ATpZVT6DVW0inpSYM__oGEtDVQRmYQZTVhUWMfP2vQELJ0YBDj-Sl3eY3eizY-6yPRGqET_Cc8YQrMfCDRiJr9ZUIAEiAQMel1qy; n_mh=MwAHPg-ldy5vjDZa2m-0Uz32UYqHWuYijCFkNHJW2Oo; sso_uid_tt=33c77a2b51d3e31c7156851bbaf08fa1; sso_uid_tt_ss=33c77a2b51d3e31c7156851bbaf08fa1; toutiao_sso_user=626e24e0bbb55c2e4cd38b8c1e5c079f; toutiao_sso_user_ss=626e24e0bbb55c2e4cd38b8c1e5c079f; sid_ucp_sso_v1=1.0.0-KDI2OGQwZDdjZGEwZGQ2NzcyNjc5NmYxYzM5MmM4NjdlZjhiYTdjMWIKHwj3jPDJhvSzAxDmsZqrBhjvMSAMMIanmvgFOAZA9AcaAmxxIiA2MjZlMjRlMGJiYjU1YzJlNGNkMzhiOGMxZTVjMDc5Zg; ssid_ucp_sso_v1=1.0.0-KDI2OGQwZDdjZGEwZGQ2NzcyNjc5NmYxYzM5MmM4NjdlZjhiYTdjMWIKHwj3jPDJhvSzAxDmsZqrBhjvMSAMMIanmvgFOAZA9AcaAmxxIiA2MjZlMjRlMGJiYjU1YzJlNGNkMzhiOGMxZTVjMDc5Zg; passport_auth_status=8a990d2b1e1e87025d7c998b3f04eae6%2C; passport_auth_status_ss=8a990d2b1e1e87025d7c998b3f04eae6%2C; uid_tt=9dd03f0b28fd094e52e2e66917fef27b; uid_tt_ss=9dd03f0b28fd094e52e2e66917fef27b; sid_tt=265d9dcf4673605195baf8c1ed7d915a; sessionid=265d9dcf4673605195baf8c1ed7d915a; sessionid_ss=265d9dcf4673605195baf8c1ed7d915a; LOGIN_STATUS=1; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=6a89f51413907b597b09f8fabb3f04b9; __security_server_data_status=1; sid_guard=265d9dcf4673605195baf8c1ed7d915a%7C1701222636%7C5183997%7CSun%2C+28-Jan-2024+01%3A50%3A33+GMT; sid_ucp_v1=1.0.0-KGQ4MjU4MDVkYzczOTAyZDBmOWIwNzBhYzhmODA0YjQ2MWNmMDkwNzgKGwj3jPDJhvSzAxDssZqrBhjvMSAMOAZA9AdIBBoCaGwiIDI2NWQ5ZGNmNDY3MzYwNTE5NWJhZjhjMWVkN2Q5MTVh; ssid_ucp_v1=1.0.0-KGQ4MjU4MDVkYzczOTAyZDBmOWIwNzBhYzhmODA0YjQ2MWNmMDkwNzgKGwj3jPDJhvSzAxDssZqrBhjvMSAMOAZA9AdIBBoCaGwiIDI2NWQ5ZGNmNDY3MzYwNTE5NWJhZjhjMWVkN2Q5MTVh; my_rd=2; store-region=cn-hb; store-region-src=uid; SEARCH_RESULT_LIST_TYPE=%22single%22; FOLLOW_RED_POINT_INFO=%221%22; carnival_live_pull=1702270990561; EnhanceDownloadGuide=%222_1701996584_2_1702344055_2_1701998541%22; download_guide=%223%2F20231129%2F1%22; strategyABtestKey=%221702515202.459%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; publish_badge_show_info=%221%2C0%2C0%2C1702515414277%22; __ac_signature=_02B4Z6wo00f01Tm0iqAAAIDBz92DhbOq05k5lI4AACsaaaXL1EKmOAV244QclHN1qwHmFotCpCE3d2HEnfTW.KrMJSkemoJML5F8DdLEmkYgJkqvprOm5GRXx23-p9NPqlUd3R6fUdDM6FVR88; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2%2F1702569600000%2F0%2F1702517717785%2F0%22; csrf_session_id=99b0f4e50cd66e764ef104fa13e7bd7e; volume_info=%7B%22isUserMute%22%3Atrue%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.2%7D; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A1067%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2%2F1702569600000%2F0%2F0%2F1702519612725%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS0tQQXpldEVkZGdGZXRwUzhkRUtONlVRb2JHelh5Q0xpdElTSUcvNkNsYmpwdTRDaGM1bUxUdEU2SkZtSERoZ1IzSkpGQmp3TGo4QUhScEVoa0V5dTQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; odin_tt=1e521ce8aa31df8ed04cd6a9f0aa7c2acdd6f13eb63cb47549308bb1feeb38fc96150845887551c83b9aeb352b813876; tt_scid=2rY2krF4056P9VWqmjVuwwuVZhgnfhUW2KjpC3cS2FiYdHcRk.clxORSYGdLiSo0df36; msToken=cU-qjcZ5wjqOEED983G270d3HoQwb3ezxXhxs1x3BC69T9LqTfB4bENfsQDAhTknF6Q4LdeaAPRrEFffeDV0rIJXJqGfx3Za7V1oQb4FX1IF0knIleSciUeE2WIw; msToken=VYoLjhD2Yj8t7HTz4cSyIl_26oKzskRZYEua7NMyIoGq5Qc86ypZMEVa3vW8XiFrErKzOJdOl3kRKFzbfO6xJakjq-BDOKBveBdMA5jxkueBdWmIq-MZVWUpbSlE; __ac_nonce=0657a9d2900ed3ce0421b; IsDouyinActive=false; passport_fe_beating_status=false',
    'Sec-Ch-Ua':'"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'

}

data = {
    
}

# url = 'https://www.douyin.com/user/MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2'
url = 'https://www.douyin.com/user/MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2?showTab=favorite_collection'
# url = 'https://www.douyin.com/video/7300081063383158068'
# url = 'https://www.douyin.com/video/7305291937240665354'
# url = 'https://www.douyin.com/user/MS4wLjABAAAA8OWpsnPTnk8P7u_2_cPgl-vExjZ-IXaFyAR1BpbjZjg?vid=7306115162312903973' #努力的啊桐 respose444
# url = 'https://www.douyin.com/user/MS4wLjABAAAApKwDi1yiBXlcNrsZtUILmCJdvWR47OoFXu8zb0v-2iU?vid=7218502285100404005'#妙卡    respose444

#获得用户代理的随机数
def get_random_number(data):
    return random.randint(0, len(data)-1)

#使用普通spider获取主页收藏的视频链接
def crawl(site):
    random_index = get_random_number(config.user_agent_list)
    random_agent = config.user_agent_list[random_index]
    headers['User-agent'] = random_agent
    session = requests.Session()
    rep = session.get(site, headers=headers, allow_redirects=False, timeout=20)
    print(rep.status_code)
    data = rep.text
    print(data)
    bs = BeautifulSoup(data, 'html.parser')
    # favorite = bs.find('ul', class_ = 'EZC0YBrG Nfs9sicY')
    # print(favorite)
    # source = bs.find('video', class_ = '' )
    # print(source)
    render_data = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', data, re.S)[0]
    # print(render_data)
    parse_data_1 = parse.unquote(render_data)
    print(parse_data_1)
    # parse_data_2 = eval(parse_data_1)
    # print(parse_data_2)
    # video_url = 'https:' + re.findall('"playAddr":\[{"src":".*?{"src":"(.*?)"}]', parse_data_1, re.S)[0]
    # print(video_url)

#使用webdriver抓取javascript内容：
def imitate(site):
    # options = webdriver.EdgeOptions()
    # options = {
    #     'request_headers': headers,
    # }
    # headers_ = list(headers)    #将请求头字典转化为请求头列表
    browser = webdriver.Edge()  #seleniumwire_options = headers
    browser.get(site)
    time.sleep(20)
    with open('practice/mine_spider/cookies.txt','w') as f:
    # 将cookies保存为json格式
        f.write(json.dumps(browser.get_cookies()))

    # num = brouser.find_element_by_xpath('').text
    # time.sleep(20)
    browser.close()
# imitate(url)

##进入相应网页
options = webdriver.EdgeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
# 模拟请求，避免被反爬
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('detach', True)
# 获取请求信息，避免被反爬
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
user_ag = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188'
options.add_argument('user-agent=%s' % user_ag)
browser = webdriver.Edge(options = options)
browser.get(url)
browser.delete_all_cookies()
with open('practice/mine_spider/cookies.txt','r') as f:
    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookies_list = json.load(f)
    for cookie in cookies_list:
        browser.add_cookie(cookie)

browser.refresh()
time.sleep(10)
# browser.close()

##在我的收藏页面进入每一个收藏视频的原页面获取相应的视频地址/模拟鼠标悬停获取网络部分的mime_type属性为video_mp4的媒体文件
##1、按顺序遍历获取每一个视频的链接，直到最近下载的一个视频那里停止（这里的确认方法是将每次下载的第一个视频的原链接存储为一个文件，每次下载会将它读取出来，然后遍历的时候进行比较，看是否相同）
##1、这个方法的缺点就是如果那第一个视频被删除，那么也就代表它不会再出现在收藏列表中，那么会一直下载下去。
###1

##2、模拟鼠标获取网络日志中的媒体文件，确认方法同上。
###2    这里的重点是如何进行定位
src = browser.find_element(By.XPATH, '//*[@id="douyin-right-container"]/div[2]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div/ul/li[1]/div/a').get_attribute('href')
print(src)


#以下的JavaScript部分属性名会改变
#class="EZC0YBrG Nfs9sicY"
#class="Eie04v01 _Vm86aQ7 PISbKxf7"
#class="B3AsdZT9 chmb2GX8 DiMJX01_"
#视频是https://www.douyin.com/video /*******；图文是https://www.douyin.com/note/*******。
#相应的列表视频地址的js路径：document.querySelector("#douyin-right-container > div.tQ0DXWWO.DAet3nqK.userNewUi > div > div > div.GE_yTyVX > div > div > div.lNYhMAbF > div > div:nth-child(2) > div > div > ul > li:nth-child(1) > div > a")
##douyin-right-container > div.tQ0DXWWO.DAet3nqK.userNewUi > div > div > div.GE_yTyVX > div > div > div.lNYhMAbF > div > div:nth-child(2) > div > div > ul > li:nth-child(1) > div > a
#完整的xpath路径   /html/body/div[2]/div[1]/div[4]/div[2]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div/ul/li[1]/div/a
#上面的这个已经直接到链接了
#到scroll-list是/ul/这一等级，下面的li[x]代表的是收藏列表中的第x个视频

#以上方法还会遇到一个问题，就是有的收藏是note，也就是图文，而不是视频，这个还需要去判定

class douyin_spider():

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
        with open ('practice/mine_spider/cookies.txt', 'r') as f:
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
        with open('practice/mine_spider/cookies.txt','w') as f:
            f.write(json.dumps(browser.get_cookies()))
        browser.close()
        with open ('practice/mine_spider/cookies.txt', 'r') as f:
            self.cookies_list = json.load(f)
            
    def get_vedio_list(self):
        src = self.browser.find_element(By.XPATH, '//*[@id="douyin-right-container"]/div[2]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div/ul/li[1]/div/a').get_attribute('href')
        print(src)
