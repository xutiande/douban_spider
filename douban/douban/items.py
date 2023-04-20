# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    comments = scrapy.Field()
    two_title = scrapy.Field()
    two_introduce = scrapy.Field()
