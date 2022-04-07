from scrapy import cmdline

# 运行爬虫
cmdline.execute(['scrapy', 'crawl', 'baidu'])

# 导出成csv文件
# cmdline.execute(['scrapy', 'crawl', 'baidu', '-o', 'result.csv'])

# 导出json文件
# cmdline.execute(['scrapy', 'crawl', 'baidu', '-o', 'result.json'])