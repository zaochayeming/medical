import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baike.baidu.com/item/急性阑尾炎']

    def parse(self, response):
        print(response.content)
        pass
