
from selenium import webdriver
import time,random
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
import os


class YIXL():

    def __init__(self):
        # 初始化程序
        options = webdriver.ChromeOptions()
        # 去掉开发者警告，避免被反爬
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
        # 浏览器初始化
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        time.sleep(5)

    def base(self):

        self.browser.get('https://www.xinli001.com/qa?page=1&type=answer&object_name=answer&title=&level2_tag=0&sort=id&from=houye-dh')

        # 设置等待使完全加载
        wait = WebDriverWait(self.browser, 100)

    def question_spider(self):
        #self.browser.get('https://www.xinli001.com/qa?page=1&type=answer&ob
        # ject_name=answer&title=&level2_tag=0&sort=id&from=houye-dh')
        self.drop_down()
        li = self.browser.find_elements(By.CLASS_NAME,"undeblock")
        data = []
        for j in li:
            title = j.find_element(By.XPATH, './/div[@class="title"]/p/a')
            author = j.find_element(By.XPATH, './/a/span[@class="username"]')
            answer = j.find_element(By.XPATH, './/div[@class="ellipsis-container"]/div')
            score = j.find_element(By.XPATH, './/span[@class="answer_zan span"]/a/font')
            texts = ''
            items = {
                "标题":title.text,
                "作者": author.text,
                "回答": answer.text,
                "得分":score.text,
            }
            print(items)
            data.append(items)
        with open('question_data.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for item in data:
                writer.writerow([item["标题"], item["作者"], item["回答"], item["得分"]])
        #print(data)
        self.page_next()
        self.browser.quit()

    def reply_spider(self):
        data = []
        for i in range(463, 501):  # range(1, 11)  就是从1到10
            url1 = 'https://www.xinli001.com/qa?page={}&type=question&object_name=question&title=&level2_tag=0&sort=id&from=houye-dh'.format(i)
            self.browser.get(url1)
            time.sleep(2)
            src = self.browser.find_elements(By.XPATH, './/p[@class="title"]/span/a')
            url_list = []
            for i in src:
                url = i.get_attribute('href')
                url_list.append(url)
            # print(url_list)
            au_name = ''
            for h in url_list:
                self.browser.get(url=h)
                time.sleep(random.randint(1500, 2000) / 1000)
                n = self.browser.find_element(By.XPATH, './/*[@id="left"]//div[@class="title"]/a')
                n_url = n.get_attribute('href')
                # print(n_url)
                if n_url == 'javascript:void(0);':
                    au_name = '匿名'
                else:
                    time.sleep(random.randint(5000, 10000) / 1000)
                    self.browser.get(url=n_url)
                    try:
                        a_name1 = self.browser.find_element(By.XPATH, './/li[@class="fs16"]')
                        au_name = a_name1.text
                    except Exception as e1:
                        try:
                            a_name2 = self.browser.find_element(By.XPATH, './/div[@class="user_name"]')
                            au_name = a_name2.text
                        except Exception as e2:
                            try:
                                a_name3 = self.browser.find_element(By.XPATH, './/h1[@class="name"]')
                                au_name = a_name3.text
                            except Exception as e3:
                                pass
                    # try:
                    #     a_name1 = self.browser.find_element(By.XPATH, './/li[@class="fs16"]')
                    #
                    #     if a_name1:
                    #         au_name = a_name1.text
                    #     else:
                    #         a_name2 = self.browser.find_element(By.XPATH, './/div[@class="user_name"]')
                    #         au_name = a_name2.text
                    # except Exception as e:
                    #     pass
                    time.sleep(random.randint(3000, 6000) / 1000)
                    self.browser.get(url=h)

                while True:
                    time.sleep(random.randint(1800, 3000) / 1000)
                    self.drop_down()
                    ques_title = self.browser.find_element(By.TAG_NAME, 'h1')
                    ques_time = self.browser.find_element(By.XPATH, './/p[@class="read-capacity"]/span[1]')
                    ques_reply = self.browser.find_element(By.XPATH, './/div[@class="title"]/strong')
                    ques_read = self.browser.find_element(By.XPATH, './/span[@class="absoulte-img"]/a')
                    ques_text = self.browser.find_element(By.XPATH, './/div[@class="content"]/p[@class="text"]')
                    li = self.browser.find_elements(By.XPATH, './/ul[@class="content-ans"]/li')
                    text_tag_str = ""
                    try:
                        text_tags = self.browser.find_elements(By.XPATH, './/*[@id="left"]/div[1]/ul/li')
                        if text_tags:
                            text_tag = [content.text for content in text_tags]
                            text_tag_str = ', '.join(text_tag)
                        else:
                            text_tag_str = ""
                    except Exception as e:
                        print(e)
                    for j in li:
                        print()
                        reply_author = j.find_element(By.XPATH, './/p[@class="user"]/a')
                        #reply_help = j.find_element(By.XPATH, './/p/span[@class="help"]')
                        reply_help = ""
                        try:
                            help_num1 = self.browser.find_element(By.XPATH, './/p/span[@class="help"]')
                            if help_num1:
                                reply_help = help_num1.text
                            else:
                                reply_help = ""
                        except Exception as e:
                            pass
                        reply_text = j.find_element(By.XPATH, './/div[@class="text"]')
                        reply_like = j.find_element(By.XPATH, './/span[@class="answer_zan"]/a/font')
                        reply_comment = j.find_element(By.XPATH, './/span[@class="comment_item"]/a/font')
                        reply_time = j.find_element(By.XPATH, './/p[@class="created_time"]')
                        item = {
                            "问题标题": ques_title.text,
                            "问题作者": au_name,
                            "问题时间": ques_time.text,
                            "问题标签": text_tag_str,
                            "阅读数": ques_read.text,
                            "回答数": ques_reply.text,
                            "问题内容": ques_text.text,
                            "回复作者": reply_author.text,
                            "累计帮助": reply_help,
                            "回复内容": reply_text.text,
                            "回复点赞": reply_like.text,
                            "回复评论": reply_comment.text,
                            "回复时间": reply_time.text
                        }
                        print(item)
                        with open('reply_data_all.csv', 'a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow([item["问题标题"], item["问题作者"],item["问题时间"], item["问题标签"], item["阅读数"], item["回答数"], item["问题内容"],
                                            item["回复作者"], item["累计帮助"], item["回复内容"], item["回复点赞"], item["回复评论"], item["回复时间"]])
                    try:  # Try to go to next page on page two
                        next = self.browser.find_element(By.LINK_TEXT, '»')
                        if next:
                            next.click()
                        else:
                            break  # 没有下一页跳出循环
                    except Exception as e:
                        pass
                        break
                    self.browser.delete_all_cookies()
                    time.sleep(random.randint(1500, 2000) / 1000)
        self.browser.quit()

    def qu_spider(self):
        data = []
        for i in range(1, 501):  # range(1, 11)  就是从1到10
            url1 = 'https://www.xinli001.com/qa?page={}&type=question&object_name=last&title=&level2_tag=0&sort=id&from=houye-dh'.format(i)
            self.browser.get(url1)
            time.sleep(2)
            src = self.browser.find_elements(By.XPATH, './/p[@class="title"]/span/a')
            url_list = []
            for i in src:
                url = i.get_attribute('href')
                url_list.append(url)
            # print(url_list)
            au_name = ''
            for h in url_list:
                self.browser.get(url=h)
                time.sleep(random.randint(1500, 2000) / 1000)
                n = self.browser.find_element(By.XPATH, './/*[@id="left"]//div[@class="title"]/a')
                n_url = n.get_attribute('href')
                # print(n_url)
                if n_url == 'javascript:void(0);':
                    au_name = '匿名'
                else:
                    time.sleep(random.randint(5000, 10000) / 1000)
                    self.browser.get(url=n_url)
                    try:
                        a_name1 = self.browser.find_element(By.XPATH, './/li[@class="fs16"]')
                        au_name = a_name1.text
                    except Exception as e1:
                        try:
                            a_name2 = self.browser.find_element(By.XPATH, './/div[@class="user_name"]')
                            au_name = a_name2.text
                        except Exception as e2:
                            pass
                    time.sleep(random.randint(3000, 6000) / 1000)
                    self.browser.get(url=h)

                while True:
                    time.sleep(random.randint(1800, 3000) / 1000)
                    ques_title = self.browser.find_element(By.TAG_NAME, 'h1')
                    ques_time = self.browser.find_element(By.XPATH, './/p[@class="read-capacity"]/span[1]')
                    ques_reply = self.browser.find_element(By.XPATH, './/div[@class="title"]/strong')
                    ques_read = self.browser.find_element(By.XPATH, './/span[@class="absoulte-img"]/a')
                    ques_text = self.browser.find_element(By.XPATH, './/div[@class="content"]/p[@class="text"]')
                    li = self.browser.find_elements(By.XPATH, './/ul[@class="content-ans"]/li')
                    text_tag_str = ""
                    try:
                        text_tags = self.browser.find_elements(By.XPATH, './/*[@id="left"]/div[1]/ul/li')
                        if text_tags:
                            text_tag = [content.text for content in text_tags]
                            text_tag_str = ', '.join(text_tag)
                        else:
                            text_tag_str = ""
                    except Exception as e:
                        print(e)
                    item = {
                            "问题标题": ques_title.text,
                            "问题作者": au_name,
                            "问题时间": ques_time.text,
                            "问题标签": text_tag_str,
                            "阅读数": ques_read.text,
                            "回答数": ques_reply.text,
                            "问题内容": ques_text.text,
                        }
                    print(item)
                    with open('qu_data_new.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                                [item["问题标题"], item["问题作者"], item["问题时间"], item["问题标签"], item["阅读数"], item["回答数"],
                                 item["问题内容"]])
                    time.sleep(random.randint(1500, 2000) / 1000)
                    break

            self.browser.quit()
    def read_spider(self):
        data = []
        for i in range(3, 4):  # 输出前十页的数据
            url1 = 'https://www.xinli001.com/info?page={}'.format(i)
            self.browser.get(url1)
            time.sleep(3)
            src = self.browser.find_elements(By.XPATH, './/div[@class="right"]/a')
            url_list = []
            for i in src:
                url = i.get_attribute('href')
                url_list.append(url)
            #print(url_list)
            for h in url_list:
                self.browser.get(url=h)
                time.sleep(random.randint(3000, 3400) / 1000)
                text_content = ""
                text_content_str = ""
                try:
                    text_contents = self.browser.find_elements(By.XPATH, './/div[@class="second-tag-m"]/a')
                    if text_contents:
                        text_content = [content.text for content in text_contents]
                        text_content_str = ', '.join(text_content)
                    else:
                        text_content_str = ""
                except Exception as e:
                    print(e)
                text_tag = ""
                text_tag_str = ""
                try:
                    text_tags = self.browser.find_elements(By.XPATH, './/div[@class="first-tag-m"]/a')
                    if text_tags:
                        text_tag = [content.text for content in text_tags]
                        text_tag_str = ', '.join(text_tag)
                    else:
                        text_tag_str = ""
                except Exception as e:
                    print(e)
                title = self.browser.find_element(By.XPATH, './/div[@class="title"]')
                like = self.browser.find_element(By.XPATH, './/span[@class="like"]')
                comment = self.browser.find_element(By.XPATH, './/span[@class="comment"]')
                read = self.browser.find_element(By.XPATH, './/span[@class="read"]')
                ti = self.browser.find_element(By.XPATH, '//div[@class="info"]/span[1]')
                items = {
                            "标题": title.text,
                            "词条": text_content_str,
                            "标签": text_tag_str,
                            "点赞数": like.text,
                            "评论数": comment.text,
                            "阅读量": read.text,
                            "时间": ti.text
                        }
                print(items)
                data.append(items)

            time.sleep(random.randint(3000, 3400) / 1000)
        with open('read_data1.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for item in data:
                writer.writerow([item["标题"], item["词条"], item["标签"], item["点赞数"],
                                 item["评论数"], item["阅读量"], item["时间"]])
        self.browser.quit()

    def expert_spider(self):
        data = []
        url1 = 'https://www.xinli001.com/consult?channel_flag=pc_dh'
        self.browser.get(url1)
        time.sleep(random.randint(3000, 3400) / 1000)
        self.drop_down()
        url_list = []
        name_list = []
        price_list = []
        m = 0
        while True:
            name_elements = self.browser.find_elements(By.XPATH, './/li/a[@class="name"]')
            price_elements = self.browser.find_elements(By.XPATH, './/li[@class="price"]')
            for name_element, price_element in zip(name_elements, price_elements):
                url = name_element.get_attribute('href')
                url_list.append(url)
                name_list.append(name_element.text)
                price_list.append(price_element.text)
            # for i in name:有bug时用来监测
            #     url = i.get_attribute('href')
            #     url_list.append(url)
            #     name_list.append(name[i].text)
            #     price_list.append(price[i].text)
            # 连续点击5次下一页，如果都没有返回证明已经到了最后一页
            for _ in range(5):
                try:
                    next = self.browser.find_element(By.XPATH, './/ul[@class="mo-paging"]/li[last()]')
                    if next:
                        next.click()
                        break
                    else:
                        break  # 没有下一页，跳出循环
                except Exception as e:
                    print(e)
                    time.sleep(2)  # 两秒以后再次尝试
            else:
                break  # 如果尝试了5次还是失败，结束函数

            time.sleep(random.randint(3000, 3400) / 1000)
        # print(len(url_list))
        # print(len(name_list))
        # 测试列表长度，检查bug
        for h in url_list:
            time.sleep(random.randint(3000, 3400) / 1000)
            self.browser.get(url=h)
            try:
                exp_price = self.browser.find_element(By.XPATH,
                                                      '//div[@class="yuyue-notice-block"]/div[last()-1]/span[last()]')
            except Exception as e:
                print(e)
                exp_price = ""
            help_num = ""
            try:
                help_num1 = self.browser.find_element(By.XPATH, './/div[@class="info-item"][1]//span')
                if help_num1:
                    help_num = help_num1.text
                else:
                    help_num = ""
            except Exception as e:
                print(e)
            thank_num = ""
            try:
                thank_num1 = self.browser.find_element(By.XPATH, './/div[@class="info-item"][2]//span')
                if thank_num1:
                    thank_num = thank_num1.text
                else:
                    thank_num = ""
            except Exception as e:
                print(e)
            exp_tag = ""
            try:
                exp_tag1 = self.browser.find_element(By.XPATH, './/h1[@class="name"]/span')
                if exp_tag1:
                    exp_tag = exp_tag1.text
                else:
                    exp_tag = ""
            except Exception as e:
                print(e)
            exp_title = ""
            try:
                exp_title1 = self.browser.find_element(By.XPATH, './/div[@class="info"]/p')
                if exp_title1:
                    exp_title = exp_title1.text
                else:
                    exp_title = ""
            except Exception as e:
                print(e)
            location = ""
            try:
                location1 = self.browser.find_element(By.XPATH, './/div/p[@class="location"]')
                if location1:
                    location = location1.text
                else:
                    location = ""
            except Exception as e:
                print(e)
            work_time = ""
            try:
                work_time1 = self.browser.find_element(By.XPATH, './/span[@class="year"]')
                if work_time1:
                    work_time = work_time1.text
                else:
                    work_time = ""
            except Exception as e:
                print(e)
            quality_str = ""
            try:
                quality_s = self.browser.find_elements(By.XPATH, './/*[@id="general-info"]/div[1]//p')
                if quality_s:
                    quality_s = [content.text for content in quality_s]
                    quality_str = ', '.join(quality_s)
                else:
                    quality_str = ""
            except Exception as e:
                print(e)
            essay_num = ""
            try:
                essay_n = self.browser.find_element(By.XPATH, './/div[@class="column-item"][1]//span[@class="num"]')
                if essay_n:
                    essay_num = essay_n.text
                else:
                    essay_num = ""
            except Exception as e:
                print(e)
            answer_num = ""
            try:
                answer_n = self.browser.find_element(By.XPATH, './/div[@class="column-item"][2]//span[@class="num"]')
                if answer_n:
                    answer_num = answer_n.text
                else:
                    answer_num = ""
            except Exception as e:
                print(e)

            items = {
                        "专家姓名": name_list[m],
                        "预约价格": price_list[m],
                        "专家资质": quality_str, # 专家取得的资格认证
                        "专家标签": exp_tag, # 专家名称旁边的词条
                        "专家称号": exp_title, # 专家展示在表中的内容，位置在主页名称下方
                        "帮助人数": help_num, # 专家帮助的人数
                        "感谢人数": thank_num, # 专家收到感谢信的数量
                        "所在地区": location,
                        "工作年数": work_time, # 在资格认证一栏中，有的专家没有
                        "文章数量": essay_num,
                        "回答数量": answer_num
                    }
            m = m+1
            print(items)
            data.append(items)
        with open('expert_datas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for item in data:
                writer.writerow([item["专家姓名"], item["预约价格"], item["专家资质"], item["专家标签"],
                                 item["专家称号"], item["帮助人数"], item["感谢人数"], item["所在地区"],
                                 item["工作年数"], item["文章数量"], item["回答数量"]])
        self.browser.quit()

    def page_next(self):
        try:
            next = self.browser.find_element(By.LINK_TEXT, '»')
            if next:
                next.click()
                self.question_spider()
            else:
                self.browser.close()
        except Exception as e:
            print(e)

    def drop_down(self):
        for x in range(1, 10):
            j = x / 10
            js = f"document.documentElement.scrollTop = document.documentElement.scrollHeight * {j}"
            self.browser.execute_script(js)
            time.sleep(random.randint(400,800)/1000)


if __name__ == '__main__':
    f = YIXL()
    f.base()
    # f.question_spider()
    # f.reply_spider()
    # f.qu_spider()
    f.read_spider()
    # f.expert_spider()
    # 切换函数实现功能
