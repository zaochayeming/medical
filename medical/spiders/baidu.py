import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baike.baidu.com/item/急性阑尾炎']

    def parse(self, response):
        print(response.status)
        # 疾病名称
        name = response.xpath('//h1/text()').extract_first()
        # 疾病简介
        summary = response.xpath('//div[@class="lemma-summary"]/div//text()').extract()
        summary = ''.join(summary)
        # 疾病英文名称
        english_name = response.xpath('//div[@class="dl-baseinfo"]/dl/dd/text()').extract()[0].replace('\n', '')
        # 就诊科室
        department = response.xpath('//div[@class="dl-baseinfo"]/dl/dd/text()').extract()[1].replace('\n', '')
        # 常见原因
        common_causes = response.xpath('//div[@class="dl-baseinfo"]/dl/dd/text()').extract()[2].replace('\n', '')
        # 常见症状
        common_symptom = response.xpath('//div[@class="dl-baseinfo"]/dl/dd/text()').extract()[2].replace('\n', '')

        title = response.xpath('//h2[@class="title-text"]/text()').extract()

        print(title)
        pass
