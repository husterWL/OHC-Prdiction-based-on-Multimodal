import scrapy
from scrapy import Request
import re
import json

#例子：使用yield求斐波那契数列
# def fab(max): 
#     n, a, b = 0, 0, 1 
#     while n < max: 
#         yield b      # 使用 yield
#         # print b 
#         a, b = b, a + b 
#         n = n + 1
 
# for n in fab(5): 
#     print(n)

class HaodfSpider(scrapy.Spider):
    name = "haodf"
    allowed_domains = ["www.haodf.com"]
    start_urls = ["https://www.haodf.com"]

    def parse(self, response):
        pass
        yield scrapy.Request()
        # response.follow()
        