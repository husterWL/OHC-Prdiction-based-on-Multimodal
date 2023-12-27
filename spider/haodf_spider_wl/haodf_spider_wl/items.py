# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#项目的目标文件，即爬取目标

import scrapy


class HaodfSpiderWlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    #主键
    doctorID = scrapy.Field()

    name = scrapy.Field()
    
    #