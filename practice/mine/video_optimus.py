'''
思路：
1.借用cookie和user-agent来访问页面中的class="EZC0YBrG Nfs9sicY"部分
2.然后在从列表中获取每一个视频的href
3.访问每一个href，然后从网页中提取视频地址，之后下载存储即可


抑或是找出界限之前的所有视频的url，放置到列表中
再访问列表进行下载
'''
from urllib import parse
import requests
import re
import urllib
from bs4 import BeautifulSoup
import selenium

session = requests.Session()
#抖音是js动态加载的，需要解密参数signature
headers = {
    'Connection':'keep-alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control':'max-age=0',
    'Cookie':'douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; ttwid=1%7CZAY4sBJZ9XMM9pWoPGdIfeIC_wK-E54--NByW5m7ZbA%7C1701222597%7C25dca317841c31fef0767f2c992bd107aaecea394f129efdee386b00668110b0; dy_swidth=1707; dy_sheight=1067; passport_csrf_token=fdc485ca1365a9a571ee65fc0fe3ab86; passport_csrf_token_default=fdc485ca1365a9a571ee65fc0fe3ab86; s_v_web_id=verify_lpj405t3_SFnk3D3x_2Tyx_4ign_8tnE_S18owaKwNeTP; bd_ticket_guard_client_web_domain=2; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; passport_assist_user=CkGpoosZ5ElotqtyO7W-uXIFL2eEOsL7yPtsjfkBliLQXp4Eb4iTiDjn6b9H0vjXIvsnu3GkmGGJSNSdqNNdKo73gRpKCjwnKJn8ATpZVT6DVW0inpSYM__oGEtDVQRmYQZTVhUWMfP2vQELJ0YBDj-Sl3eY3eizY-6yPRGqET_Cc8YQrMfCDRiJr9ZUIAEiAQMel1qy; n_mh=MwAHPg-ldy5vjDZa2m-0Uz32UYqHWuYijCFkNHJW2Oo; sso_uid_tt=33c77a2b51d3e31c7156851bbaf08fa1; sso_uid_tt_ss=33c77a2b51d3e31c7156851bbaf08fa1; toutiao_sso_user=626e24e0bbb55c2e4cd38b8c1e5c079f; toutiao_sso_user_ss=626e24e0bbb55c2e4cd38b8c1e5c079f; sid_ucp_sso_v1=1.0.0-KDI2OGQwZDdjZGEwZGQ2NzcyNjc5NmYxYzM5MmM4NjdlZjhiYTdjMWIKHwj3jPDJhvSzAxDmsZqrBhjvMSAMMIanmvgFOAZA9AcaAmxxIiA2MjZlMjRlMGJiYjU1YzJlNGNkMzhiOGMxZTVjMDc5Zg; ssid_ucp_sso_v1=1.0.0-KDI2OGQwZDdjZGEwZGQ2NzcyNjc5NmYxYzM5MmM4NjdlZjhiYTdjMWIKHwj3jPDJhvSzAxDmsZqrBhjvMSAMMIanmvgFOAZA9AcaAmxxIiA2MjZlMjRlMGJiYjU1YzJlNGNkMzhiOGMxZTVjMDc5Zg; passport_auth_status=8a990d2b1e1e87025d7c998b3f04eae6%2C; passport_auth_status_ss=8a990d2b1e1e87025d7c998b3f04eae6%2C; uid_tt=9dd03f0b28fd094e52e2e66917fef27b; uid_tt_ss=9dd03f0b28fd094e52e2e66917fef27b; sid_tt=265d9dcf4673605195baf8c1ed7d915a; sessionid=265d9dcf4673605195baf8c1ed7d915a; sessionid_ss=265d9dcf4673605195baf8c1ed7d915a; LOGIN_STATUS=1; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=6a89f51413907b597b09f8fabb3f04b9; __security_server_data_status=1; sid_guard=265d9dcf4673605195baf8c1ed7d915a%7C1701222636%7C5183997%7CSun%2C+28-Jan-2024+01%3A50%3A33+GMT; sid_ucp_v1=1.0.0-KGQ4MjU4MDVkYzczOTAyZDBmOWIwNzBhYzhmODA0YjQ2MWNmMDkwNzgKGwj3jPDJhvSzAxDssZqrBhjvMSAMOAZA9AdIBBoCaGwiIDI2NWQ5ZGNmNDY3MzYwNTE5NWJhZjhjMWVkN2Q5MTVh; ssid_ucp_v1=1.0.0-KGQ4MjU4MDVkYzczOTAyZDBmOWIwNzBhYzhmODA0YjQ2MWNmMDkwNzgKGwj3jPDJhvSzAxDssZqrBhjvMSAMOAZA9AdIBBoCaGwiIDI2NWQ5ZGNmNDY3MzYwNTE5NWJhZjhjMWVkN2Q5MTVh; publish_badge_show_info=%221%2C0%2C0%2C1701222643321%22; pwa2=%220%7C0%7C3%7C0%22; SEARCH_RESULT_LIST_TYPE=%22single%22; my_rd=2; store-region=cn-hb; store-region-src=uid; FOLLOW_RED_POINT_INFO=%221%22; download_guide=%223%2F20231129%2F1%22; csrf_session_id=c0d80cc111bf0a3c4163226ce66b56b1; strategyABtestKey=%221701392864.026%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.137%7D; FRIEND_NUMBER_RED_POINT_INFO=%22MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2%2F1701446400000%2F1701393039841%2F0%2F0%22; EnhanceDownloadGuide=%221_1701395870_1_1701267105_1_1701328463%22; __ac_nonce=0656986d900b68f1dedd7; __ac_signature=_02B4Z6wo00f01V0-JUgAAIDAqEHP1WMKXOFdHiHAADIpmNdtjJlN5tPpZ27AHzZtgO7h4Mp8d.mInC5.JfcHKI1REokUbsEXPebeiIt66xq-zWk30TcODvlhFEG8HUHBXOVB2ENj1-L9zNol7a; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2%2F1701446400000%2F0%2F0%2F1701415997101%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; passport_fe_beating_status=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A1067%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A200%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2%2F1701446400000%2F0%2F1701416320430%2F0%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS0tQQXpldEVkZGdGZXRwUzhkRUtONlVRb2JHelh5Q0xpdElTSUcvNkNsYmpwdTRDaGM1bUxUdEU2SkZtSERoZ1IzSkpGQmp3TGo4QUhScEVoa0V5dTQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; msToken=EfN0dC_mfSOzxIkZ1j9jBbPqgzPTXQ1C2guEVPvZf0IeZOGYRalwRkPo9LxLLaqoUrJ-RFp0aMZWb5TJ0SX2kr7tlAAQQCjdvYm-8xqZqYo1_SkOtlrp3qxJpP1R; msToken=5jK6fGbQUGVWTx2A2qpIqS80r857p-WCzEU_MRxUOIy6pNPCcTJADK9iONxmd8kofz58QF7xC1SjxGbkFyYAHYePrKqlQMVPf5QYf-ZFMuLlOOIn8bpdfCzK_yEH; odin_tt=e5c1e52f49c063d0b78368e94f893dcf5d2856f62a135044b484c5d41d570d4196a35284b6b822341c3028479ad176ca49bfeef13ec527133ee4d7bd2f64be92; IsDouyinActive=false; tt_scid=DUEiZ-Kc65Z7rKx4dp-Wv0V4kwKRBb7EZCmNjGc14Ii8yxlzkO4qEggVHW7IAWWP9087',
    'Sec-Ch-Ua':'"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User=agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'

}

