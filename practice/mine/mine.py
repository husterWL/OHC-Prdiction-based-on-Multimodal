#2023年11月30日
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import lxml
# import re
# import scrapy
# html = urlopen('https://pythonscraping.com/pages/page1.html')
# # print(html.read())
# print('\n')
# '''
# 这段代码是使用Python的urllib库中的urlopen函数打开一个网页，并打印出该网页的内容。
# 但是，这段代码存在一个问题，即在第一次调用html.read()后，文件指针已经移动到了文件的末尾，所以在第二次调用html.read()时，它将返回空字符串。
# 如果你想再次读取网页内容，你需要重新打开文件或者将文件指针重置到文件的开头。
# '''
# # print(html.read())
# bs = BeautifulSoup(html.read(), 'lxml')
# print(bs.h1)
# bs.findAll()
# bs.find_all()
# re.compile()


#2023年12月5日
import requests
def get_cookie(self):
        count = 10
        while count:
            try:
                session = requests.session()
                h = session.get(url, verify=False, allow_redirects=False, timeout=20).headers
                x_vc_bdturing_parameters = h.get('x-vc-bdturing-parameters')
                if not x_vc_bdturing_parameters:
                    count -= 1
                    logger.info(f'提取：x_vc_bdturing_parameters 失败，重试！')
                    time.sleep(random.randint(3, 5))
                    continue
                verify_data = json.loads(base64.b64decode(h.get('x-vc-bdturing-parameters')).decode("utf-8"))
                fp = verify_data.get("fp")
                detail = verify_data.get("detail")
                logger.info(f"成功提取：{fp}, 开始验证")
                try:  # 有几率报错，报错重试
                    msg = Verify().verify(fp, detail)
                    logger.info(msg)
                except Exception as e:
                    logger.info(f"{e}")
                    continue
                if msg.get('code') != 200:
                    logger.info(f"{msg.get('message')}，重试")
                    continue
                logger.info(f"ck s_v_web_id：{fp}, {msg.get('message')}")
                s_v_web_id = f's_v_web_id={verify_data.get("fp")};'
                self.cookie = s_v_web_id
                return
            except Exception as e:
                logger.info(f'提取：x_vc_bdturing_parameters 出错：{e}')
                time.sleep(random.randint(3, 5))
                continue