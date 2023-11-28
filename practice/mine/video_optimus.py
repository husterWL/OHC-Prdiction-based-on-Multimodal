'''
思路：
1.借用cookie和user-agent来访问页面中的class="EZC0YBrG Nfs9sicY"部分
2.然后在从列表中获取每一个视频的href
3.访问每一个href，然后从网页中提取视频地址，之后下载存储即可


抑或是找出界限之前的所有视频的url，放置到列表中
再访问列表进行下载
'''
import requests
import re
import urllib
# for page in range(26, 29):
#     print(f'====================================正在采集第{page}页数据内容====================================')
#     url = f'https://minivideo/getMiniVideoList.php?act=recommend&page={page}&pagesize=25'
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
#     }
#     response = requests.get(url=url, headers=headers)

#抖音是js动态加载的，需要解密参数signature
headers = {
    'cookie':'douyin.com; passport_csrf_token=82d44bc7a0df2af342965704c89b0f8a; passport_csrf_token_default=82d44bc7a0df2af342965704c89b0f8a; s_v_web_id=verify_lo85xd1a_ZdmgAS8W_23MT_4wd5_8Nsg_otHX889YBUSt; xgplayer_user_id=840928142841; n_mh=MwAHPg-ldy5vjDZa2m-0Uz32UYqHWuYijCFkNHJW2Oo; LOGIN_STATUS=1; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; store-region=cn-hb; store-region-src=uid; d_ticket=f1ffec9134f30eac21217990ae8dc8bfbfd39; my_rd=2; sso_uid_tt=fa51cc305c1281308b55116195f04434; sso_uid_tt_ss=fa51cc305c1281308b55116195f04434; toutiao_sso_user=5375fa95148d4d6764f3eb9f3d7513c4; toutiao_sso_user_ss=5375fa95148d4d6764f3eb9f3d7513c4; sid_ucp_sso_v1=1.0.0-KGY4ODhiYzk0NDE1MTZhMjU0YTlhMWVlYTRmNzkyYjNmYjAxN2RmZjgKHwj3jPDJhvSzAxDTsryqBhjvMSAMMIanmvgFOAZA9AcaAmxxIiA1Mzc1ZmE5NTE0OGQ0ZDY3NjRmM2ViOWYzZDc1MTNjNA; ssid_ucp_sso_v1=1.0.0-KGY4ODhiYzk0NDE1MTZhMjU0YTlhMWVlYTRmNzkyYjNmYjAxN2RmZjgKHwj3jPDJhvSzAxDTsryqBhjvMSAMMIanmvgFOAZA9AcaAmxxIiA1Mzc1ZmE5NTE0OGQ0ZDY3NjRmM2ViOWYzZDc1MTNjNA; passport_assist_user=CkEbni14eORJlfm78F7rcIHxsSX1IuWes280tpgMR9ReGSXUHXyS9_2kgbMNhQ0vajUh43Tg4zjTEogsxzjbRmqobRpKCjziXcVrIbF-szFFAz1U8j79Q5VR89xhrRxeq-5kp0h2e41WjE0K4ZaDga2rsJiiZx_b8V5CJo19WFNJf_sQ_f7ADRiJr9ZUIAEiAQNMgkkR; passport_auth_status=811f4a30090ced0c64de180b4bea3db4%2C9e5bc8a3c8b1297147e26f08969447d3; passport_auth_status_ss=811f4a30090ced0c64de180b4bea3db4%2C9e5bc8a3c8b1297147e26f08969447d3; uid_tt=db58092f8f523fbd0fcf89cad008c3bd; uid_tt_ss=db58092f8f523fbd0fcf89cad008c3bd; sid_tt=b4a261a06c2af0bdad369a054c37f0cd; sessionid=b4a261a06c2af0bdad369a054c37f0cd; sessionid_ss=b4a261a06c2af0bdad369a054c37f0cd; _bd_ticket_crypt_cookie=fa747602674b2c90911105018f120cea; sid_guard=b4a261a06c2af0bdad369a054c37f0cd%7C1699682650%7C5183996%7CWed%2C+10-Jan-2024+06%3A04%3A06+GMT; sid_ucp_v1=1.0.0-KGE0YTc0M2EyYmJkMWE4YzRjZDAwMTg5NTYxMGI5M2UxMDExZDNiZDgKGwj3jPDJhvSzAxDasryqBhjvMSAMOAZA9AdIBBoCbGYiIGI0YTI2MWEwNmMyYWYwYmRhZDM2OWEwNTRjMzdmMGNk; ssid_ucp_v1=1.0.0-KGE0YTc0M2EyYmJkMWE4YzRjZDAwMTg5NTYxMGI5M2UxMDExZDNiZDgKGwj3jPDJhvSzAxDasryqBhjvMSAMOAZA9AdIBBoCbGYiIGI0YTI2MWEwNmMyYWYwYmRhZDM2OWEwNTRjMzdmMGNk; ttwid=1%7C-kyomimA1kz0NwFLEnDPi8pG0DDtuP9Fl5Vk9Oye3vI%7C1700316333%7Cd9aa8965f164152063aea9d5fbaa78825222e6684adfa6e1d9995a5f0990568b; bd_ticket_guard_client_web_domain=2; odin_tt=92593bd0e86435e60eb22ee6bce297beeb9ac8dc6f989d372fa259760a3f17d34fe0c09abfe006e26025d09ab513aa81940cc009f9e7e6cdb5012c7f18e72940; dy_swidth=1707; dy_sheight=1067; SEARCH_RESULT_LIST_TYPE=%22single%22; pwa2=%220%7C0%7C3%7C0%22; download_guide=%223%2F20231123%2F1%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1701656499370%2C%22type%22%3A1%7D; douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; csrf_session_id=c0d80cc111bf0a3c4163226ce66b56b1; strategyABtestKey=%221701150470.09%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.236%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; publish_badge_show_info=%221%2C0%2C0%2C1701150474946%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A1067%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; passport_fe_beating_status=true; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2%2F1701187200000%2F0%2F0%2F1701154987001%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2%2F1701187200000%2F0%2F0%2F1701155587002%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS0tQQXpldEVkZGdGZXRwUzhkRUtONlVRb2JHelh5Q0xpdElTSUcvNkNsYmpwdTRDaGM1bUxUdEU2SkZtSERoZ1IzSkpGQmp3TGo4QUhScEVoa0V5dTQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; msToken=Y8hSz111nrlfQ_zRRGWdwzbh5UToIB0bTQGQ-P5oRPyoNKrBmu7bl7aRiBU4ruYUMxqZ0Gxaymj0TNg1cMC7LHrLmyWaJ7ncTPBpGP0iBOOZNxC9OrOhROr8iiA5; tt_scid=Te2NX4lO5xqu8LXiGIN5XHxM2eY1eRpCo48R57QhAYOzec0IGqJYXT43i9J48Wzmd3a0; msToken=_pRMdjJeCdbWxAaohve44LeZOPtVIBn8JzbVWSxCN6_s2DpzNVkB7Y4Bce8fKX_x327TDlibZ_ov9SwMZOdIKL8QX1a6mqpIqx6qIXYhHOUIoeeWlAo3XRhSsER-; IsDouyinActive=false; __ac_nonce=065658eb7004d3bb32ffb; __ac_signature=_02B4Z6wo00f01VMuYDwAAIDAplGKoSof0NlTDmSAADGxDoFwPdHh-siRQdOOyK53iZXoA1TlncUQ9Uqdz9wDHAp5RngWQMKAFEkNyF4mUJR3Qv2XZntOfHY.beTTCACsPA8Q1Zbch5ssvJSJ8a; __ac_referer=__ac_blank',
    'user=agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
}

