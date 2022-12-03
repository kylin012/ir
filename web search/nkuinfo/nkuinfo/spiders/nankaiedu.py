# 爬取数据
import scrapy
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from nkuinfo.items import NkuinfoItem
import time

class NankaieduSpider(scrapy.Spider):
    name = 'nankaiedu'
    allowed_domains = ['nankai.edu.cn']
    start_urls = ['http://www.nankai.edu.cn']

    def parse(self, response):
        # 提取域名下的所有链接
        allow_links = LinkExtractor(allow_domains=self.allowed_domains)
        links = allow_links.extract_links(response)
        ts = time.time()
        item = NkuinfoItem(
            # 网站标题
            title=response.xpath('//title/text()').get(''),
            # url地址
            url=response.url,
            # 现在的时间
            date=ts,
            # 网站文字标签，通过换行符分割
            text=BeautifulSoup(response.text, 'lxml').get_text(separator=" ", strip=True),
            # 网站html代码
            restext=response.text,
            # 网站内的所有链接
            links=links
        )
        yield item
        # 从主页面扩散到其他页面，不断执行请求
        yield from response.follow_all(links,callback=self.parse)
