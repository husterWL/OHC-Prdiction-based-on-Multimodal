import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['mms.tjmu.edu.cn']
    start_urls = ['http://mms.tjmu.edu.cn/szll1/jsml1/xxglx.htm']

    #解析的方法，每个初始URL完成下载后将被调用，调用的时候传入从每一个URL传回的Response对象来作为唯一参数
    def parse(self, response):
        filename = 'ygyxinguanlaoshi.html'
        open(filename, 'w', encoding = 'UTF-8').write(response.text)