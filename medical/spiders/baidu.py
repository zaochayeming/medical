import scrapy
from scrapy import Item, Field
from scrapy.loader import ItemLoader

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baike.baidu.com/item/急性阑尾炎']

    def parse(self, response):
        print(response.status)

        item = Item()
        item_l = ItemLoader(item=item)

        # 疾病名称
        name = response.xpath('//h1/text()').extract_first()
        item.fields['疾病名称'] = Field()
        item_l.add_value('疾病名称', name)

        # 疾病简介
        summary = response.xpath('//div[@class="lemma-summary"]/div//text()').extract()
        summary = ''.join(summary)
        item.fields['疾病简介'] = Field()
        item_l.add_value('疾病简介', summary)

        # 基本信息
        basic_key = response.xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]/dl/dt/text()').extract()
        basic_value = response.xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]/dl/dd/text()').extract()
        basic_information = dict(zip(basic_key,basic_value))
        for item in basic_information.items():
            key = item[0]
            value = item[1].replace('\n','')
            print(key)
            print(value)
            # item.fields[key] = Field()
            # item_l.add_value(key, value)


        # print(item_l.load_item())


        # # 疾病英文名称
        # english_name = response.xpath('//div[@class="dl-baseinfo"]/dl/dd/text()').extract()[0].replace('\n', '')
        # # 就诊科室
        # department = response.xpath('//div[@class="dl-baseinfo"]/dl/dd/text()').extract()[1].replace('\n', '')
        # # 常见原因
        # common_causes = response.xpath('//div[@class="dl-baseinfo"]/dl/dd/text()').extract()[2].replace('\n', '')
        # # 常见症状
        # common_symptom = response.xpath('//div[@class="dl-baseinfo"]/dl/dd/text()').extract()[2].replace('\n', '')
        #
        # title = response.xpath('//h2[@class="title-text"]/text()').extract()
        # print(title)

        return item_l.load_item()
