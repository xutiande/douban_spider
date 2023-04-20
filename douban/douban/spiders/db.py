import re

import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
from douban.items import DoubanItem
from scrapy import Request


class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        for i in range(1):
            yield Request('https://movie.douban.com/top250?start={}&filter='.format(i * 25))

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        get_div = sel.xpath('//*[@id="content"]/div/div[1]/ol/li')
        i = 0
        for list_item in get_div:
            i += 1
            # 二级页面
            info_two = list_item.xpath(
                f'//*[@id="content"]/div/div[1]/ol/li[{i}]/div/div[2]/div[1]/a/@href').extract_first()
            douban_movie = DoubanItem()
            title = list_item.xpath(
                f'//*[@id="content"]/div/div[1]/ol/li[{i}]/div/div[2]/div[1]/a/span[1]/text()').extract_first()
            douban_movie['title'] = re.sub(r'[^\w\s]', '', title).replace('\n', '').replace(' ', '').replace(' ', '')
            time = list_item.xpath(
                f'//*[@id="content"]/div/div[1]/ol/li[{i}]/div/div[2]/div[2]/p[1]/text()[2]').extract_first()
            douban_movie['time'] = re.sub(r'[^\w\s]', '', time).replace('\n', '').replace(' ', '').replace(' ', '')[0:4]
            try:
                comments = list_item.xpath(
                    f'//*[@id="content"]/div/div[1]/ol/li[{i}]/div/div[2]/div[2]/p[2]/span/text()').extract_first()
                print(comments)
                douban_movie['comments'] = re.sub(r'[^\w\s]', '', comments)
            except Exception as e:
                print("程序错误为:", e)
                douban_movie['comments'] = re.sub(r'[^\w\s]', '', '无电影介绍信息')
            yield Request(
                url=info_two, callback=self.parse_info_two, cb_kwargs={'item': douban_movie}
                # 回调函数callback，cb_kwargs往函数传递参数
            )

    def parse_info_two(self, response, **kwargs):

        douban_movie = kwargs['item']
        sel = Selector(response)
        two_title = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract_first()
        two_introduce = sel.css('span[property="v:summary"]::text').extract_first().replace('\n','').replace(' ','')
        douban_movie['two_title'] = two_title
        douban_movie['two_introduce'] = two_introduce
        yield douban_movie
        a = 1
