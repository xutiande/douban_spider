# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


# 中间件添加cookie，每次访问网页都会携带cookie
def get_cookies_dict():
    cookies_str='zhishiTopicRequestTime=1681480304462; BAIKE_SHITONG=%7B%22data%22%3A%223b107bba97296d64b493c68c92f7843316d6b84db1d2744f80033c62171773004b8a2290378db5e609c65121c9a9bc1630a3cab0c8edcc1b733247ed382079ae6ccff174ccc2ef1048114549f1a6662f975fb7c5f8284a512f38fc4e562f772e%22%2C%22key_id%22%3A%2210%22%2C%22sign%22%3A%2256c4801e%22%7D; BIDUPSID=0FDF12572DCB13B343E18A4F9154C948; PSTM=1657867787; BAIDUID=6CEE2BA83ECA4C9F0B7FD414511D32AE:FG=1; BDUSS_BFESS=X5BZm4wS1hxa3lCVGZJdmNsLVRieHlNcWx4cX5JSHNWdVBlVm5BUk5DemVCaVJqSUFBQUFBJCQAAAAAAAAAAAEAAABZpZNmAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN55~GLeefxid; channel=baidusearch; BAIDUID_BFESS=6CEE2BA83ECA4C9F0B7FD414511D32AE:FG=1; BA_HECTOR=8k0h012h05a5alah0la020c21i3gea61m; ZFY=VWeHT:BaEaJ0fTrOl0dlPbJaOIY0ovTv9:A981UVGuoxE:C; BDRCVFR[6Nn-yyPn7_s]=mk3SLVN4HKm; delPer=0; PSINO=7; H_PS_PSSID=26350; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; X_ST_FLOW=0; baikeVisitId=6ed168ed-106c-418d-9c90-c39e8523985a; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1681480291; __bid_n=186b208540ef12c67e4207; FPTOKEN=tfSfXgOZuh+BxZl0B4o6uobz618QqJe1USRrQhsvOaX7Rry6TrAHbeBcjoS2En0g9jDWVGNDgUlDmiQSw5t5dVmEBOyiY2tbZtrZNwXpxH2bqghhqZep80arKPScrY8TdjCmen3/5ilIY8mKpz7/nYe3juTgVTkPG9AuMn4KcQEM8KCgG068NdEnMeo4WkxXuxPefOFrk7vx+W2VwxCict2HFOBCrlesCyGQueM/K/lIxvCxOG8esUhzxbcpig2iH09+BJOD5zB6IldAn+dtMEycxzTFB1mxe53i+O6GUm7iNx2QEKLoORIINQp8ABbGyPq6Kw0QMcpR6hxzoBSF1tvcaN+i0QECDiv+k/E8ceXtOWWxgAtz1CstiFm5B8jmMEWUqZ9Pnl30opkcvEbxfg==|hvZ/yZM815KxU2HRRBPf/XSABMRa4oJejqZ5VuikE3U=|10|80658257e7e546478379e6924502d8b0; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E9%9D%92%E4%BA%91%E5%BF%97%22%2C%22%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F.*%3F%22%2C%22%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F.*%EF%BC%9F%22%5D%7D; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1681480304; ab_sr=1.0.1_ZmQxMWVjM2E4NjBiZjRjMjJkZjQ1OTU1MGE4MGQzN2NiOWVhMjNjZGUwNTU0ZDdlODA5NDM4ZWJjZjRlNTg5MTczNmE2OTBkMTkzYTNkZDliNDkzZmRhYzE5Y2JkYmZlYzA4MWJjYzJhMDMwY2Q0NmI1MmU1MmUzYTVlZGNkZjg4OWRjY2U2MDMzNWZiN2NkYmNhODE1N2U3N2Q2ZjExMDc2NjQ1YWUzNjE3NDBlYmRmZWVhZmY0YTY0Y2RhNTVj; RT="z=1&dm=baidu.com&si=b9d9a8db-5098-434d-9281-3af01616d23d&ss=lggly7a0&sl=7&tt=68s&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1jc4&nu=kpaxjfo&cl=1rgw&ul=252v"'

    cookies_dict = {}
    for item in cookies_str.split(';'):
        key, value = item.split('=', maxsplit=1)
        cookies_dict[key] = value
    return cookies_dict


COOKIES_DICT = get_cookies_dict()


class DoubanSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.cookies = COOKIES_DICT      #拦截请求，给请求添加cookies信息
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