data = {
    
}

# url = 'https://m.douyin.com/share/user/MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2?showTab=favorite_collection'
# url = 'https://www.douyin.com/user/MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2?showTab=favorite_collection'
url = 'https://www.douyin.com/video/7300081063383158068'
# url = 'https://www.douyin.com/user/MS4wLjABAAAA8OWpsnPTnk8P7u_2_cPgl-vExjZ-IXaFyAR1BpbjZjg?vid=7306115162312903973' #努力的啊桐 respose444
# url = 'https://www.douyin.com/user/MS4wLjABAAAApKwDi1yiBXlcNrsZtUILmCJdvWR47OoFXu8zb0v-2iU?vid=7218502285100404005'#妙卡    respose444


rep = session.get(url, headers = headers)
print(rep)
bs = BeautifulSoup(rep.text, 'html.parser')
title = bs.find('p', class_ = 'title')
print(title)
# aweme_list = rep.json().get('aweme_list')


# print(html)
# print(html.text) #访问自己的是200，其他的是444，可能是因为data的原因

#class="EZC0YBrG Nfs9sicY"
#class="Eie04v01 _Vm86aQ7 PISbKxf7"
#class="B3AsdZT9 chmb2GX8 DiMJX01_"
#视频是https://www.douyin.com/video/*******；图文是https://www.douyin.com/note/*******。


# html_data = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', html.text, re.S)[0]

# html_data = eval(parse.unquote(html_data))
