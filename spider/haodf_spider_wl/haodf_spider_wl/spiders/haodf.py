import scrapy


class HaodfSpider(scrapy.Spider):
    name = "haodf"
    allowed_domains = ["www.haodf.com"]
    start_urls = ["https://www.haodf.com"]

    def parse(self, response):
        pass