data = {
    "sec_uid": "MS4wLjABAAAAlwXCzzm7SmBfdZAsqQ_wVVUbpTvUSX1WC_x8HAjMa3gLb88-MwKL7s4OqlYntX4r",
    "count": "21",
    "max_cursor": "1111111111",
    "aid": "1128",
    "_signature": "1rexVRAciIE-bZMoZ46qv9a3sU",
    "dytk": "96ad80961288263ad9d1cff2895d0636"
}



url = "https://m.douyin.com/share/user/MS4wLjABAAAAztmNcl6IuIaPLfdjJX73RKTy2X--P8GKi0z87YlP9hnpjlLrZrO3ZmRkpW74AdR2"
# url = 'https://www.douyin.com/user/MS4wLjABAAAA8OWpsnPTnk8P7u_2_cPgl-vExjZ-IXaFyAR1BpbjZjg?vid=7306115162312903973' #努力的啊桐 respose444
# url = 'https://www.douyin.com/user/MS4wLjABAAAApKwDi1yiBXlcNrsZtUILmCJdvWR47OoFXu8zb0v-2iU?vid=7218502285100404005'#妙卡    respose444
req=urllib.request.Request(url)
resp=urllib.request.urlopen(req)
data=resp.read().decode('utf-8')
print(data) #还是会有jsvmprt=function

html = requests.get(url, headers = headers)
print(html) #访问自己的是200，其他的是444，可能是因为data的原因