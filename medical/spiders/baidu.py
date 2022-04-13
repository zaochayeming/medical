import scrapy
from scrapy import Item, Field
from scrapy.loader import ItemLoader


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = [
                  'http://baike.baidu.com/item/急性阑尾炎',
                  'http://baike.baidu.com/item/细菌性肺炎',
                  'http://baike.baidu.com/item/慢性阻塞性肺疾病',
                  'http://baike.baidu.com/item/肾衰竭/4427798#2',
                  'http://baike.baidu.com/item/高血压/195863',
                  'http://baike.baidu.com/item/腰椎间盘突出症/2996107',
                  'http://baike.baidu.com/item/急性心肌梗死',
                  'http://baike.baidu.com/item/急性白血病',
                  'http://baike.baidu.com/item/充血性心力衰竭',
                  'http://baike.baidu.com/item/消化道出血/1509#viewPageContent',
                  'http://baike.baidu.com/item/结节性甲状腺肿',
                  'http://baike.baidu.com/item/前列腺增生',
                  'http://baike.baidu.com/item/急性胰腺炎',
                  'http://baike.baidu.com/item/再生障碍性贫血',
                  'http://baike.baidu.com/item/急性上消化道出血',
                  'http://baike.baidu.com/item/急性胆囊炎',
                  'http://baike.baidu.com/item/肺结核',
                  'http://baike.baidu.com/item/病毒性肝炎/344481',
                  'http://baike.baidu.com/item/老年性白内障',
                  'http://baike.baidu.com/item/甲状腺功能亢进症',
                  'http://baike.baidu.com/item/心力衰竭/1373927',
                  'http://baike.baidu.com/item/心房颤动',
                  'http://baike.baidu.com/item/短暂性脑缺血发作',
                  'http://baike.baidu.com/item/短暂性脑缺血发作',
                  'http://baike.baidu.com/item/脑出血',
                  'http://baike.baidu.com/item/脑膜瘤',
                  'http://baike.baidu.com/item/神经胶质瘤',
                  'http://baike.baidu.com/item/垂体腺瘤',
                  'http://baike.baidu.com/item/支气管哮喘/661#viewPageContent',
                  # 'http://baike.baidu.com/item/原发性肾病综合征',
                  # 'http://baike.baidu.com/item/脑梗死',  # 内容太多
                  ]

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
        basic_value = response.xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]/dl/dd//text()').extract()
        basic_value = ''.join(basic_value).split('\n\n')
        for i in range(len(basic_key)):
            key = basic_key[i].replace('所属科室', '就诊科室')
            value = basic_value[i].replace('\n', '')
            item.fields[key] = Field()
            item_l.add_value(key, value)

        # 其他详细信息
        detail_content = response.xpath(
            '//div[@class="content"]/div[1]/div[@class="para-title level-2  J-chapter" or @class="para" or @class="para-title level-3  "]')  # 其他详情信息的xpath
        if len(detail_content) == 0:
            detail_content = response.xpath(
                '//div[@class="main_tab main_tab-defaultTab  curTab"]/div[@class="para-title level-2  J-chapter" or @class="para" or @class="para-title level-3  "]')  # 其他详情信息的xpath
        index = []
        # print(detail_content)
        for i in detail_content:
            # print(i, 1)
            detail_key = i.xpath('./h2/text()').extract()  # 数组——详情信息内容标题
            if len(detail_key) != 0:
                x = detail_content.index(i)
                index.append(x)
        # print(index)
        for i in range(0, len(index)-1):
            start_index = index[i]
            end_index = index[i + 1]
            detail_key = detail_content[start_index].xpath('./h2/text()').extract_first()
            detail_key = detail_key.replace('疾病', '')\
                                    .replace('常见', '')\
                                    .replace('诊断及鉴别诊断', '诊断')\
                                    .replace('实验室', '')\
                                    .replace('临床分型及病理', '分类')\
                                    .replace('病因及常见疾病', '病因')\
                                    .replace('病理生理', '分类')\
                                    .replace('发病原因', '病因')
            # print(detail_key)
            item.fields[detail_key] = Field()

            detail_value = ''
            detail_value_xpath = detail_content[start_index+1:end_index]
            for i in detail_value_xpath:
                h3 = i.xpath('./h3/text()').extract()
                tem = i.xpath('./b/text()').extract()
                if len(tem) > 0:
                    detail_value_title = i.xpath('./b//text()').extract()
                    detail_value += ''.join(detail_value_title)
                    detail_value += '\n'
                elif len(h3) > 0:
                    detail_value += ''.join(h3)
                    detail_value += '\n'
                else:
                    detail_value_content = i.xpath('.//text()').extract()
                    detail_value += ''.join(detail_value_content)
                    detail_value += '\n'
                # print(detail_value_title)
            # print(detail_key)
            # print(detail_value_xpath)
            item_l.add_value(detail_key, detail_value)


        # print(item_l.load_item())

        return item_l.load_item()
