# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjvkeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    meter = scrapy.Field()
    room = scrapy.Field()
    hall = scrapy.Field()
    money = scrapy.Field()
    housing_estate = scrapy.Field()
    detail_address = scrapy.Field()
    message = scrapy.Field()
