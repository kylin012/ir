# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NkuinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    restext = scrapy.Field()
    links = scrapy.Field()

