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
        basic_value = response.xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]/dl/dd/text()').extract()
        for i in range(len(basic_key)):
            item.fields[basic_key[i]] = Field()
            item_l.add_value(basic_key[i], basic_value[i].replace('\n', ''))

        # 其他详细信息
        detail_content = response.xpath(
            '//div[@class="main_tab main_tab-defaultTab  curTab"]/div[@class="para-title level-2  J-chapter" or @class="para"]')  # 其他详情信息的xpath
        index = []
        for i in detail_content:
            detail_key = i.xpath('./h2/text()').extract()  # 数组——详情信息内容标题
            if len(detail_key) != 0:
                x = detail_content.index(i)
                index.append(x)
        print(index)
        for i in range(0, len(index)-1):
            start_index = index[i]
            end_index = index[i + 1]
            detail_key = detail_content[start_index].xpath('./h2/text()').extract_first()
            item.fields[detail_key] = Field()

            detail_value = ''
            detail_value_xpath = detail_content[start_index+1:end_index]
            for i in detail_value_xpath:
                tem = i.xpath('./b/text()').extract()
                if len(tem) > 0:
                    detail_value_title = i.xpath('./b//text()').extract()
                    detail_value += ''.join(detail_value_title)
                    detail_value += '\n'
                else:
                    detail_value_content = i.xpath('.//text()').extract()
                    detail_value += ''.join(detail_value_content)
                    detail_value += '\n'
                # print(detail_value_title)
            print(detail_key)
            print(detail_value_xpath)
            item_l.add_value(detail_key, detail_value)

            # print(i)
            # print(k, v)
            # value = detail_content[1:6]
            # print(value)

        # item.fields[key] = Field()  # 将详情信息的标题放入key中

        # print(len(detail_key))
        # detail_value_title = i.xpath('./b//text()').extract()  # 详情信息内容加粗内容
        # detail_value_text = i.xpath('./text()').extract()   # 详情信息内容未加粗的内容
        # if len(detail_key) != 0:
        #     key = detail_key[0]  # 字符串——详情信息内容标题
        #     item.fields[key] = Field()  # 将详情信息的标题放入key中
        #     print(key)

        #     if len(detail_value) > 0:
        #         item_l.add_value(key, detail_value)
        #         detail_value = ''
        # elif len(detail_value_title) > 0:
        #     detail_value += ''.join(detail_value_title) + '\n'
        #     # if len(detail_value_text) > 0:
        #     #     detail_value += ''.join(detail_value_text)
        #     print(detail_value)
        #
        # elif len(detail_value_text) > 0:
        #     detail_value += ''.join(detail_value_text)
        #
        # else:
        #     item_l.add_value(key, detail_value)
        #     print('结束')
        # print(detail_value_text)

        print(item_l.load_item())

        return item_l.load_item()
