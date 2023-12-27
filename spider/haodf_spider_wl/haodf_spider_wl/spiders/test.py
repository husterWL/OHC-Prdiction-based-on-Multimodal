import scrapy
from haodf_spider_wl.items import HaodfSpiderWlItem

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['mms.tjmu.edu.cn']
    start_urls = ['http://mms.tjmu.edu.cn/szll1/jsml1/xxglx.htm']

    #解析的方法，每个初始URL完成下载后将被调用，调用的时候传入从每一个URL传回的Response对象来作为唯一参数
    def parse(self, response):
        # filename = 'ygyxinguanlaoshi.html'
        # open(filename, 'w', encoding = 'UTF-8').write(response.text)
        context = response.xpath('/html/head/title/text()')
        title = context.extract_first()   #extract()返回列表，extract_first()返回字符串
        print(title)
        # print(type(title))
        items = []
        print(response.xpath('/html/body/div[5]/div/div[2]//div/div/ul/li/a//p/text()'))
        for i in response.xpath('/html/body/div[5]/div/div[2]//div/div/ul/li/a//p/text()').extract():   #不使用extract()函数，会导致提取的姓名只有第一个字
            pass
            item = HaodfSpiderWlItem()
            # name = i.extract()    #返回的是列表
            
            item['name'] = i
            # response.urljoin()
            items.append(item)
        print(items)
        return items
    #打印医管信息管理系老师的姓名